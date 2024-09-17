import argparse
import pandas as pd
from typing import Text
import yaml
import joblib
import matplotlib.pyplot as plt
import mlflow

from src.utils.logs import get_logger
from src.train.train import train
from src.utils.mlflow_run_decorator import mlflow_run


@mlflow_run
def train_model(config_path: Text) -> None:
    """Train model.
    Args:
        config_path {Text}: path to config
    """

    with open(config_path) as conf_file:
        config = yaml.safe_load(conf_file)

    logger = get_logger("TRAIN", log_level=config["base"]["log_level"])

    logger.info("Getting estimator name... 🤖")
    estimator_name = config["train"]["estimator_name"]
    logger.info(f"Estimator name: {estimator_name}")
    mlflow.log_param("estimator_name", estimator_name)

    logger.info("Load scaled data... 💽")
    df_scaled = pd.read_csv(
        config["scaling"]["norm_path"], encoding=config["data_load"]["encoding"]
    )
    mlflow.log_artifacts("data/processed", artifact_path="norm_online_retail.csv")

    logger.info("Getting train parameters... 🚂")
    n_clusters, max_iter, random_state = (
        config["train"]["n_clusters"],
        config["train"]["max_iter"],
        config["base"]["random_state"],
    )
    mlflow.log_param("n_clusters", n_clusters)
    mlflow.log_param("max_iter", max_iter)
    mlflow.log_param("random_state", random_state)

    logger.info("Train model... 🚂")
    model = train(
        df=df_scaled,
        estimator_name=estimator_name,
        n_clusters=n_clusters,
        max_iter=max_iter,
        random_state=random_state,
    )

    logger.info("Save model... 💾")
    model_path = config["train"]["model_path"]
    joblib.dump(model, model_path)
    mlflow.log_artifacts("models", artifact_path="model.pkl")
    mlflow.sklearn.log_model(
        sk_model=model,
        artifact_path="models/model.pkl",
        registered_model_name="online_retail_model",
    )

    # # get centroids
    # centroids = kmeans.cluster_centers_
    # cen_x = [i[0] for i in centroids]
    # cen_y = [i[1] for i in centroids]

    # ## add to dataframe
    # data_rfm['cen_x'] = data_rfm.cluster.map({0: cen_x[0], 1: cen_x[1], 2: cen_x[2]})
    # data_rfm['cen_y'] = data_rfm.cluster.map({0: cen_y[0], 1: cen_y[1], 2: cen_y[2]})

    # # define and map colors
    # colors = ['#DF2020', '#81DF20', '#2095DF', '#8e7cc3']
    # data_rfm['c'] = data_rfm.cluster.map({0: colors[0], 1: colors[1], 2: colors[2], 3: colors[3]})

    # df_cluster = pd.merge(data, data_rfm, on='CustomerID', how='right')
    # rfm_path = config['train']['cluster_path']
    # df_cluster.to_csv(rfm_path, index=False)

    # # Crear el gráfico de pastel
    # logger.info('save pie population data graph')

    # grouped = df_cluster.groupby('cluster')
    # group_counts = grouped.size()
    # plt.pie(group_counts, labels=group_counts.index, autopct='%1.1f%%')
    # plt.title("Poblacion por cluster", fontsize=18)
    # plt.savefig(config['train']['pie_poblacion_graph_path'])

    # logger.info('save pie total sales data graph')

    # grouped = df_cluster.groupby('cluster')['Total_sales'].sum()
    # plt.title("Total de compras por cluster", fontsize=18)
    # plt.pie(grouped, labels=grouped.index, autopct='%1.1f%%')
    # plt.savefig(config['train']['pie_compras_graph_path'])

    # logger.info('save 3d graph')
    # generate3d(config, data_rfm)


def generate3d(config, data_rfm):
    fig = plt.figure(figsize=(12, 12))
    ax = fig.add_subplot(111, projection="3d")
    ax.scatter(
        data_rfm.log_R, data_rfm.log_M, data_rfm.log_F, c=data_rfm.c, cmap="viridis"
    )
    ax.set_xlabel("log_R")
    ax.set_ylabel("log_M")
    ax.set_zlabel("log_F")
    ax.set_xlabel("Recency", fontsize=12)
    ax.set_ylabel("Monetary", fontsize=12)
    ax.set_zlabel("Frequency", fontsize=12)
    plt.savefig(config["train"]["graph_path"])


if __name__ == "__main__":
    args_parser = argparse.ArgumentParser()
    args_parser.add_argument("--config", dest="config", required=True)
    args = args_parser.parse_args()

    train_model(config_path=args.config)
