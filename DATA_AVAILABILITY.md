# Data Availability Statement

> Journal-ready template. Fill bracketed fields before submission. This statement is required by MDPI (JRFM), Elsevier (Finance Research Letters), and most Scopus-indexed journals.

---

## Standard statement (paste into manuscript)

> **Data Availability Statement:** The data and code that support the findings of this study are openly available in the GitHub repository **[REPO_NAME]** at **[REPO_URL]**, released under [CC BY 4.0 for text/figures; MIT for code]. Raw market data obtained from the National Stock Exchange of India (NSE) and Screener.in are subject to those providers' terms of use; where redistribution is restricted, the repository documents the exact retrieval URL and access date in `DATA_SOURCES.md` so that the dataset can be independently reconstructed. Regulatory texts are publicly available from the Securities and Exchange Board of India (SEBI). All processed datasets, analysis notebooks, and the scripts used to generate every figure and statistical result are included to enable full reproduction.

---

## Provenance summary

| Data category | Source (official) | Redistributable in repo? | Location |
|---|---|---|---|
| Listed-InvIT daily price / volume / bid-ask | NSE India | [Yes/No — per NSE terms] | `data/raw/NSE/` |
| InvIT financials (Core Watchlist) | Screener.in | [No — link only] | `data/raw/Screener/` |
| SEBI regulatory provisions | SEBI (official circulars) | Yes (public) | `data/raw/SEBI/` |
| Macroeconomic / infra (P1) | RBI, ADB, JICA, BDA, MOSPI | Yes (public docs) | `data/raw/` |
| Survey responses (if applicable) | Primary collection (Zoho) | [De-identified only] | `data/raw/survey/` |

## Reproducibility
- All notebooks fix `random_state = 42`.
- Software versions pinned in `requirements.txt`.
- Each figure file maps to a specific notebook cell (documented in the manuscript supplementary).

## Ethics / consent (if survey used)
- [Sample frame: documented in survey_design.md]
- [Consent obtained; data de-identified before commit]
- [IRB / institutional approval reference: ________]

---
*Last updated: [DATE] · Maintainer: Sandeep S (@SanKabira)*
