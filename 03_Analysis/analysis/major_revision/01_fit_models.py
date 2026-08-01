"""
Major Revision 統計解析 01: Model 0-4 の当てはめ

config.yaml の models: セクションに従い、Model 0（旧曝露単独＝旧解析再現）から
Model 4（新曝露＋高齢化率＋一般病床数＋WBGT28日数）まで階層的に当てはめる。
主要推論はHC3ロバストSE、通常OLS SEは監査用に併記する（config.yaml audit_se）。

出力:
  - results/model_results.csv （係数レベル、非標準化・標準化・HC3/classical を tidy 形式で）
  - results/model_fit.csv （N, R2, adjR2, AIC, AICc, BIC）
  - results/vif.csv
"""
import pandas as pd

from _common import (
    CONFIG,
    OUTCOME,
    RESULTS_DIR,
    compute_vif,
    fit_ols,
    load_dataset,
    model_fit_row,
    partial_r2,
    standardized_coefs,
    unstandardized_rows,
)


def main():
    df = load_dataset()
    y = df[OUTCOME]

    all_coef_rows = []
    all_fit_rows = []
    all_vif_rows = []

    for model_name, spec in CONFIG["models"].items():
        if not isinstance(spec, dict) or "exposure" not in spec:
            continue  # primary_inference_model, inference_se, audit_se はスキップ

        exposure = spec["exposure"]
        adjust = spec["adjust"]
        cols = [exposure] + adjust
        X = df[cols]

        # --- HC3 (主要推論) ---
        model_hc3 = fit_ols(y, X, robust="HC3")
        rows_hc3 = unstandardized_rows(model_hc3, model_name)
        rows_hc3["se_type"] = "HC3"
        rows_hc3["coef_type"] = "unstandardized"

        # --- classical OLS SE (監査用) ---
        model_classical = fit_ols(y, X, robust=None)
        rows_classical = unstandardized_rows(model_classical, model_name)
        rows_classical["se_type"] = "classical_ols"
        rows_classical["coef_type"] = "unstandardized"

        # --- 標準化係数 (HC3) ---
        std_rows = standardized_coefs(y, X, robust="HC3").reset_index().rename(columns={"index": "variable"})
        std_rows["model"] = model_name
        std_rows["se_type"] = "HC3"
        std_rows["coef_type"] = "standardized"
        std_rows = std_rows.rename(
            columns={"std_coef": "coef", "std_ci_low": "ci_low", "std_ci_high": "ci_high", "std_p": "p_value"}
        )
        std_rows["se"] = float("nan")

        all_coef_rows.extend([rows_hc3, rows_classical, std_rows[rows_hc3.columns]])

        # --- exposure の partial R2 ---
        p_r2 = partial_r2(y, X, exposure)

        fit_row = model_fit_row(model_classical, model_name)
        fit_row["exposure"] = exposure
        fit_row["exposure_partial_r2"] = p_r2
        all_fit_rows.append(fit_row)

        # --- VIF (共変量が2つ以上のモデルのみ意味を持つ) ---
        vif_df = compute_vif(X)
        vif_df["model"] = model_name
        all_vif_rows.append(vif_df)

    coef_df = pd.concat(all_coef_rows, ignore_index=True)
    fit_df = pd.DataFrame(all_fit_rows)
    vif_df_all = pd.concat(all_vif_rows, ignore_index=True)

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    coef_df.to_csv(RESULTS_DIR / "model_results.csv", index=False, encoding="utf-8-sig")
    fit_df.to_csv(RESULTS_DIR / "model_fit.csv", index=False, encoding="utf-8-sig")
    vif_df_all.to_csv(RESULTS_DIR / "vif.csv", index=False, encoding="utf-8-sig")

    print("[OK] model_results.csv, model_fit.csv, vif.csv written to", RESULTS_DIR)
    print()
    print(fit_df[["model", "exposure", "n", "adj_r_squared", "exposure_partial_r2", "aicc"]].to_string(index=False))
    print()
    exposure_coefs = coef_df[
        (coef_df["coef_type"] == "unstandardized")
        & (coef_df["se_type"] == "HC3")
        & (coef_df["variable"].isin(["older_living_alone_pct", "original_elderly_solo_household_pct"]))
    ]
    print(exposure_coefs.to_string(index=False))


if __name__ == "__main__":
    main()
