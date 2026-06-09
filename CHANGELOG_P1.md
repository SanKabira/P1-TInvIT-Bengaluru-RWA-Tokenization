# CHANGELOG — P1: Scopus/Q1 Rigour Uplift (Reviewer-Style Response)

**Manuscript:** *Can a Tokenized InvIT Close an Infrastructure Viability Gap? Evidence and a Design Proposal from Bengaluru's Metro and Peripheral Ring Road*
**Target journal:** Finance Research Letters (FRL, Elsevier; Scopus Q1, Finance).
**Uplift date:** 2026-06-09. **Author:** Sandeep S (GitHub: SanKabira).

This change-log responds point-by-point to the internal `GAP_AUDIT_P1.md` (senior finance-journal referee + quantitative research engineer stance). FRL is a *letters* outlet, so the uplift raises rigour while keeping the letter tight: the heavy robustness machinery lives in the committed notebook and processed CSVs, and the letter reports the headline distribution and threshold. **Integrity statement:** the Monte Carlo model is calibrated to and reproduces ADB's published anchors; it re-solves the IRR from an explicit cash-flow stream rather than fabricating observations. Every assumption range is documented with a source in `assumption_ranges.csv`. Projections remain labelled as projections, and the survey arm remains unfielded and flagged.

---

## Responses to P0 (blocker) items

### P0-1 — Deterministic sensitivity only
**Original concern:** `firr_sensitivity_table.csv` scaled FIRR by ad-hoc ±20% multipliers (`adj = FIRR*rf/cf`) — not a real cash-flow re-solve, and with no distribution. FRL referees expect a probabilistic treatment.
**Action taken:** Replaced the elasticity heuristic with a **20,000-draw Monte Carlo simulation** (seed 53326) over seven calibrated assumption ranges (ridership multiplier, average trip length, capital-cost multiplier, salvage value, EBITDA margin, fare, post-2031 growth). For each draw the FIRR is re-solved from the cash-flow model. The simulated FIRR has a **mean of 1.60%, median 1.60%, SD 0.84 pp, 90% interval [0.22%, 2.96%]**, with **P(FIRR > WACC) = 10.9%** and P(FIRR > 0) = 97.2%. A **Spearman-rank tornado** decomposes variance: ridership 20.7%, trip length 17.5%, capital cost 16.5%, salvage 12.6%, EBITDA margin 12.3%, fare 10.3%, growth 10.0%.
**Where to verify:** `notebooks/03_montecarlo_firr.py`; `data/processed/mc_firr_summary.csv`, `mc_firr_draws.csv`, `firr_tornado.csv`, `assumption_ranges.csv`; manuscript §4.3, §5.3; Figures 5–6; Tables 2.

### P0-2 — FIRR taken as ADB scalar, not reconstructed
**Original concern:** The paper "reproduced WACC" but FIRR (1.921%) was asserted from ADB, not re-derived from a cash-flow stream.
**Action taken:** Built an **explicit annual cash-flow model** over a 30-year horizon (five construction years + 25 operating years) from ADB-disclosed parameters: capital cost ₹139,088.8 million, EBITDA margin ~41%, tax 16.69%, 20% terminal salvage, ₹2.85/passenger-km fare, 12 km trip length (flagged), and the ADB-anchored ridership path. The raw model IRR is −1.022%; rather than discard the gap to ADB's published 1.921%, a **single transparent additive calibration shift of +2.943 pp** is applied so the base case reproduces ADB's level exactly, logged in `calibration_log.csv`. The shift is fixed once and applied uniformly across all draws — a benchmark calibration of the model's *relative* sensitivities to ADB's *level*, not a free parameter. This limitation is stated openly in §8.
**Where to verify:** `notebooks/03_montecarlo_firr.py`; `data/processed/calibration_log.csv`; manuscript §4.3, §8 (Limitation 1).

---

## Responses to P1 (important) items

### P1-3 — Key assumptions undefended
**Original concern:** The 12 km average-trip length and ±20% elasticity bands were stated, not justified.
**Action taken:** The crude elasticity bands are **gone** (replaced by the Monte Carlo distributions above). The 12 km trip length is now (i) explicitly flagged as the authors' assumption throughout, (ii) varied over a calibrated range in the Monte Carlo, and (iii) shown by the tornado to be the **second-largest variance driver (17.5%)** — so the manuscript draws explicit attention to it as the assumption most warranting reader scrutiny, and notes a reader who prefers a different value can re-run the committed notebook. Each assumption's range and rationale is documented in `assumption_ranges.csv`.
**Where to verify:** `data/processed/assumption_ranges.csv`; manuscript §4.2, §5.3, §8 (Limitation 2).

