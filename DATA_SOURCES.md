# Data Sources & Provenance Register — P1 (T-InvIT Bengaluru RWA Tokenization)

Owner: Sandeep S (GitHub: SanKabira). Last updated: 2026-06-06.

Integrity rule: every figure used in the paper traces to a real, downloadable
source committed to this repo, OR — where the publisher blocks redistribution —
the retrieval URL and access date are documented here with the extracted figures
logged in a status file under `data/raw/`.

## Status Legend
- 🔴 Not collected
- 🟡 Identified; figures extracted but full PDF not redistributable (URL + date logged)
- 🟢 Collected and committed to /data/raw/

---

## Module 1: BMRCL / Namma Metro Phase 2A/2B Financial Viability

| # | Variable | Source | File in repo | Status | Date |
|---|---|---|---|---|---|
| 1 | Post-tax FIRR 1.921% | ADB Financial Analysis (ind-53326-001-fa.pdf, Nov 2020) | `data/raw/JICA_loans/ADB/ADB_FA_download_status.md` | 🟡 | 2026-06-06 |
| 2 | Post-tax WACC 2.629% (real) | ADB Financial Analysis, Table FA-2 | same | 🟡 | 2026-06-06 |
| 3 | DSCR < 1.0 to FY2034 (entity); sponsor support ₹83.6bn | ADB Financial Analysis | same | 🟡 | 2026-06-06 |
| 4 | Ridership anchors FY2025 (157,594/day) & FY2031 (600,651/day); 4.11% p.a. growth | ADB Financial Analysis | same | 🟡 | 2026-06-06 |
| 5 | Fare ₹2.85/pax-km; non-farebox 10% of farebox | ADB Financial Analysis | same | 🟡 | 2026-06-06 |
| 6 | Total project cost ₹139,088.8 million (Apr-2020 prices) | ADB Financial Analysis | same | 🟡 | 2026-06-06 |
| 7 | BMRCL statutory annual filing FY2023-24 | BMRCL (bmrc.co.in) | `data/raw/BMRCL/BMRCL_Annual_Report_2023-24.pdf` | 🟢 | 2026-06-06 |

> Note on #7: The file BMRCL published at the "Annual Report 2023-24" link is the
> RTI Act §25 statutory yearly report (request-disposal statistics), **not** a
> financial annual report. It is committed for provenance, but it contains **no**
> revenue/ridership figures. All financial/operational parameters in this paper
> therefore come from the ADB Financial Analysis (rows 1–6), which is the
> authoritative published source for this project's economics.

> Note on ADB PDF (🟡): adb.org returns HTTP 403 (Cloudflare) to automated
> download. The canonical URL and the complete extracted figure set are logged in
> `ADB_FA_download_status.md`. URL: https://www.adb.org/sites/default/files/linked-documents/ind-53326-001-fa.pdf

## Module 2: JICA ODA Loan (Phase 3)

| # | Variable | Source | File in repo | Status | Date |
|---|---|---|---|---|---|
| 8 | Loan ¥102,480 million; TORF + 80bp; 30-yr tenor, 10-yr grace | JICA Ex-Ante Evaluation (24 Mar 2026) | `data/raw/JICA_loans/JICA_BengaluruMetro_loanterms_2026-03-24.pdf` | 🟢 | 2026-06-06 |
| 9 | Press release / scope (Phase 3 lines, 252 cars) | JICA | `data/raw/JICA_loans/JICA_BengaluruMetro_loan_2026-03-24.html` | 🟢 | 2026-06-06 |
| — | Extracted terms summary | — | `data/raw/JICA_loans/JICA_loan_terms.txt` | 🟢 | 2026-06-06 |

## Module 3: PRR / Bengaluru Business Corridor (BBC) Land & Cost

| # | Variable | Source | File in repo | Status | Date |
|---|---|---|---|---|---|
| 10 | Total project ~₹27,000 cr; land acq ~₹21,000 cr; Package-1 bid ₹3,348 cr (SNC) | Moneycontrol (May 2026) | `data/raw/PRR_BBC/Moneycontrol_BBC_Package1_bid_result_2026-05.html` | 🟢 | 2026-06-06 |
| 11 | Land acquisition 948 acres; higher compensation policy | Deccan Herald | `data/raw/PRR_BBC/DeccanHerald_PRR_compensation_2026.html` | 🟢 | 2026-06-06 |
| 12 | Project background/overview | Moneycontrol | `data/raw/PRR_BBC/Moneycontrol_BBC_article_2026.html` | 🟢 | 2026-06-06 |
| 13 | BDA PRR-2 DPR consultancy tender (BDA/2023-24/SE0010) | BDA e-procurement | `data/raw/PRR_BBC/BDA_PRR2_DPR_tender_2024.html` | 🟢 | 2026-06-06 |
| — | Primary BDA DPR / Govt Order | — | `data/raw/PRR_BBC/PRR_source_status.md` | 🔴 | 2026-06-06 |

> Note on PRR primary doc: No completed DPR or Government Order is publicly
> available. A Feb-2024 BDA tender to *prepare* the PRR-2 DPR confirms the
> southern-stretch DPR was still being commissioned. Search log:
> `PRR_source_status.md`. Cost figures used in the paper are sourced from the
> most current public bid result (row 10), not from a primary DPR.

## Module 4: SEBI Regulatory (shared with P2)

| # | Variable | Source | File in repo | Status | Date |
|---|---|---|---|---|---|
| 14 | SEBI InvIT 3rd Amendment 2025 (min investment ₹1cr → ₹25L) | SEBI.gov.in | (committed in P2 repo: `data/raw/SEBI/`) | 🟢 | 2026-06-06 |
| 15 | SEBI Master Circular for InvITs (11 Jul 2025) | SEBI.gov.in | (committed in P2 repo: `data/raw/SEBI/`) | 🟢 | 2026-06-06 |

---

## Derived / processed outputs (this repo)

| File | Built by | Contents |
|---|---|---|
| `data/processed/firr_wacc_recompute.csv` | `notebooks/02_firr_wacc_forecast.py` | FIRR, WACC (reported + recomputed), viability gap |
| `data/processed/wacc_components.csv` | same | JICA/ADB/Equity weights & costs (WACC reproduces 2.629%) |
| `data/processed/ridership_forecast.csv` | same | FY2025–FY2045 ridership (ADB anchors + 4.11% p.a.) |
| `data/processed/revenue_forecast.csv` | same | Farebox + non-farebox revenue (ADB fare params) |
| `data/processed/firr_sensitivity_table.csv` | same | ±20% ridership/cost sensitivity (model simulation) |
| `data/processed/tokenization_scenario.csv` | same | T-InvIT lever scenario |
| `figures/fig1_wacc_firr_gap.png` … `fig4_*` | same | 4 figures at 300 DPI |

All forecast figures are labelled "ADB-parameterised projection": they
interpolate/extrapolate strictly between ADB's two published ridership anchors
(FY2025, FY2031) using ADB's own stated 4.11% p.a. growth. No observation is
fabricated.
