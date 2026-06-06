#!/usr/bin/env python3
"""
P1 — Notebook 02: FIRR/WACC Recomputation + Ridership/Revenue Forecast
Namma Metro Phase 2A/2B (Bengaluru Metro Rail Project, ADB Project 53326-001)

Author : Sandeep S | PhD Scholar, University of Mysore | GitHub: SanKabira
Paper  : P1 — T-InvIT Bengaluru RWA Tokenization

DATA INTEGRITY
--------------
ALL base parameters are extracted DIRECTLY from the ADB Financial Analysis
document (ind-53326-001-fa.pdf, ADB Nov 2020) — see
data/raw/JICA_loans/ADB/ADB_FA_download_status.md for the full extraction log
and the canonical URL. JICA loan terms are from JICA's Ex-Ante Evaluation
(data/raw/JICA_loans/). Project cost figures for the PRR/BBC corridor are from
the latest public bid results (data/raw/PRR_BBC/).

NO figure here is invented. Forecast cells are clearly labelled as
"ADB-PARAMETERISED PROJECTION" — they interpolate/extrapolate ONLY between the
two ridership anchor points that ADB itself published (FY2025 and FY2031) using
ADB's own stated post-2026 growth rate of 4.11% p.a. They are reproducible
projections built on real published anchors, not fabricated observations.

Outputs (all written to data/processed/ and figures/):
  - firr_wacc_recompute.csv
  - wacc_components.csv
  - ridership_forecast.csv
  - revenue_forecast.csv
  - firr_sensitivity_table.csv
  - tokenization_scenario.csv
  - fig1_wacc_firr_gap.png
  - fig2_ridership_forecast.png
  - fig3_revenue_forecast.png
  - fig4_firr_sensitivity_tornado.png
"""

import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy_financial as npf
from datetime import datetime

# ---------------------------------------------------------------------------
# Paths (run from repo root)
# ---------------------------------------------------------------------------
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROC = os.path.join(ROOT, "data", "processed")
FIGS = os.path.join(ROOT, "figures")
os.makedirs(PROC, exist_ok=True)
os.makedirs(FIGS, exist_ok=True)

DPI = 300
plt.rcParams.update({"figure.dpi": 110, "savefig.dpi": DPI, "font.size": 11,
                     "axes.grid": True, "grid.alpha": 0.3})

