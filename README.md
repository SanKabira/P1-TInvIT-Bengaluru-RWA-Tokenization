# 🏙️ P1: Tokenizing Real-World Assets for Bengaluru Infrastructure

> **A Diagnostic and Prognostic Framework for the Tokenization of Real-World Assets (RWA) of Bengaluru's National Infrastructure Projects (Namma Metro, PRR/BBC) — Re-engineering the InvIT Structure using Blockchain and RBI-backed CBDC**

[![Scopus Target](https://img.shields.io/badge/Target-Scopus%20Q1%2FQ2-blue)](https://www.scopus.com)
[![Status](https://img.shields.io/badge/Status-Data%20Collection%20Phase-orange)]()
[![Python](https://img.shields.io/badge/Python-3.10%2B-green)]()
[![License](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey)]()

---

## 📌 Research Objective

This paper proposes a **Tokenized InvIT (T-InvIT)** framework that re-engineers India's infrastructure financing model by combining:
- SEBI-regulated InvIT structure
- RBI CBDC (Digital Rupee) as programmable settlement layer
- Permissioned blockchain (NPCI Vajra / Hyperledger Fabric)

Applied specifically to **Namma Metro (BMRCL)** and the **Bengaluru Business Corridor (PRR)** to solve the sovereign debt trap and land acquisition paralysis.

---

## 🗂️ Repository Structure

```
P1-TInvIT-Bengaluru-RWA-Tokenization/
│
├── 📁 data/
│   ├── raw/                    # Original downloaded datasets (do not modify)
│   │   ├── BMRCL/              # Annual reports, ADB financial analysis
│   │   ├── PRR_BBC/            # BDA cost data, land acquisition records
│   │   ├── JICA_loans/         # JICA ODA loan disclosures
│   │   ├── SEBI_regulations/   # SEBI InvIT Amendment circulars 2025
│   │   └── macroeconomic/      # RBI, MoF, MOSPI data (GDP, CPI, forex)
│   └── processed/              # Cleaned, analysis-ready datasets
│       ├── BMRCL_financials_clean.csv
│       ├── PRR_cost_timeline.csv
│       ├── JICA_forex_exposure.csv
│       └── macro_indicators.csv
│
├── 📁 notebooks/
│   ├── 01_FIRR_WACC_Recomputation.ipynb     # Reproduce ADB financial analysis
│   ├── 02_JICA_Forex_Risk_Model.ipynb       # Currency depreciation simulation
│   ├── 03_TInvIT_IRR_Simulator.ipynb        # T-InvIT vs traditional WACC
│   ├── 04_LPT_Valuation_Model.ipynb         # Land Pooling Token pricing
│   ├── 05_Revenue_Waterfall_Simulation.ipynb # Smart contract cash flow model
│   ├── 06_ARIMA_Ridership_Forecast.ipynb    # Namma Metro ridership forecasting
│   └── 07_Macro_INR_Hedge_Analysis.ipynb    # T-InvIT as INR stabilizer
│
├── 📁 figures/
│   ├── fig1_TInvIT_architecture.png
│   ├── fig2_revenue_waterfall.png
│   ├── fig3_FIRR_WACC_comparison.png
│   ├── fig4_forex_risk_exposure.png
│   └── fig5_roadmap_2026_2030.png
│
├── 📁 paper/
│   ├── draft_v1.md              # Current manuscript draft
│   ├── references.bib           # BibTeX citations (Zotero export)
│   ├── supplementary_material.md
│   └── submission/              # Journal-formatted versions
│
├── 📁 sub_agents/
│   ├── DataAgent_ADB.py         # Downloads/parses ADB financial PDFs
│   ├── DataAgent_BMRCL.py       # Scrapes BMRCL annual report data
│   ├── DataAgent_SEBI.py        # Extracts SEBI regulatory provisions
│   ├── LitAgent_P1.py           # Google Scholar/Scopus citation search
│   └── agent_orchestrator.py   # Master orchestration script
│
├── 📁 environments/
│   ├── requirements.txt         # Python dependencies
│   └── environment.yml          # Conda environment
│
├── DATA_SOURCES.md              # Complete data provenance documentation
├── METHODOLOGY.md               # Statistical methods and reproducibility guide
├── JOURNAL_TARGETS.md           # Target Scopus journals with IF and submission guidelines
└── MASTER_PROMPT.md             # 🤖 AI sub-agent orchestration master prompt
```

---

## 📊 Target Data Sources (Verified, Non-Fabricated)

| Dataset | Source | URL | Access Method |
|---|---|---|---|
| BMRCL Financial Analysis | Asian Development Bank | [ADB RRP](https://www.adb.org/sites/default/files/linked-documents/ind-53326-001-fa.pdf) | Direct PDF download |
| JICA ODA Loan Terms | JICA India | [JICA Press](https://www.jica.go.jp/india/english/office/topics/) | Web scrape |
| PRR/BBC Cost Data | BDA / Times of India | Public sources | Web scrape + manual |
| SEBI InvIT Amendments 2025 | SEBI.gov.in | [SEBI Circulars](https://www.sebi.gov.in) | PDF extract |
| RBI CBDC FAQs & Reports | RBI.org.in | [RBI CBDC](https://www.rbi.org.in) | Direct download |
| India GDP/CPI/Forex | MOSPI / RBI DBIE | [DBIE](https://dbie.rbi.org.in) | API / CSV |

---

## 🎯 Target Journals (Scopus)

| Journal | Publisher | Scopus Quartile | Impact Factor | Notes |
|---|---|---|---|---|
| Finance Research Letters | Elsevier | Q1 | ~9.8 | Fast-track, accepts empirical finance |
| Journal of Risk and Financial Management | MDPI | Q2 | ~2.2 | Open access, strong on emerging markets |
| IIMB Management Review | Elsevier | Q2 | ~2.5 | India-focused, policy-relevant |

---

## ⚠️ Data Integrity Commitment

All datasets in this repository are:
- ✅ Downloaded from official, citable sources
- ✅ Timestamped at collection
- ✅ Linked to notebook cells via provenance comments
- ❌ NOT synthetically generated or manually fabricated

Every statistical result is reproducible by running the notebooks in sequence.

---

## 👤 Author
**Sandeep S** | PhD Research Scholar, REITs & InvITs | University of Mysore  
MScFE, WorldQuant University | Bengaluru, Karnataka, India
