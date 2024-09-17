import argparse
import pandas as pd
import numpy as np
from typing import Text
from sklearn.preprocessing import PowerTransformer, StandardScaler
import yaml
import mlflow

from src.utils.logs import get_logger
from src.utils.mlflow_run_decorator import mlflow_run


@mlflow_run
def scale(config_path: Text) -> None:
    """Scale features.
    Args:
        config_path {Text}: path to config
    """

    with open(config_path) as conf_file:
        config = yaml.safe_load(conf_file)

    logger = get_logger("DATA_SCALING", log_level=config["base"]["log_level"])

    logger.info("Load featurized data... 💽")
    df_rfm = pd.read_csv(
        config["featurize"]["features_path"], encoding=config["data_load"]["encoding"]
    )

    SKEW_THRESHOLD = config["scaling"]["skew_threshold"]
    mlflow.log_param("skew_threshold", SKEW_THRESHOLD)

    skew_vals = df_rfm[["recency", "frequency", "monetary"]].skew()
    skew_cols = skew_vals[abs(skew_vals) > SKEW_THRESHOLD]

    logger.info("Apply Log Transformation to Skewed Cols... 📐")
    rfm_log = df_rfm[skew_cols.index].copy()
    for col in skew_cols.index.values:
        rfm_log[col] = rfm_log[col].apply(np.log1p)

    logger.info("Apply Power Transformation... 🔌")
    rfm_before_transform = df_rfm[skew_cols.index].copy()
    pt = PowerTransformer(method="yeo-johnson")
    trans = pt.fit_transform(rfm_before_transform)
    rfm_trans = pd.DataFrame(trans, columns=skew_cols.index)

    logger.info("Apply Standard Scaler... 📏")
    scaler = StandardScaler()
    scaler.fit(rfm_trans)

    rfm_scaled = scaler.transform(rfm_trans)
    rfm_scaled = pd.DataFrame(rfm_scaled, columns=skew_cols.index)

    logger.info("Save scaled features... 💾")
    norm_path = config["scaling"]["norm_path"]
    rfm_scaled.to_csv(norm_path, index=False)


if __name__ == "__main__":
    args_parser = argparse.ArgumentParser()
    args_parser.add_argument("--config", dest="config", required=True)
    args = args_parser.parse_args()

    scale(config_path=args.config)
