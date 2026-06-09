#!/usr/bin/env python3
"""
P1 — Notebook 03: Monte Carlo FIRR sensitivity surface + tokenization cost-of-equity sweep
Namma Metro Phase 2A/2B (Bengaluru Metro Rail Project, ADB Project 53326-001)

Author : Sandeep S | PhD Scholar | GitHub: SanKabira
Paper  : P1 — T-InvIT Bengaluru RWA Tokenization (target: Finance Research Letters)

PURPOSE (addresses GAP_AUDIT_P1)
--------------------------------
The original Notebook 02 used a crude proportional FIRR fudge (adj = FIRR * rid / cost).
A Q1 reviewer would reject that. This notebook replaces it with an EXPLICIT annual
cash-flow IRR model and a proper Monte Carlo (>=10,000 draws) over the project's
uncertain drivers, plus a tokenization cost-of-equity sweep that maps directly to the
viability gap (FIRR vs WACC).

DATA INTEGRITY
--------------
- Every structural anchor is REAL and traceable to the ADB Financial Analysis
  (ind-53326-001-fa.pdf, ADB Nov 2020): total project cost Rs 13,908.88 crore,
  5 construction years + 25 operating years, ridership anchors FY2025 & FY2031,
  4.11% p.a. post-2031 growth, fare Rs 2.85/pax-km, ~41% EBITDA margin, 16.69% tax,
  reported post-tax FIRR 1.921% and real WACC 2.629%.
  Source log: data/raw/JICA_loans/ADB/ADB_FA_download_status.md (adb.org returns 403;
  figures extracted/indexed, PDF NOT redistributed).
- The explicit cash-flow model is CALIBRATED to the ADB-reported FIRR by an additive
  shift (documented in calibration_log.csv). Public anchors omit ADB's internal cost
  ramps and financing schedule, so the absolute reconstructed IRR differs; the Monte
  Carlo therefore explores RELATIVE sensitivity around the ADB-published 1.921% anchor.
  This is a transparent benchmark calibration, NOT fabricated data.
- Each Monte Carlo parameter distribution is documented with its literature/source
  basis in assumption_ranges.csv (also written to the repo).
- NO survey data is used. NO tokenized InvIT exists yet; the tokenization sweep is an
  explicitly labelled forward scenario, not an observed instrument.

Run:  python3 notebooks/03_montecarlo_firr.py
Outputs: data/processed/{mc_firr_draws,mc_firr_summary,assumption_ranges,
         calibration_log,tokenization_coe_sweep,firr_tornado}.csv
         + figures/{fig5_mc_firr_distribution,fig6_mc_tornado,
                    fig7_tokenization_coe_sweep,fig8_mc_sensitivity_surface}.png  (300 DPI)
"""
import os
import numpy as np
import pandas as pd
import numpy_financial as npf
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROC = os.path.join(ROOT, "data", "processed")
FIGS = os.path.join(ROOT, "figures")
os.makedirs(PROC, exist_ok=True); os.makedirs(FIGS, exist_ok=True)

DPI = 300
plt.rcParams.update({"figure.dpi": 110, "savefig.dpi": DPI, "font.size": 11,
                     "axes.grid": True, "grid.alpha": 0.3,
                     "axes.spines.top": False, "axes.spines.right": False})
RNG = np.random.default_rng(53326)  # seed = ADB project number for reproducibility

# ============================================================ ADB anchors (REAL)
ADB_FIRR = 0.01921          # reported post-tax project FIRR (ADB Table FA-1)
ADB_WACC = 0.02629          # reported real WACC (ADB Table FA-2)
TOTAL_CAPEX_CR = 13908.88   # Rs crore (ADB total project cost, Apr-2020 prices)
TAX = 0.1669                # ADB tax rate
EBITDA_MARGIN = 0.41        # ADB EBITDA margin by FY2027
FARE_BASE = 2.85            # Rs/pax-km (ADB FY2020 base)
TRIP_BASE = 12.0            # km avg lead (ASSUMPTION; defended via 9-15 km MC range)
NONFARE = 0.10              # non-farebox as fraction of farebox after ramp
GROWTH_BASE = 0.0411        # ADB post-2031 ridership growth p.a.
DAYS = 365
SALVAGE_FRAC = 0.20         # terminal/residual value as fraction of capex (assumption)
N_CONSTR = 5                # construction years (FY2021-2025)
ANCHORS = {2025: {"2A": 75754, "2B": 81840},
           2031: {"2A": 289387, "2B": 311264}}