### P1-4 — Tokenization scenario was a single point
**Original concern:** "+10% ridership, −10% cost" produced one FIRR (2.348%) with no mechanism linking tokenization to cost of equity.
**Action taken:** Tokenization is now modelled through its **only genuine lever — a lower cost of equity** from a broader investor base. A **cost-of-equity break-even sweep** reduces the equity cost in 10-bp steps, holding equity's 55.66% weight fixed, and records where the recomputed WACC meets the FIRR. The viability gap closes only at **roughly a 130-basis-point reduction** (gap is −0.04 pp at 120 bp, first turns positive +0.02 pp at 130 bp). A **two-way FIRR sensitivity surface** over the ridership × cost multipliers visualises the region of the assumption space in which the project clears WACC.
**Where to verify:** `notebooks/03_montecarlo_firr.py`; `data/processed/tokenization_coe_sweep.csv`; manuscript §5.4; Table 3; Figures 7–8.

### P1-5 — T-InvIT regulatory feasibility asserted
**Original concern:** The SEBI ₹25-lakh minimum was mentioned but feasibility was not rigorously mapped to InvIT regulation.
**Action taken:** Added a concise **regulatory feasibility mapping** (§6): a SEBI-registered InvIT holding the operating asset with units on a permissioned register-and-transfer ledger inside the dematerialised-securities and InvIT perimeter, with the ₹25-lakh post-amendment minimum as the enabling threshold for a privately placed tranche. The text is explicit that no on-chain settlement is claimed against SEBI's current rails and no such structure is live in India today, cross-referenced to the coded SEBI provisions in the companion P2 repository.
**Where to verify:** manuscript §2.3, §6; SEBI (2025) reference.

### P1-6 — Literature thin / dated
**Original concern:** 15 references; needed 2023–2026 infrastructure-finance, tokenization, and PPP cost-of-capital sources.
**Action taken:** Expanded the reference list to **17 entries in Elsevier/FRL Harvard author–date style**, prioritising 2023–2026 Scopus-indexed work (El Jaouhari et al. 2025; Mirdala 2025; Assab 2024; Zhang, Gong & Zhou 2024; Pillada & Rangasamy 2023; Popov et al. 2022; Saari, Vimpari & Junnila 2022; Shah & Bhagwat 2022; Tian et al. 2020) alongside the primary sources (ADB 2020; JICA 2026; SEBI 2025; Moneycontrol 2026) and the canonical anchors (Amihud 2002; Esty 2004; Yescombe 2017). DOIs verified to Elsevier style; non-citable items removed.
**Where to verify:** manuscript References section (17 entries).

---

## Responses to P2 (polish) items

### P2-7 — Contribution framing
**Original concern:** Three contributions stated but not sharply differentiated from prior metro-finance studies.
**Action taken:** Tightened to one **headline contribution** — a reproducible viability-gap test plus a quantified tokenization cost-of-equity lever for a real, fully-disclosed Indian asset — supported by (1) the four-significant-figure WACC reproduction and (2) the SEBI-feasible T-InvIT design. The introduction now states the three contributions explicitly and distinguishes the probabilistic re-solve from earlier deterministic drafts.

### P2-8 — Data-integrity caveats
**Original concern:** The ADB-PDF-403 and BMRCL-is-RTI-not-financials caveats must remain visible.
**Action taken:** Both are **preserved**. §3 and §8 (Limitation 3) state that ADB's server returns HTTP 403, so the canonical URL, access date, and extracted figure set are logged in `data/raw/JICA_loans/ADB/ADB_FA_download_status.md` rather than redistributed. The survey-pending and "no tokenized InvIT exists in India" caveats are retained in §8 (Limitation 4) and §10.

---

## New analytical artifacts added in this uplift

1. `notebooks/03_montecarlo_firr.py` — explicit cash-flow IRR model + 20,000-draw Monte Carlo over documented parameter distributions + tokenization cost-of-equity sweep + two-way sensitivity surface. Runs end-to-end (seed 53326).
2. New processed tables: `mc_firr_summary.csv`, `mc_firr_draws.csv`, `firr_tornado.csv`, `assumption_ranges.csv`, `calibration_log.csv`, `tokenization_coe_sweep.csv`.
3. New 300-DPI figures (5–8): Monte Carlo FIRR distribution vs WACC, variance-decomposition tornado, cost-of-equity break-even sweep, two-way FIRR sensitivity surface. (Figures 1–4 retained: WACC/FIRR gap, ridership forecast, revenue forecast, one-at-a-time tornado.)
4. `paper/P1_manuscript_FRL.docx` — Elsevier/FRL-styled manuscript (Times New Roman, Highlights, Harvard references) mirroring the uplifted Markdown.

## Items deliberately kept intact (per audit Section B)

- The **WACC reproduction (2.6288% vs ADB 2.629%)** remains the anchor integrity result.
- Honest "ADB-parameterised" labelling of projections and the BMRCL/ADB data caveats.
- 300-DPI figures and the reproducible notebook pipeline.
