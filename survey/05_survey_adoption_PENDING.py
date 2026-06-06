#!/usr/bin/env python3
"""
05_survey_adoption_PENDING.py
Adoption-arm analysis for the REITs/InvITs practitioner survey.

STATUS: PENDING — NO RESPONSES HAVE BEEN COLLECTED.

This script will NOT run on an empty/template response file and NEVER fabricates,
simulates, or imputes responses. It aborts immediately unless a real, populated
response CSV (with at least MIN_VALID rows of genuine data) is supplied.

Once real responses are collected from Zoho Survey:
  1. Export responses to CSV using the column layout of `survey_responses_TEMPLATE.csv`.
  2. Save as `survey_responses.csv` in this folder (or pass a path as argv[1]).
  3. Run:  python3 05_survey_adoption_PENDING.py [path_to_responses.csv]

Pipeline (runs only on real data):
  reliability (Cronbach's alpha) -> chi-square tests -> logistic regression.
Mirrors the secondary-data arm (P2 chi-square + logistic/RF/XGBoost classifiers).
"""
import sys
import os

import numpy as np
import pandas as pd

# --- configuration ----------------------------------------------------------
DEFAULT_RESPONSES = "survey_responses.csv"      # the REAL file, once collected
TEMPLATE_FILE     = "survey_responses_TEMPLATE.csv"  # headers-only, never analysed
MIN_VALID         = 30   # pilot floor; full analysis expects n >= 250

LIKERT_MAP = {"Strongly Disagree": 1, "Disagree": 2, "Neutral": 3,
              "Agree": 4, "Strongly Agree": 5,
              "1": 1, "2": 2, "3": 3, "4": 4, "5": 5}

CONSTRUCTS = {
    "AWARE":    ["AWARE1", "AWARE2", "AWARE3", "AWARE4"],   # AWARE5 is binary, handled separately
    "DIVERS":   ["DIVERS1", "DIVERS2", "DIVERS3", "DIVERS4"],
    "RISKP":    ["RISKP1", "RISKP2", "RISKP3", "RISKP4"],
    "REGTRUST": ["REGTRUST1", "REGTRUST2", "REGTRUST3"],
    "BLR":      ["BLR1", "BLR2", "BLR3"],
    "ADOPT":    ["ADOPT1", "ADOPT2", "ADOPT3"],
}


def abort(msg: str) -> None:
    print("\n[ABORT] " + msg)
    print("[ABORT] No analysis performed. No data fabricated.\n")
    sys.exit(1)


def load_real_responses(path: str) -> pd.DataFrame:
    """Load responses, refusing to proceed on a missing/empty/template file."""
    if not os.path.exists(path):
        abort(f"Response file '{path}' not found. Responses are PENDING — "
              f"collect real data from Zoho Survey first.")

    # Refuse if the caller pointed us at the headers-only template.
    if os.path.abspath(path) == os.path.abspath(TEMPLATE_FILE):
        abort(f"'{path}' is the empty template (headers only). "
              f"Supply a populated response export instead.")

    df = pd.read_csv(path)
    if len(df) == 0:
        abort(f"'{path}' has 0 data rows. Responses are PENDING — nothing to analyse.")
    if len(df) < MIN_VALID:
        abort(f"'{path}' has only {len(df)} rows (< MIN_VALID={MIN_VALID}). "
              f"Collect at least the pilot n before running.")
    return df


def clean(df: pd.DataFrame) -> pd.DataFrame:
    """Apply screening/attention filters and Likert coding. Real data only."""
    n0 = len(df)
    if "consent_passed" in df.columns:
        df = df[df["consent_passed"].astype(str).str.lower().isin(["1", "true", "yes"])]
    if "A1" in df.columns:
        df = df[df["A1"].astype(str).str.lower() == "yes"]
    if "A2" in df.columns:
        df = df[df["A2"].astype(str).str.lower() == "yes"]
    if "ATTN1" in df.columns:
        df = df[df["ATTN1"].astype(str).str.strip().isin(["Agree", "4"])]
    print(f"Screening: {n0} -> {len(df)} valid records.")
    if len(df) < MIN_VALID:
        abort(f"After screening only {len(df)} valid records remain (< {MIN_VALID}).")

    likert_cols = [c for cols in CONSTRUCTS.values() for c in cols]
    for c in likert_cols:
        if c in df.columns:
            df[c] = df[c].map(lambda v: LIKERT_MAP.get(str(v).strip(), np.nan))
    return df


