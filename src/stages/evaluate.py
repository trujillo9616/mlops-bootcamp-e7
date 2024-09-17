from typing import Text
import argparse
import pandas as pd
import joblib
import yaml
import mlflow
from sklearn.metrics import (
    silhouette_score,
    calinski_harabasz_score,
    davies_bouldin_score,
)

from src.utils.logs import get_logger
from src.utils.mlflow_run_decorator import mlflow_run


@mlflow_run
def evaluate(config_path: Text) -> None:
    with open(config_path) as conf_file:
        config = yaml.safe_load(conf_file)
    logger = get_logger("EVALUATE", log_level=config["base"]["log_level"])

    logger.info("Evaluating model... 🚀")

    # Load data
    logger.info("Load scaled data... 💽")
    df_scaled = pd.read_csv(
        config["scaling"]["norm_path"], encoding=config["data_load"]["encoding"]
    )
    df = pd.read_csv(
        config["featurize"]["features_path"], encoding=config["data_load"]["encoding"]
    )

    # Load model
    logger.info("Load model... 💾")
    model_path = config["train"]["model_path"]
    model = joblib.load(model_path)

    # Predict
    model.fit_predict(df_scaled)
    labels = model.labels_

    # Evaluate
    logger.info("Evaluate model... 📊")
    silhouette = silhouette_score(df_scaled, labels)
    calinski = calinski_harabasz_score(df_scaled, labels)
    davies = davies_bouldin_score(df_scaled, labels)
    logger.info(f"Silhouette Score: {silhouette}")
    mlflow.log_metric("silhouette", silhouette)
    logger.info(f"Calinski Harabasz Score: {calinski}")
    mlflow.log_metric("calinski", calinski)
    logger.info(f"Davies Bouldin Score: {davies}")
    mlflow.log_metric("davies", davies)

    # Save labels
    logger.info("Save labels... 💾")
    df["clusterid"] = labels
    df["labels"] = df["clusterid"].map(
        {
            0: "Lost/Needs Attention Customers",
            1: "Current Customers",
            2: "Top/Best Customers",
        }
    )
    df_final = df[["customerid", "clusterid", "labels"]]
    final_path = config["evaluate"]["final_path"]
    df_final.to_csv(final_path, index=False)
    mlflow.log_artifact("data/final", artifact_path="final_online_retail_.csv")

    logger.info("Model evaluated successfully! 🎉")


if __name__ == "__main__":
    mlflow.set_tracking_uri("https://dagshub.com/trujillo9616/mlops-bootcamp-e7.mlflow")
    mlflow.set_experiment("OnlineRetail")
    args_parser = argparse.ArgumentParser()
    args_parser.add_argument("--config", dest="config", required=True)
    args = args_parser.parse_args()

    evaluate(config_path=args.config)
