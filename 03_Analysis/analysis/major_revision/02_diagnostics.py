"""
Major Revision 統計解析 02: 主要推論モデル（Model 4）の回帰診断

残差・レバレッジ・Cook距離・DFBETAs（曝露変数）を都道府県別に出力する。
通常OLS（非ロバスト）に基づく古典的influence統計量を用いる（HC3はSEのみを変える推論上の選択であり、
影響診断の標準的な定義はOLSの hat matrix に基づくため）。

出力:
  - results/influence.csv （都道府県別 residual, leverage, cooks_d, dfbeta_exposure）
"""
import pandas as pd

from _common import CONFIG, OUTCOME, RESULTS_DIR, fit_ols, load_dataset


def main():
    df = load_dataset()
    y = df[OUTCOME]

    spec = CONFIG["models"][CONFIG["models"]["primary_inference_model"]]
    exposure = spec["exposure"]
    cols = [exposure] + spec["adjust"]
    X = df[cols]

    model = fit_ols(y, X, robust=None)
    influence = model.get_influence()

    dfbetas = influence.dfbetas
    exposure_idx = list(model.params.index).index(exposure)

    out = pd.DataFrame(
        {
            "pref_code": df["pref_code"],
            "residual": model.resid.values,
            "leverage": influence.hat_matrix_diag,
            "cooks_d": influence.cooks_distance[0],
            "dfbeta_exposure": dfbetas[:, exposure_idx],
        }
    ).sort_values("cooks_d", ascending=False)

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    out.to_csv(RESULTS_DIR / "influence.csv", index=False, encoding="utf-8-sig")

    n = len(df)
    k = len(cols) + 1
    cooks_threshold = 4 / n
    high_influence = out[out["cooks_d"] > cooks_threshold]

    print(f"[OK] influence.csv written ({n} prefectures, model={CONFIG['models']['primary_inference_model']})")
    print(f"Cook's D threshold (4/N): {cooks_threshold:.4f}")
    print(f"Prefectures exceeding threshold: {len(high_influence)}")
    print(high_influence[["pref_code", "cooks_d", "leverage"]].to_string(index=False))


if __name__ == "__main__":
    main()