def cronbach_alpha(frame: pd.DataFrame) -> float:
    items = frame.dropna()
    k = items.shape[1]
    if k < 2 or len(items) < 2:
        return float("nan")
    item_var = items.var(axis=0, ddof=1).sum()
    total_var = items.sum(axis=1).var(ddof=1)
    return (k / (k - 1)) * (1 - item_var / total_var)


def build_features(df: pd.DataFrame) -> pd.DataFrame:
    for name, items in CONSTRUCTS.items():
        present = [c for c in items if c in df.columns]
        df[f"{name}_mean"] = df[present].mean(axis=1)
    # binary recognition flag from AWARE5 open text
    if "AWARE5" in df.columns:
        df["aware5_flag"] = df["AWARE5"].apply(
            lambda v: 0 if (pd.isna(v) or str(v).strip() == "") else 1)
    # derived binary adoption outcome (rule fixed at design time, not tuned)
    cur_prev = df.get("ADOPT4", pd.Series([""] * len(df))).astype(str)
    intent = df[["ADOPT1", "ADOPT2"]].mean(axis=1) if {"ADOPT1", "ADOPT2"} <= set(df.columns) else 0
    df["adopt_binary"] = ((cur_prev.isin(["Yes-currently", "Yes-previously"])) | (intent >= 4)).astype(int)
    return df


def run_reliability(df: pd.DataFrame) -> None:
    print("\n=== Cronbach's alpha (target >= 0.70) ===")
    for name, items in CONSTRUCTS.items():
        present = [c for c in items if c in df.columns]
        a = cronbach_alpha(df[present])
        flag = "OK" if a >= 0.70 else "LOW"
        print(f"  {name:9s} (k={len(present)}): alpha = {a:.3f}  [{flag}]")


def run_chisquare(df: pd.DataFrame) -> None:
    from scipy.stats import chi2_contingency, fisher_exact
    print("\n=== Chi-square tests of association ===")
    tests = [
        ("chi2-1 A3 x ADOPT4",        "A3",          "ADOPT4"),
        ("chi2-2 aware5 x adopt_bin",  "aware5_flag", "adopt_binary"),
        ("chi2-3 B3 x adopt_bin",      "B3",          "adopt_binary"),
        ("chi2-4 B2 x BLR2",           "B2",          "BLR2"),
        ("chi2-5 B4 x adopt_bin",      "B4",          "adopt_binary"),
    ]
    for label, a, b in tests:
        if a not in df.columns or b not in df.columns:
            print(f"  {label}: SKIP (missing column)")
            continue
        ct = pd.crosstab(df[a], df[b])
        if ct.size == 0 or ct.shape[0] < 2 or ct.shape[1] < 2:
            print(f"  {label}: SKIP (degenerate table)")
            continue
        chi2, p, dof, exp = chi2_contingency(ct)
        n = ct.values.sum()
        cramers_v = np.sqrt(chi2 / (n * (min(ct.shape) - 1))) if n else float("nan")
        note = ""
        if (exp < 5).any() and ct.shape == (2, 2):
            _, p = fisher_exact(ct.values)
            note = " (Fisher exact)"
        print(f"  {label}: chi2={chi2:.3f} df={dof} p={p:.4f} V={cramers_v:.3f}{note}")


def run_logit(df: pd.DataFrame) -> None:
    import statsmodels.formula.api as smf
    print("\n=== Logistic regression: adopt_binary ~ constructs + covariates ===")
    formula = ("adopt_binary ~ AWARE_mean + DIVERS_mean + RISKP_mean + "
               "REGTRUST_mean + BLR_mean + C(A3) + C(B3) + C(B4)")
    model = smf.logit(formula, data=df.dropna(subset=[
        "adopt_binary", "AWARE_mean", "DIVERS_mean", "RISKP_mean",
        "REGTRUST_mean", "BLR_mean"])).fit(disp=False)
    print(model.summary())
    params = model.params
    conf = model.conf_int()
    print("\nOdds ratios (95% CI):")
    for term in params.index:
        print(f"  {term:24s} OR={np.exp(params[term]):.3f} "
              f"[{np.exp(conf.loc[term, 0]):.3f}, {np.exp(conf.loc[term, 1]):.3f}]")


def main() -> None:
    path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_RESPONSES
    print(f"Adoption-arm analysis | response file: {path}")
    df = load_real_responses(path)   # aborts on missing/empty/template/too-few
    df = clean(df)
    df = build_features(df)
    print(f"\nAnalysing {len(df)} valid responses.")
    run_reliability(df)
    run_chisquare(df)
    run_logit(df)
    print("\nDone. All results derive solely from collected responses.")


if __name__ == "__main__":
    main()
