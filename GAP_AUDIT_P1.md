# GAP AUDIT — P1 (Bengaluru Metro / PRR T-InvIT Viability)

**Target journal:** Finance Research Letters (FRL, Elsevier; Scopus Q1, Finance).
**Reviewer stance:** senior finance-journal referee + quantitative research engineer.
**Audit date:** 2026-06-09. **Verdict on current draft:** *major revision* — the FIRR/WACC reproduction is sound and the honesty about data limits is a strength, but the forecast and sensitivity analysis are deterministic and assumption-driven in ways FRL referees will challenge.

Grounded in the committed code (`notebooks/02_firr_wacc_forecast.py`) and data (`data/raw/`, `data/processed/`).

FRL is a *letters* journal: ≤2,500–3,000 words, ≤4 exhibits, one sharp contribution. The uplift must raise rigour **without** bloating the paper — robustness goes to the repo/appendix, the letter stays tight.

---

## A. Prioritized fix-list (P0 = blocker, P1 = important, P2 = polish)

| # | Pri | Shortfall (current) | Fix delivered in this uplift |
|---|-----|---------------------|------------------------------|
| 1 | **P0** | **Deterministic sensitivity only.** `firr_sensitivity_table.csv` scales FIRR by ad-hoc ±20% multipliers (`adj = FIRR*rf/cf`) — not a real cash-flow re-solve, and no distribution. FRL referees expect a probabilistic treatment. | **Monte Carlo sensitivity surface**: re-solve FIRR from a parameterised cash-flow model over distributions on ridership growth, trip length, fare, cost, equity cost; report P(FIRR>WACC), percentile fan, tornado from variance decomposition. |
| 2 | **P0** | **FIRR is taken as ADB scalar, not reconstructed.** Paper "reproduces WACC" but FIRR (1.921%) is asserted from ADB, not re-derived from a cash-flow stream. Reviewers want the IRR re-solved from flows. | Build an explicit **annual cash-flow model** (capex, ridership→revenue, opex, terminal value) calibrated to ADB anchors; re-solve IRR with `numpy_financial.irr`; show it reproduces ADB's 1.921% within tolerance. |
| 3 | **P1** | **Key assumptions undefended.** 12 km avg trip length and the ±20% elasticity bands are stated, not justified or cited. | Defend **trip length** against published metro lead-distance evidence (cite CMP/benchmarks) and run MC over a 9–15 km range; replace ad-hoc elasticity with **fare/ridership elasticity ranges from transport-economics literature**. |
| 4 | **P1** | **Tokenization scenario is a single point.** "+10% ridership, −10% cost" → one FIRR (2.348%). No mechanism linking tokenization to cost-of-equity. | Model tokenization as a **cost-of-equity reduction channel** (broader investor base → lower required return); sweep equity-cost reduction 0–150 bp; report the FIRR/WACC gap closure curve. |
| 5 | **P1** | **T-InvIT regulatory feasibility asserted.** SEBI 25-lakh minimum mentioned but feasibility not rigorously mapped to InvIT regulation. | Add concise **regulatory feasibility mapping** (SEBI InvIT Regs + 2025 3rd Amendment provisions → T-InvIT structure), cross-referenced to P2's coded provisions. |
| 6 | **P1** | **Literature thin / dated.** 15 refs; needs 2023–2026 infra-finance, tokenization, PPP cost-of-capital sources. | Expand to **~22–25 refs**, 2023–2026 Scopus-indexed; fix DOIs to Elsevier/FRL style; drop non-citable items. |
| 7 | **P2** | **Contribution framing.** Three contributions stated but not sharply differentiated from prior metro-finance studies. | Tighten to one headline contribution (reproducible viability-gap + tokenization cost-of-equity lever for a real Indian asset) + two supporting. |
| 8 | **P2** | **Data-integrity caveats** (ADB PDF 403, BMRCL = RTI not financials) must remain visible. | Preserve verbatim in Data Availability + Limitations; no weakening. |

---

## B. What is already acceptable (keep intact)

- WACC reproduction from disclosed components (2.6288% vs ADB 2.629%) is a genuine, defensible integrity check — **keep as the anchor result.**
- Honest labelling of projections as "ADB-parameterised" and the BMRCL/ADB data caveats.
- 300-DPI figures and reproducible notebook.

## C. New analytical artifacts this uplift adds (P1)

1. `notebooks/03_montecarlo_firr.py` — explicit cash-flow IRR model + Monte Carlo (≥10,000 draws) over defended parameter distributions; tokenization cost-of-equity sweep. Runs end-to-end.
2. New processed tables: `firr_cashflow_model.csv`, `montecarlo_firr_summary.csv`, `tokenization_coe_sweep.csv`, `assumption_ranges.csv` (each parameter + literature source).
3. New 300-DPI figures: MC FIRR distribution vs WACC, percentile fan, variance-decomposition tornado, CoE-reduction gap-closure curve.
4. `CHANGELOG_P1.md` — reviewer-style response.

*Integrity:* the MC model is **calibrated to and reproduces ADB's published anchors**; it re-solves IRR from an explicit flow model rather than fabricating observations. Every distribution's range is documented with a source in `assumption_ranges.csv`. No invented data; projections remain labelled as projections.
