# Practitioner Survey Design — Adoption Arm

**Thesis:** REITs & InvITs in India — Diversification Opportunities for Investors, with Focus on Bengaluru
**Author:** Sandeep S (PhD Research Scholar, University of Mysore; MScFE, WorldQuant University)
**Platform:** Zoho Survey | **Design date:** 2026-06-03 | **Status:** DRAFT instrument — pilot and obtain IRB/ethics clearance before fielding.

> **Integrity note.** This file specifies the *design* of the adoption-arm survey. No survey responses exist yet. The response dataset is intentionally empty (`survey_responses_TEMPLATE.csv` carries headers only, no rows), and the analysis notebook (`05_survey_adoption_PENDING.py`) aborts unless a real, populated response file is supplied. No responses are fabricated, simulated, or imputed at the design stage.

This survey is the **adoption arm** shared by both papers:

- **P2 (BInvIT — liquidity around SEBI's 2025 InvIT reform):** the survey supplies the *demand-side* counterpart to the secondary-market liquidity evidence — whether the access-widening reform translates into stated adoption intention, and which investor segments would take up a future tokenized access layer.
- **P1 (T-InvIT — Bengaluru metro / Peripheral Ring Road viability gap):** the survey measures retail and HNI appetite for a Bengaluru-focused tokenized InvIT, informing the access-and-cost-of-equity assumptions in the financing design.

In both manuscripts the survey arm is reported as **pending / not yet fielded**; survey-dependent analyses are marked accordingly in each paper's Data Availability statement.

---

## 1. Constructs and hypotheses

The instrument operationalises six latent/manifest constructs across 23 scored items. The construct → hypothesis → item map is the canonical `Construct_Measurement_Matrix.csv` (23 rows).

| Construct | Label | Items | Hypothesis | Scale | Role |
|---|---|---|---|---|---|
| AWARE | Awareness | AWARE1–4 (Likert), AWARE5 (binary 0/1) | H6 | 5-pt Likert + 1 binary | reflective (1–4), manifest (5) |
| DIVERS | Perceived Diversification | DIVERS1–4 | H1 | 5-pt Likert | reflective |
| RISKP | Perceived Risk / Rate Sensitivity | RISKP1–4 | H5 | 5-pt Likert | reflective |
| REGTRUST | Regulatory Trust | REGTRUST1–3 | H7 | 5-pt Likert | reflective |
| BLR | Bengaluru Focus | BLR1–3 | H4 | 5-pt Likert | reflective |
| ADOPT | Adoption Intention | ADOPT1–3 (Likert), ADOPT4 (categorical) | H6 (dependent) | 5-pt Likert + 1 categorical | reflective (1–3), manifest (4) |

**Scale coding.** 5-point Likert: Strongly Disagree = 1 … Strongly Agree = 5. No reverse-scored items in this draft (RISKP items are perception, not reverse-coded — re-check at pilot). AWARE5 is an open name field coded to a binary 0/1 recognition flag. ADOPT4 is a four-level categorical adoption-status item.

---

## 2. Questionnaire (final draft)

### Consent text (Section A, page 1)

> You are invited to participate in an academic survey on investor perceptions of REITs and InvITs in India, conducted as part of doctoral research at the University of Mysore. Participation is voluntary, anonymous, and takes about 6–8 minutes. You may exit at any time. No personally identifying information is required, and responses are used only in aggregate for academic analysis. By selecting "Yes" below you confirm that you are 18 years or older and consent to participate.

### Section A — Screening & Consent (page 1)

- **A1.** I confirm I am 18+ and consent to participate in this academic survey. *(Yes / No — "No" exits)*
- **A2.** Are you an investor, finance professional, or industry participant in Indian capital markets? *(Yes / No — "No" exits)*
- **A3.** Which best describes you? *(Retail investor / HNI / Institutional investor / Wealth advisor / REIT-InvIT industry professional / Academic-researcher / Other)*

### Section B — Respondent Profile (page 2)

- **B1.** Age band *(18–25 / 26–35 / 36–45 / 46–55 / 56–65 / 65+)*
- **B2.** City / region of residence *(Bengaluru / Other Karnataka / Other metro India / Non-metro India / Outside India)*
- **B3.** Investment experience *(< 1 yr / 1–3 yrs / 3–5 yrs / 5–10 yrs / 10+ yrs)*
- **B4.** Approximate investable corpus *(< ₹5L / ₹5L–25L / ₹25L–1Cr / ₹1Cr–5Cr / > ₹5Cr / Prefer not to say)*
- **B5.** Asset classes currently held *(multi-select: Equity / Mutual funds / Debt-bonds / Real estate-physical / REITs / InvITs / Gold / Crypto / Other)*

### Section C — Awareness (AWARE, H6) — 5-pt Likert

- **AWARE1.** I am aware that REITs are listed and traded on Indian stock exchanges.
- **AWARE2.** I am aware that InvITs are listed and traded on Indian stock exchanges.
- **AWARE3.** I understand how REITs/InvITs generate income (rent/toll/transmission charges) and distribute it.
- **AWARE4.** I am aware of the Small & Medium REIT (SM REIT) framework introduced by SEBI.
- **AWARE5.** I can name at least one listed Indian REIT or InvIT. *(Open text — coded 0/1)*

### Section D — Perceived Diversification Benefit (DIVERS, H1) — 5-pt Likert

- **DIVERS1.** Adding REITs/InvITs to a portfolio reduces overall risk.
- **DIVERS2.** REIT/InvIT returns move differently from equities (low correlation).
- **DIVERS3.** REITs/InvITs provide stable, predictable income relative to stocks.
- **DIVERS4.** REITs/InvITs are a useful inflation/real-asset hedge.

### Section E — Perceived Risk & Rate Sensitivity (RISKP, H5) — 5-pt Likert

- **RISKP1.** REIT/InvIT prices are sensitive to interest-rate changes.
- **RISKP2.** I am concerned about liquidity when buying/selling REITs/InvITs.
- **RISKP3.** I find REIT/InvIT distributions' taxation complex.
- **RISKP4.** I worry about valuation transparency of underlying assets.

### Attention check (between E and F)

- **ATTN1.** Please select "Agree" for this item. *(Responses other than "Agree" flag the record for review/exclusion.)*

### Section F — Regulatory Trust (REGTRUST, H7) — 5-pt Likert

- **REGTRUST1.** SEBI regulation of REITs/InvITs adequately protects investors.
- **REGTRUST2.** Disclosure/reporting by REITs/InvITs is sufficient for informed decisions.
- **REGTRUST3.** The regulatory framework increases my confidence to invest.

### Section G — Bengaluru Focus (BLR, H4) — 5-pt Likert

- **BLR1.** Bengaluru's office-property market is attractive for REIT investment.
- **BLR2.** I would prefer REITs with significant Bengaluru/South-India office exposure.
- **BLR3.** Growth of Bengaluru's GCC/IT-office demand makes office REITs more attractive.

### Section H — Adoption Intention (ADOPT, H6 dependent) — 5-pt Likert + categorical

- **ADOPT1.** I intend to invest (or invest more) in REITs within the next 12 months.
- **ADOPT2.** I intend to invest (or invest more) in InvITs within the next 12 months.
- **ADOPT3.** I would recommend REITs/InvITs to peers.
- **ADOPT4.** Have you ever invested in a REIT or InvIT? *(Yes-currently / Yes-previously / No-but considering / No-not considering)*

### Section I — Open Feedback (optional)

- **I1.** What is the single biggest barrier to your investing in REITs/InvITs? *(Open text)*
- **I2.** Any additional comments. *(Open text)*

### Survey logic & quality controls

- **Branching:** A1 = "No" or A2 = "No" → thank-you exit (record discarded).
- **Attention check:** ATTN1 between Sections E and F; non-"Agree" responses flagged.
- **Mandatory:** all Likert items mandatory; open-text optional.
- **Randomisation:** randomise item order *within* each construct block; keep blocks intact.
- **Estimated completion:** 6–8 minutes (~30 scored items).

---

## 3. Sampling plan

**Target sample:** **n ≥ 250 valid (completed, attention-check-passing) responses.** This is the SEM minimum (5–10× the largest construct's indicator count; the largest reflective block has 4 indicators, so 250 comfortably exceeds the 5–10× floor and supports CFA/SEM if N > 200).

**Sampling frame.** The frame is the curated outreach list `Survey_Target_List.csv` (**262 prospects**), assembled from REIT/InvIT issuers, sponsors, advisors, institutional investors, and academics (e.g., Embassy REIT, Brookfield, Mindspace, Nexus, IndiGrid, IRB InvIT, PGInvIT, CBRE, Indian REITs Association). Of these, **125 carry a public LinkedIn URL** and **75 carry a public email**, which define the directly contactable seed. The frame is supplemented by snowball referral and open distribution through professional networks to reach the retail tier, which the curated list under-represents.

**Stratification.** The frame's `Survey_Priority` field defines three strata, mapped to outreach tiers:

| Tier | `Survey_Priority` | Frame count | Description | Sampling approach |
|---|---|---|---|---|
| Tier-1 | High | 28 | Senior issuer/sponsor IR, named experts | Census — contact all; personalised outreach |
| Tier-2 | Medium | 214 | Advisors, institutional, mid-level professionals, academics | Stratified outreach across the full list |
| Tier-3 | Low | 20 | Peripheral / lower-relevance contacts | Opportunistic; included if responsive |

**Geography.** The frame is **India-heavy (214 India, 48 global/other)**, consistent with the Bengaluru focus (construct BLR, H4). India residents are the primary analytic population; outside-India respondents (B2 = "Outside India") are retained for descriptive comparison but excluded from Bengaluru-specific sub-analyses.

**Response-rate planning.** A curated-list survey of this kind typically yields 8–20% from the directly contactable seed. With 125 contactable prospects plus snowball and open distribution, reaching n ≥ 250 requires the seed *plus* network amplification — budget a 4–6 week field window with one reminder wave. If the seed alone under-delivers, escalate open distribution (LinkedIn posts, REIT-investor communities) to fill the retail tier.

**Pilot.** Field a pilot of **n ≈ 30** before the full launch. Compute Cronbach's α per reflective construct (AWARE, DIVERS, RISKP, REGTRUST, BLR, ADOPT); **target α ≥ 0.70**. Re-examine RISKP for any reverse-coding need and refine wording before the full field.

---

## 4. Statistical test mapping

This is the exact specification of which items feed which test. Two analytic families are pre-registered here: **(a) chi-square tests of association** on categorical/binary items, and **(b) logistic regression** of a binary adoption outcome on construct means and covariates. This mirrors the P2 pipeline (chi-square on liquidity tier × stale-day; logistic regression / RF / XGBoost on the modelling arm) so the survey arm is methodologically consistent with the secondary-data arm.

### 4.1 Derived variables

- **`adopt_binary`** (logistic-regression dependent variable): coded **1** if the respondent is a current/past adopter or shows strong stated intention, **0** otherwise. Operationalisation: `adopt_binary = 1` if `ADOPT4 ∈ {Yes-currently, Yes-previously}` **OR** `mean(ADOPT1, ADOPT2) ≥ 4`; else `0`. (The exact rule is fixed here and applied identically once real data arrive; it is *not* tuned to results.)
- **`adopt_status`** (chi-square): the raw four-level `ADOPT4` categorical.
- **Construct means:** `AWARE_mean` (AWARE1–4), `DIVERS_mean` (DIVERS1–4), `RISKP_mean` (RISKP1–4), `REGTRUST_mean` (REGTRUST1–3), `BLR_mean` (BLR1–3). Computed only after the pilot confirms α ≥ 0.70; otherwise items are inspected individually.
- **`aware5_flag`:** binary 0/1 recognition flag from AWARE5 open text.

### 4.2 Chi-square tests of association (categorical / binary items)

| # | Test | Variables | Hypothesis link |
|---|---|---|---|
| χ²-1 | Respondent type × adoption status | `A3` × `ADOPT4` | H6 — does investor segment associate with adoption? |
| χ²-2 | Name-recognition × adoption | `aware5_flag` (0/1) × `adopt_binary` | H6 — does concrete awareness associate with adoption? |
| χ²-3 | Experience tier × adoption | `B3` (banded) × `adopt_binary` | H6 — experience as adoption correlate |
| χ²-4 | Region × Bengaluru preference | `B2` × `BLR2` (banded agree/neutral/disagree) | H4 — geography × Bengaluru appetite |
| χ²-5 | Corpus tier × adoption | `B4` × `adopt_binary` | H6 — wealth tier × adoption |

For each: report χ², df, p-value, and Cramér's V effect size. Use Fisher's exact test where any expected cell count < 5. (Mirrors P2's chi-square on liquidity tier × stale-day incidence.)

### 4.3 Logistic regression (binary adoption outcome)

**Model:** `adopt_binary ~ AWARE_mean + DIVERS_mean + RISKP_mean + REGTRUST_mean + BLR_mean + C(A3) + C(B3) + C(B4)`

- **Dependent variable:** `adopt_binary` (derived above).
- **Construct predictors:** the five construct means (DIVERS for H1, BLR for H4, RISKP for H5, AWARE for H6, REGTRUST for H7).
- **Covariates:** respondent type (`A3`), experience (`B3`), corpus (`B4`).
- **Reporting:** coefficients, odds ratios with 95% CI, pseudo-R², ROC-AUC, and a confusion matrix at the 0.5 threshold — matching the P2 classifier reporting (LogReg / RF / XGBoost with ROC-AUC).
- **Diagnostics:** multicollinearity (VIF on construct means), Hosmer–Lemeshow goodness-of-fit. If multicollinearity is high among construct means, report a reduced model and note it.
- **Optional robustness:** Random Forest / gradient-boosting classifier on the same feature set for comparison, reported only as a robustness check (not the primary inferential model). Mirrors the P2 ML arm; survey-data only, no fabrication.

### 4.4 Supporting reliability/descriptive steps (run first)

1. Cronbach's α per reflective construct (pilot and full sample); target ≥ 0.70.
2. Item and construct-mean descriptives by tier/region.
3. Optional CFA/SEM if N > 200 and α thresholds are met (per `Hypothesis_Data_Mapping.md`).

### 4.5 What is explicitly NOT in this arm

H2, H3, and H7's forecast components are answered by the **secondary-data** pipelines (correlation, regression/VAR, ARIMA/GARCH/Monte Carlo) on price and macro series — not by the survey. The survey contributes the *primary/perception* evidence for the triangulation matrix in `Hypothesis_Data_Mapping.md`.

---

## 5. Files in this survey package

| File | Contents | Fabrication status |
|---|---|---|
| `SURVEY_DESIGN.md` | This document | n/a |
| `survey_questions_import.csv` | Ready-to-import question list (Zoho-importable): one row per item with section, code, text, type, options | n/a |
| `survey_responses_TEMPLATE.csv` | Empty response template — **headers only, zero data rows** | **EMPTY / PENDING — no responses** |
| `05_survey_adoption_PENDING.py` | Analysis notebook: aborts unless a real populated response file is supplied; runs reliability → chi-square → logistic regression | reads real data only; never simulates |

---

## 6. Provenance

- Instrument: PhD Vault `09_Survey_Zoho/Survey_Instrument.md`
- Construct map: PhD Vault `09_Survey_Zoho/Construct_Measurement_Matrix.csv`
- Hypothesis/test map: PhD Vault `09_Survey_Zoho/Hypothesis_Data_Mapping.md`
- Sampling frame: PhD Vault `09_Survey_Zoho/Survey_Target_List.csv` (262 prospects; High 28 / Medium 214 / Low 20)

*Affiliation note: the working `Hypothesis_Data_Mapping.md` lists Alliance University; the manuscripts and this design use the current affiliation, University of Mysore.*
