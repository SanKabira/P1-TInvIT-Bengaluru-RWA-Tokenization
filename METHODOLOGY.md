# 📐 Methodology & Reproducibility Guide — P1

## Research Design
**Type:** Diagnostic + Prognostic Framework with Quantitative Modeling  
**Approach:** Mixed Methods — Financial analysis + Policy simulation + Macroeconomic modeling

---

## Statistical & Analytical Methods

### M1: FIRR/WACC Recomputation (Notebook 01)
- **Purpose:** Independently verify ADB financial viability indicators
- **Data:** BMRCL Phase 2A/2B cost, revenue, debt schedule from ADB PDF
- **Method:** NPV-based FIRR recalculation; WACC = weighted cost of equity + debt
- **Tool:** Python (numpy_financial, pandas)
- **Output:** Verified FIRR and WACC with sensitivity table (±1% scenarios)

### M2: Forex Risk Quantification (Notebook 02)
- **Purpose:** Quantify hidden cost of JICA/ADB loans due to INR depreciation
- **Data:** INR/JPY rates 2010–2025 (RBI DBIE), loan tenor 40 years
- **Method:** Monte Carlo simulation (10,000 paths) of INR depreciation
  - Distribution: GBM (Geometric Brownian Motion) fitted to historical returns
  - Output: Distribution of effective interest rate burden
- **Tool:** Python (scipy, numpy)

### M3: T-InvIT IRR Simulation (Notebook 03)
- **Purpose:** Compare WACC reduction under T-InvIT vs traditional structure
- **Method:** DCF model with retail CBDC settlement cost assumptions
  - Scenario 1: Traditional (broker intermediation, T+2 settlement)
  - Scenario 2: T-InvIT (atomic DvP, 247 market, fractional units)
- **Output:** IRR differential, payback period comparison table

### M4: ARIMA Ridership Forecast (Notebook 06)
- **Purpose:** Generate independent ridership projections for MYT yield modeling
- **Data:** BMRCL historical ridership (Phase 1: 2011–2024)
- **Method:** ARIMA(p,d,q) with auto_arima; Prophet for seasonal decomposition
- **Validation:** Hold-out test 2022–2024, MAPE < 10%

---

## Reproducibility Protocol

1. Run `00_setup.ipynb` to install dependencies
2. Run `DataAgent_BMRCL.py` to populate `/data/raw/BMRCL/`
3. Run notebooks in sequence (01 → 07)
4. All figures auto-saved to `/figures/`
5. All processed outputs auto-saved to `/data/processed/`

## Software Versions
- Python 3.10+
- pandas 2.x, numpy 1.26+, scipy 1.12+, statsmodels 0.14+
- arch 6.x (GARCH), prophet 1.1+, numpy_financial 1.0+
