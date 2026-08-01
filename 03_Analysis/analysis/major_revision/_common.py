"""
Major Revision 統計解析: 共通ユーティリティ

Model 0-4・感度分析・非線形性・多重性のすべてのスクリプトから読み込む。
config.yaml のモデル仕様（変数名・調整変数リスト）をコードに直書きしない。
"""
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm
import yaml
from statsmodels.stats.outliers_influence import variance_inflation_factor

PROJECT_ROOT = Path(__file__).resolve().parents[3]
DATA_PATH = PROJECT_ROOT / "02_Data" / "interim" / "major_revision" / "prefecture_analysis.csv"
CONFIG_PATH = PROJECT_ROOT / "config" / "config.yaml"
RESULTS_DIR = PROJECT_ROOT / "03_Analysis" / "results" / "major_revision"

with open(CONFIG_PATH, encoding="utf-8") as f:
    CONFIG = yaml.safe_load(f)

OUTCOME = "large_volume_infusion_procedure_rate"
METRO_EXCLUDE = CONFIG["metropolitan_exclusion"]


def load_dataset() -> pd.DataFrame:
    df = pd.read_csv(DATA_PATH, dtype={"pref_code": str})
    assert len(df) == 47
    return df


def fit_ols(y: pd.Series, X: pd.DataFrame, robust: str = "HC3"):
    """定数項付きOLS。robust='HC3' でロバストSE、None で通常OLS SE。"""
    Xc = sm.add_constant(X, has_constant="add")
    model = sm.OLS(y, Xc).fit(cov_type=robust) if robust else sm.OLS(y, Xc).fit()
    return model


def standardized_coefs(y: pd.Series, X: pd.DataFrame, robust: str = "HC3") -> pd.DataFrame:
    """全変数をz-score標準化してから同じモデルを当てはめ、標準化係数・CI・pを返す。"""
    y_z = (y - y.mean()) / y.std(ddof=1)
    X_z = (X - X.mean()) / X.std(ddof=1)
    model = fit_ols(y_z, X_z, robust=robust)
    ci = model.conf_int()
    out = pd.DataFrame(
        {
            "std_coef": model.params,
            "std_ci_low": ci[0],
            "std_ci_high": ci[1],
            "std_p": model.pvalues,
        }
    )
    return out.drop(index="const")


def partial_r2(y: pd.Series, X_full: pd.DataFrame, focal_col: str) -> float:
    """focal_colを除いた縮小モデルとの残差平方和比較によるpartial R2（SEの取り方に依存しない）。"""
    full_model = fit_ols(y, X_full, robust=None)
    reduced_cols = [c for c in X_full.columns if c != focal_col]
    if reduced_cols:
        reduced_model = fit_ols(y, X_full[reduced_cols], robust=None)
    else:
        reduced_model = fit_ols(y, pd.DataFrame(index=X_full.index), robust=None)
    ssr_full = full_model.ssr
    ssr_reduced = reduced_model.ssr
    if ssr_reduced == 0:
        return np.nan
    return (ssr_reduced - ssr_full) / ssr_reduced


def compute_vif(X: pd.DataFrame) -> pd.DataFrame:
    """中心化した説明変数に定数項を加えてVIFを算出（切片由来の見かけ上のVIF膨張を避ける）。"""
    if X.shape[1] < 2:
        return pd.DataFrame({"variable": X.columns, "VIF": [np.nan] * X.shape[1]})
    Xc = X - X.mean()
    Xc = sm.add_constant(Xc, has_constant="add")
    vifs = []
    for i, col in enumerate(Xc.columns):
        if col == "const":
            continue
        vifs.append({"variable": col, "VIF": variance_inflation_factor(Xc.values, i)})
    return pd.DataFrame(vifs)


def aicc(model) -> float:
    n = int(model.nobs)
    k = int(model.df_model) + 1 + 1  # + intercept + sigma
    aic = model.aic
    if n - k - 1 <= 0:
        return np.nan
    return aic + (2 * k * (k + 1)) / (n - k - 1)


def model_fit_row(model, model_name: str) -> dict:
    return {
        "model": model_name,
        "n": int(model.nobs),
        "r_squared": model.rsquared,
        "adj_r_squared": model.rsquared_adj,
        "aic": model.aic,
        "aicc": aicc(model),
        "bic": model.bic,
    }


def unstandardized_rows(model, model_name: str) -> pd.DataFrame:
    ci = model.conf_int()
    df = pd.DataFrame(
        {
            "model": model_name,
            "variable": model.params.index,
            "coef": model.params.values,
            "se": model.bse.values,
            "ci_low": ci[0].values,
            "ci_high": ci[1].values,
            "p_value": model.pvalues.values,
        }
    )
    return df[df["variable"] != "const"]