print("Run timestamp:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
print("Source: ADB ind-53326-001-fa.pdf (extracted) + JICA Ex-Ante Eval\n")

# ===========================================================================
# SECTION 1 — FIRR / WACC (ADB-REPORTED, primary data)
# ===========================================================================
ADB_FIRR = 0.01921   # post-tax project FIRR (ADB Table FA-1)
ADB_WACC = 0.02629   # post-tax real WACC  (ADB Table FA-2)
gap = ADB_FIRR - ADB_WACC

wacc_components = pd.DataFrame([
    {"source": "JICA Loan", "weight": 0.1724, "nominal_cost": 0.0142, "real_cost": 0.0000},
    {"source": "ADB Loan",  "weight": 0.2710, "nominal_cost": 0.0258, "real_cost": 0.0054},
    {"source": "Equity",    "weight": 0.5566, "nominal_cost": 0.0864, "real_cost": 0.0446},
])
# Reproduce WACC from components (real terms) as an integrity check
wacc_recomputed = float((wacc_components["weight"] * wacc_components["real_cost"]).sum())
wacc_components.to_csv(os.path.join(PROC, "wacc_components.csv"), index=False)

firr_wacc = pd.DataFrame([{
    "metric": "Post-tax FIRR (project)", "value_pct": ADB_FIRR * 100, "source": "ADB Table FA-1"},
    {"metric": "Post-tax WACC (real, reported)", "value_pct": ADB_WACC * 100, "source": "ADB Table FA-2"},
    {"metric": "WACC recomputed from components", "value_pct": wacc_recomputed * 100, "source": "computed"},
    {"metric": "Viability gap (FIRR - WACC)", "value_pct": gap * 100, "source": "computed"},
])
firr_wacc.to_csv(os.path.join(PROC, "firr_wacc_recompute.csv"), index=False)

print("=== Section 1: FIRR / WACC ===")
print(firr_wacc.to_string(index=False))
print(f"\nWACC reproduced from components (real): {wacc_recomputed*100:.3f}% "
      f"vs ADB reported {ADB_WACC*100:.3f}%")
print(f"Viability gap = {gap*100:.3f}% (NEGATIVE -> project below cost of capital "
      f"without sovereign support)\n")

# ===========================================================================
# SECTION 2 — RIDERSHIP FORECAST  (ADB-PARAMETERISED PROJECTION)
# Anchors published by ADB: FY2025 & FY2031 daily ridership; growth 4.11% p.a.
# ===========================================================================
# ADB anchor points (passengers/day), Phase 2A and Phase 2B
anchors = {
    2025: {"2A": 75754,  "2B": 81840},
    2031: {"2A": 289387, "2B": 311264},
}
GROWTH = 0.0411  # ADB stated post-2026 annual ridership growth

# CAGR implied by ADB's own two anchor points (integrity cross-check)
cagr_2a = (anchors[2031]["2A"] / anchors[2025]["2A"]) ** (1 / 6) - 1
cagr_2b = (anchors[2031]["2B"] / anchors[2025]["2B"]) ** (1 / 6) - 1

years = list(range(2025, 2046))  # 25-year operating horizon (FY2025-FY2045)
rows = []
for ph in ("2A", "2B"):
    base = anchors[2025][ph]
    base_2031 = anchors[2031][ph]
    cagr = (base_2031 / base) ** (1 / 6) - 1
    for y in years:
        if y <= 2031:
            val = base * (1 + cagr) ** (y - 2025)      # interpolate on ADB anchors
            method = "ADB anchor CAGR"
        else:
            val = base_2031 * (1 + GROWTH) ** (y - 2031)  # ADB post-2026 growth
            method = "ADB 4.11% p.a."
        rows.append({"fy": y, "phase": ph, "riders_per_day": round(val), "method": method})

ridership = pd.DataFrame(rows)
ridership_wide = ridership.pivot(index="fy", columns="phase", values="riders_per_day")
ridership_wide["total"] = ridership_wide["2A"] + ridership_wide["2B"]
ridership.to_csv(os.path.join(PROC, "ridership_forecast.csv"), index=False)

print("=== Section 2: Ridership forecast (ADB-parameterised) ===")
print(f"Implied ADB anchor CAGR FY25->FY31: 2A={cagr_2a*100:.2f}%  2B={cagr_2b*100:.2f}%")
print(ridership_wide.loc[[2025, 2031, 2045]].to_string())
print()

# ===========================================================================
# SECTION 3 — REVENUE FORECAST (ADB fare assumptions)
# Fare ₹2.85/pax-km (FY2020 base, ADB), no escalation; assume avg trip 12 km
# (typical metro avg lead distance). Non-farebox = 10% of farebox after ramp.
# These structural assumptions are ADB's own; trip length flagged as ASSUMPTION.
# ===========================================================================
FARE_PER_PAXKM = 2.85          # ADB FA assumption
AVG_TRIP_KM = 12.0             # ASSUMPTION (typical urban metro avg lead)
NONFAREBOX_RATIO = 0.10        # ADB FA: 10% of farebox after 2-yr ramp
DAYS = 365

rev_rows = []
for y in years:
    riders = float(ridership_wide.loc[y, "total"])
    farebox = riders * AVG_TRIP_KM * FARE_PER_PAXKM * DAYS / 1e7  # ₹ crore
    ramp = 0.0 if y <= 2026 else NONFAREBOX_RATIO   # ADB: ramp first 2 yrs
    nonfare = farebox * ramp
    rev_rows.append({"fy": y, "farebox_cr": round(farebox, 1),
                     "nonfarebox_cr": round(nonfare, 1),
                     "total_revenue_cr": round(farebox + nonfare, 1)})
revenue = pd.DataFrame(rev_rows)
revenue.to_csv(os.path.join(PROC, "revenue_forecast.csv"), index=False)

print("=== Section 3: Revenue forecast (₹ crore, ADB fare params) ===")
print(revenue[revenue["fy"].isin([2025, 2031, 2045])].to_string(index=False))
print()

# ===========================================================================
# SECTION 4 — FIRR SENSITIVITY (model simulation, clearly labelled)
# Elasticity-style adjustment around the ADB base FIRR.
# ===========================================================================
scenarios = {
    "Base Case (ADB)":   (1.00, 1.00),
    "Ridership +20%":    (1.20, 1.00),
    "Ridership -20%":    (0.80, 1.00),
    "Cost +20%":         (1.00, 1.20),
    "Cost -20%":         (1.00, 0.80),
    "T-InvIT (+10% rid, -10% cost)": (1.10, 0.90),
}
srows = []
for name, (rf, cf) in scenarios.items():
    adj = ADB_FIRR * rf / cf
    srows.append({"scenario": name, "firr_pct": round(adj * 100, 3),
                  "vs_wacc": "Viable" if adj > ADB_WACC else "Needs subsidy"})
sens = pd.DataFrame(srows)
sens.to_csv(os.path.join(PROC, "firr_sensitivity_table.csv"), index=False)

tok = pd.DataFrame([{
    "lever": "Lower equity cost via tokenized retail capital",
    "note": "T-InvIT broadens investor base; SEBI 3rd Amendment cut min "
            "investment to ₹25 lakh, deepening demand for infra units.",
    "base_firr_pct": ADB_FIRR * 100,
    "scenario_firr_pct": float(sens.loc[sens.scenario.str.startswith("T-InvIT"),
                                         "firr_pct"].iloc[0]),
    "wacc_pct": ADB_WACC * 100,
}])
tok.to_csv(os.path.join(PROC, "tokenization_scenario.csv"), index=False)

print("=== Section 4: FIRR sensitivity ===")
print(sens.to_string(index=False))
print()

# ===========================================================================
# FIGURES (all 300 DPI)
# ===========================================================================
# Fig 1 — FIRR vs WACC gap
fig, ax = plt.subplots(figsize=(7, 5))
bars = ax.bar(["FIRR\n(project)", "WACC\n(real)"], [ADB_FIRR * 100, ADB_WACC * 100],
              color=["#c0392b", "#2c3e50"], width=0.55)
for b, v in zip(bars, [ADB_FIRR * 100, ADB_WACC * 100]):
    ax.text(b.get_x() + b.get_width() / 2, v + 0.04, f"{v:.3f}%",
            ha="center", va="bottom", fontweight="bold")
ax.set_ylabel("Rate (%)")
ax.set_ylim(0, 3.1)
ax.set_title("Namma Metro Phase 2A/2B: FIRR below WACC\n"
             f"Viability gap = {gap*100:.3f}% (ADB FA, Project 53326-001)")
ax.annotate("", xy=(1, ADB_WACC * 100), xytext=(1, ADB_FIRR * 100),
            arrowprops=dict(arrowstyle="<->", color="#e67e22", lw=1.8))
ax.text(1.12, (ADB_FIRR + ADB_WACC) / 2 * 100, f"gap\n{gap*100:.3f}%",
        color="#e67e22", fontweight="bold", va="center")
plt.tight_layout()
plt.savefig(os.path.join(FIGS, "fig1_wacc_firr_gap.png"), dpi=DPI, bbox_inches="tight")
plt.close()

# Fig 2 — Ridership forecast
fig, ax = plt.subplots(figsize=(9, 5))
ax.plot(ridership_wide.index, ridership_wide["2A"], marker="o", ms=3,
        label="Phase 2A", color="#2980b9")
ax.plot(ridership_wide.index, ridership_wide["2B"], marker="s", ms=3,
        label="Phase 2B", color="#27ae60")
ax.plot(ridership_wide.index, ridership_wide["total"], marker="^", ms=3,
        label="Total", color="#8e44ad", lw=2)
for yr in (2025, 2031):
    ax.axvline(yr, color="grey", ls=":", lw=0.8)
ax.scatter([2025, 2031], [anchors[2025]["2A"], anchors[2031]["2A"]],
           color="red", zorder=5, s=40, label="ADB published anchors")
ax.scatter([2025, 2031], [anchors[2025]["2B"], anchors[2031]["2B"]],
           color="red", zorder=5, s=40)
ax.set_xlabel("Fiscal Year")
ax.set_ylabel("Ridership (passengers/day)")
ax.set_title("Ridership Forecast — ADB anchors (FY25, FY31) + 4.11% p.a. post-2031")
ax.legend(fontsize=9)
plt.tight_layout()
plt.savefig(os.path.join(FIGS, "fig2_ridership_forecast.png"), dpi=DPI, bbox_inches="tight")
plt.close()

# Fig 3 — Revenue forecast
fig, ax = plt.subplots(figsize=(9, 5))
ax.bar(revenue["fy"], revenue["farebox_cr"], label="Farebox", color="#16a085")
ax.bar(revenue["fy"], revenue["nonfarebox_cr"], bottom=revenue["farebox_cr"],
       label="Non-farebox (10%)", color="#f39c12")
ax.set_xlabel("Fiscal Year")
ax.set_ylabel("Revenue (₹ crore)")
ax.set_title("Projected Operating Revenue (ADB fare ₹2.85/pax-km, 12 km avg lead)")
ax.legend()
plt.tight_layout()
plt.savefig(os.path.join(FIGS, "fig3_revenue_forecast.png"), dpi=DPI, bbox_inches="tight")
plt.close()

# Fig 4 — Sensitivity tornado
fig, ax = plt.subplots(figsize=(8, 5))
sdf = sens[sens.scenario != "Base Case (ADB)"].copy()
sdf["delta"] = sdf["firr_pct"] - ADB_FIRR * 100
sdf = sdf.sort_values("delta")
colors = ["#27ae60" if d > 0 else "#c0392b" for d in sdf["delta"]]
ax.barh(sdf["scenario"], sdf["delta"], color=colors)
ax.axvline(0, color="black", lw=0.8)
ax.set_xlabel("Δ FIRR vs ADB base (percentage points)")
ax.set_title("FIRR Sensitivity (model simulation around ADB base FIRR 1.921%)")
for i, (d, s) in enumerate(zip(sdf["delta"], sdf["firr_pct"])):
    ax.text(d + (0.01 if d >= 0 else -0.01), i, f"{s:.2f}%",
            va="center", ha="left" if d >= 0 else "right", fontsize=8)
plt.tight_layout()
plt.savefig(os.path.join(FIGS, "fig4_firr_sensitivity_tornado.png"), dpi=DPI, bbox_inches="tight")
plt.close()

print("All processed CSVs and 4 figures (300 DPI) written.")
print("Figures:", [f for f in os.listdir(FIGS) if f.endswith(".png")])
