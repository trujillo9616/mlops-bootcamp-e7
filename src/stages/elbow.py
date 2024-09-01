import argparse
import pandas as pd
import numpy as np
from typing import Text
import yaml
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns

from src.utils.logs import get_logger


def elbow_model(config_path: Text) -> None:
    """Elbow model.
    Args:
        config_path {Text}: path to config
    """

    with open(config_path) as conf_file:
        config = yaml.safe_load(conf_file)

    logger = get_logger('TRAIN', log_level=config['base']['log_level'])

    logger.info('Load featured data')
    data_rfm = pd.read_csv(config['featurize']['features_path'], encoding=config['data_load']['encoding'])

    data_rfm['Recency'] = pd.to_numeric(data_rfm['Recency'])
    data_rfm['Frequency'] = pd.to_numeric(data_rfm['Frequency'])
    data_rfm['Monetary'] = pd.to_numeric(data_rfm['Monetary'])

    data_rfm["log_R"] = np.log(data_rfm.Recency)
    data_rfm["log_F"] = np.log(data_rfm.Frequency)
    data_rfm["log_M"] = np.log(data_rfm.Monetary)

    ### Features Used in training K Means - Log Transformed Recency, Frequency and Monetary values
    data_norm = data_rfm[["log_R", "log_F", "log_M"]]

    sse = {}
    # Fit KMeans and calculate SSE for each k
    for k in range(1, 11):
        # Initialize KMeans with k clusters
        kmeans = KMeans(n_clusters=k, random_state=1)

        # Fit KMeans on the normalized dataset
        kmeans.fit(data_norm)

        # Assign sum of squared distances to k element of dictionary
        sse[k] = kmeans.inertia_

    # Plotting the elbow plot
    plt.figure(figsize=(10, 4))
    plt.title('The Elbow Method')
    plt.xlabel('k')
    plt.ylabel('Sum of squared errors')
    sns.pointplot(x=list(sse.keys()), y=list(sse.values()))
    plt.savefig(config['elbow']['graph_path'])

if __name__ == '__main__':

    args_parser = argparse.ArgumentParser()
    args_parser.add_argument('--config', dest='config', required=True)
    args = args_parser.parse_args()

    elbow_model(config_path=args.config)