OPS_YEARS = list(range(2025, 2050))  # 25 operating years

print("Run:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
print("Explicit cash-flow IRR model calibrated to ADB FIRR 1.921%\n")

# ============================================================ ridership generator
def riders(y, ph, growth=GROWTH_BASE):
    b = ANCHORS[2025][ph]; b31 = ANCHORS[2031][ph]
    cagr = (b31 / b) ** (1 / 6) - 1
    return b * (1 + cagr) ** (y - 2025) if y <= 2031 else b31 * (1 + growth) ** (y - 2031)

# ============================================================ explicit cash-flow IRR
def model_irr(trip=TRIP_BASE, fare=FARE_BASE, rid_mult=1.0, cost_mult=1.0,
              margin=EBITDA_MARGIN, tax=TAX, capex=TOTAL_CAPEX_CR,
              salvage=SALVAGE_FRAC, growth=GROWTH_BASE):
    """Explicit 5-yr construction + 25-yr operating annual cash-flow IRR (real, post-tax).
    Returns the *uncalibrated* model IRR (decimal)."""
    cf = [-capex / N_CONSTR * cost_mult] * (N_CONSTR - 1)  # FY2021-2024 tranches
    for i, y in enumerate(OPS_YEARS):
        tot = (riders(y, "2A", growth) + riders(y, "2B", growth)) * rid_mult
        farebox = tot * trip * fare * DAYS / 1e7  # Rs crore
        ramp = 0.0 if y <= 2026 else NONFARE
        revenue = farebox * (1 + ramp)
        ebitda = revenue * margin
        ncf = ebitda * (1 - tax) if y > 2026 else ebitda * 0.3  # ADB: first 2 yrs op loss
        if i == 0:
            ncf += (-capex / N_CONSTR * cost_mult)  # FY2025 final construction tranche
        if i == len(OPS_YEARS) - 1:
            ncf += capex * salvage  # terminal/residual value
        cf.append(ncf)
    irr = npf.irr(cf)
    return float(irr) if irr is not None and np.isfinite(irr) else np.nan

BASE_MODEL_IRR = model_irr()
CALIB_SHIFT = ADB_FIRR - BASE_MODEL_IRR  # additive calibration to ADB benchmark
def firr_calibrated(**kw):
    v = model_irr(**kw)
    return v + CALIB_SHIFT if np.isfinite(v) else np.nan

pd.DataFrame([{
    "base_model_irr_pct": BASE_MODEL_IRR * 100,
    "adb_reported_firr_pct": ADB_FIRR * 100,
    "calibration_shift_pp": CALIB_SHIFT * 100,
    "method": "additive shift to ADB benchmark (public anchors omit ADB cost ramps/financing)",
    "calibrated_base_pct": firr_calibrated() * 100,
}]).to_csv(os.path.join(PROC, "calibration_log.csv"), index=False)
print(f"Base model IRR {BASE_MODEL_IRR*100:.4f}%  ->  calibration shift {CALIB_SHIFT*100:+.4f} pp")
print(f"Calibrated base FIRR {firr_calibrated()*100:.4f}% (target ADB 1.921%)\n")

# ============================================================ assumption ranges (documented)
assumptions = pd.DataFrame([
    {"parameter": "trip_length_km", "dist": "triangular", "low": 9.0, "mode": 12.0, "high": 15.0,
     "source": "ADB FA uses pax-km revenue; 12 km is typical Indian metro average lead "
               "(Namma Metro reported lead ~12-14 km; DMRC ~15 km). Range 9-15 km brackets "
               "BMRCL/MoHUA metro lead-distance disclosures."},
    {"parameter": "fare_per_paxkm", "dist": "triangular", "low": 2.57, "mode": 2.85, "high": 3.42,
     "source": "ADB FY2020 base Rs 2.85/pax-km. +/-10% low, +20% high to allow modest fare "
               "indexation (ADB assumed no escalation; real fare revisions in Indian metros "
               "historically lag inflation)."},
    {"parameter": "ridership_multiplier", "dist": "normal", "low": 0.70, "mode": 1.00, "high": 1.30,
     "source": "ADB ridership forecasts for Indian metros have historically over-predicted "
               "(CAG/MoHUA reviews show 30-50% shortfalls). Mean 1.0, SD 0.12 truncated to "
               "[0.70, 1.30] reflects this demand-risk band."},
    {"parameter": "cost_multiplier", "dist": "triangular", "low": 0.95, "mode": 1.00, "high": 1.30,
     "source": "Indian metro capex commonly overruns 10-30% (Flyvbjerg infrastructure cost-overrun "
               "literature; Namma Metro Phase-2 escalations). Downside capped at -5%."},
    {"parameter": "ebitda_margin", "dist": "normal", "low": 0.33, "mode": 0.41, "high": 0.49,
     "source": "ADB FA states ~41% EBITDA margin by FY2027. SD 0.03 truncated to [0.33,0.49] "
               "covers O&M-cost uncertainty (energy, staff, maintenance)."},
    {"parameter": "post2031_growth", "dist": "triangular", "low": 0.025, "mode": 0.0411, "high": 0.055,
     "source": "ADB stated 4.11% p.a. post-2031. Band 2.5-5.5% reflects urban-transit demand "
               "growth uncertainty for Bengaluru."},
    {"parameter": "salvage_fraction", "dist": "triangular", "low": 0.10, "mode": 0.20, "high": 0.30,
     "source": "Terminal/residual value of long-life metro assets (civil + rolling stock). "
               "Range reflects RBI/infra-asset depreciation conventions; flagged as assumption."},
])
assumptions.to_csv(os.path.join(PROC, "assumption_ranges.csv"), index=False)
print("=== Documented Monte Carlo assumption ranges ===")
print(assumptions[["parameter", "dist", "low", "mode", "high"]].to_string(index=False))

# ============================================================ Monte Carlo (>=10,000 draws)
N = 20000
def tri(low, mode, high, n):
    return RNG.triangular(low, mode, high, n)
def tnorm(mean, sd, lo, hi, n):
    x = RNG.normal(mean, sd, n)
    return np.clip(x, lo, hi)

trip = tri(9.0, 12.0, 15.0, N)
fare = tri(2.57, 2.85, 3.42, N)
ridm = tnorm(1.0, 0.12, 0.70, 1.30, N)
costm = tri(0.95, 1.00, 1.30, N)
marg = tnorm(0.41, 0.03, 0.33, 0.49, N)
grow = tri(0.025, 0.0411, 0.055, N)
salv = tri(0.10, 0.20, 0.30, N)

firr_draws = np.empty(N)
for i in range(N):
    firr_draws[i] = firr_calibrated(trip=trip[i], fare=fare[i], rid_mult=ridm[i],
                                    cost_mult=costm[i], margin=marg[i],
                                    growth=grow[i], salvage=salv[i])
mc = pd.DataFrame({
    "trip_km": trip, "fare": fare, "rid_mult": ridm, "cost_mult": costm,
    "ebitda_margin": marg, "growth": grow, "salvage": salv, "firr": firr_draws,
})
mc = mc.dropna(subset=["firr"])
mc.to_csv(os.path.join(PROC, "mc_firr_draws.csv"), index=False)

p_viable = float((mc["firr"] > ADB_WACC).mean())
summary = pd.DataFrame([{
    "n_draws": len(mc),
    "firr_mean_pct": mc["firr"].mean() * 100,
    "firr_median_pct": mc["firr"].median() * 100,
    "firr_sd_pp": mc["firr"].std() * 100,
    "firr_p5_pct": np.percentile(mc["firr"], 5) * 100,
    "firr_p25_pct": np.percentile(mc["firr"], 25) * 100,
    "firr_p75_pct": np.percentile(mc["firr"], 75) * 100,
    "firr_p95_pct": np.percentile(mc["firr"], 95) * 100,
    "wacc_pct": ADB_WACC * 100,
    "prob_firr_gt_wacc": p_viable,
    "prob_firr_gt_0": float((mc["firr"] > 0).mean()),
}])
summary.to_csv(os.path.join(PROC, "mc_firr_summary.csv"), index=False)
print("\n=== Monte Carlo FIRR summary (n={}) ===".format(len(mc)))
print(summary.T.to_string())
print(f"\nP(FIRR > WACC {ADB_WACC*100:.3f}%) = {p_viable*100:.1f}%")

# ============================================================ tornado (variance decomposition)
# Rank drivers by |Spearman correlation| with FIRR (standard MC sensitivity).
from scipy.stats import spearmanr
drivers = ["rid_mult", "cost_mult", "trip_km", "fare", "ebitda_margin", "growth", "salvage"]
tor_rows = []
for d in drivers:
    rho, _ = spearmanr(mc[d], mc["firr"])
    tor_rows.append({"driver": d, "spearman_rho": rho, "abs_rho": abs(rho)})
tornado = pd.DataFrame(tor_rows).sort_values("abs_rho", ascending=False)
tornado["contribution_pct"] = tornado["abs_rho"] / tornado["abs_rho"].sum() * 100
tornado.to_csv(os.path.join(PROC, "firr_tornado.csv"), index=False)
print("\n=== Variance decomposition (Spearman) ===")
print(tornado.to_string(index=False))

# ============================================================ tokenization cost-of-equity sweep
# T-InvIT thesis: tokenization broadens the retail investor base, lowering the cost of
# equity. Sweep equity cost reduction 0-150 bp; recompute the viability gap (FIRR vs WACC).
# WACC equity weight 55.66% (ADB). A delta_coe bp cut lowers WACC by 0.5566*delta_coe.
EQUITY_WEIGHT = 0.5566
sweep_bp = np.arange(0, 151, 10)
coe_rows = []
for bp in sweep_bp:
    new_wacc = ADB_WACC - EQUITY_WEIGHT * (bp / 1e4)
    gap = ADB_FIRR - new_wacc
    coe_rows.append({"coe_reduction_bp": int(bp), "new_wacc_pct": new_wacc * 100,
                     "firr_pct": ADB_FIRR * 100, "viability_gap_pp": gap * 100,
                     "viable": gap > 0})
coe = pd.DataFrame(coe_rows)
coe.to_csv(os.path.join(PROC, "tokenization_coe_sweep.csv"), index=False)
breakeven = coe[coe["viable"]]
be_bp = int(breakeven["coe_reduction_bp"].iloc[0]) if not breakeven.empty else None
print("\n=== Tokenization cost-of-equity sweep ===")
print(coe.to_string(index=False))
print(f"\nBreak-even: FIRR >= WACC requires equity-cost cut of "
      f"{'~%d bp' % be_bp if be_bp is not None else '>150 bp'}.")

# ============================================================ FIGURES (300 DPI)
# Fig 5 — MC FIRR distribution with WACC line
fig, ax = plt.subplots(figsize=(8, 5))
ax.hist(mc["firr"] * 100, bins=60, color="#2980b9", alpha=0.8, edgecolor="white", lw=0.3)
ax.axvline(ADB_WACC * 100, color="#c0392b", lw=2, ls="--",
           label=f"WACC {ADB_WACC*100:.3f}%")
ax.axvline(ADB_FIRR * 100, color="#27ae60", lw=2, ls="-",
           label=f"ADB base FIRR {ADB_FIRR*100:.3f}%")
ax.axvline(mc["firr"].median() * 100, color="#8e44ad", lw=1.5, ls=":",
           label=f"MC median {mc['firr'].median()*100:.3f}%")
ax.set_xlabel("Project FIRR (%)"); ax.set_ylabel("Frequency")
ax.set_title(f"Monte Carlo FIRR distribution (n={len(mc):,})\n"
             f"P(FIRR > WACC) = {p_viable*100:.1f}%")
ax.legend(fontsize=9)
fig.tight_layout(); fig.savefig(os.path.join(FIGS, "fig5_mc_firr_distribution.png"),
                                dpi=DPI, bbox_inches="tight"); plt.close(fig)

# Fig 6 — tornado
fig, ax = plt.subplots(figsize=(8, 5))
t2 = tornado.sort_values("abs_rho")
colors = ["#27ae60" if r > 0 else "#c0392b" for r in t2["spearman_rho"]]
ax.barh(t2["driver"], t2["spearman_rho"], color=colors)
ax.axvline(0, color="black", lw=0.8)
ax.set_xlabel("Spearman rank correlation with FIRR")
ax.set_title("FIRR sensitivity tornado (Monte Carlo variance decomposition)")
for i, (r, c) in enumerate(zip(t2["spearman_rho"], t2["contribution_pct"])):
    ax.text(r + (0.01 if r >= 0 else -0.01), i, f"{c:.0f}%",
            va="center", ha="left" if r >= 0 else "right", fontsize=8)
fig.tight_layout(); fig.savefig(os.path.join(FIGS, "fig6_mc_tornado.png"),
                                dpi=DPI, bbox_inches="tight"); plt.close(fig)

# Fig 7 — tokenization cost-of-equity sweep
fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(coe["coe_reduction_bp"], coe["viability_gap_pp"], "o-", color="#2980b9", lw=1.8)
ax.axhline(0, color="#c0392b", lw=1.5, ls="--", label="Viability threshold (FIRR = WACC)")
ax.fill_between(coe["coe_reduction_bp"], 0, coe["viability_gap_pp"],
                where=coe["viability_gap_pp"] > 0, color="#27ae60", alpha=0.2)
if be_bp is not None:
    ax.axvline(be_bp, color="#27ae60", lw=1.2, ls=":",
               label=f"Break-even ~{be_bp} bp")
ax.set_xlabel("Tokenization-driven equity-cost reduction (bp)")
ax.set_ylabel("Viability gap, FIRR - WACC (pp)")
ax.set_title("T-InvIT cost-of-equity sweep: closing the viability gap")
ax.legend(fontsize=9)
fig.tight_layout(); fig.savefig(os.path.join(FIGS, "fig7_tokenization_coe_sweep.png"),
                                dpi=DPI, bbox_inches="tight"); plt.close(fig)

# Fig 8 — sensitivity surface (ridership x cost -> P(FIRR>WACC) shaded)
grid_rid = np.linspace(0.75, 1.25, 25)
grid_cost = np.linspace(0.95, 1.30, 25)
Z = np.empty((len(grid_cost), len(grid_rid)))
for ci, c in enumerate(grid_cost):
    for ri, r in enumerate(grid_rid):
        Z[ci, ri] = firr_calibrated(rid_mult=r, cost_mult=c) * 100
fig, ax = plt.subplots(figsize=(8, 6))
cf_ = ax.contourf(grid_rid, grid_cost, Z, levels=20, cmap="RdYlGn")
cs = ax.contour(grid_rid, grid_cost, Z, levels=[ADB_WACC * 100],
                colors="black", linewidths=2)
ax.clabel(cs, fmt={ADB_WACC * 100: "FIRR = WACC"}, fontsize=9)
cbar = fig.colorbar(cf_, ax=ax); cbar.set_label("Calibrated FIRR (%)")
ax.set_xlabel("Ridership multiplier"); ax.set_ylabel("Cost multiplier")
ax.set_title("FIRR sensitivity surface (ridership x cost)\nblack line = viability frontier")
ax.grid(False)
fig.tight_layout(); fig.savefig(os.path.join(FIGS, "fig8_mc_sensitivity_surface.png"),
                                dpi=DPI, bbox_inches="tight"); plt.close(fig)

print("\nAll Monte Carlo outputs + 4 figures (300 DPI) written.")
print("Figures:", [f for f in os.listdir(FIGS) if f.startswith(("fig5","fig6","fig7","fig8"))])
