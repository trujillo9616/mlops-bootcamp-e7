import argparse
import pandas as pd
import numpy as np
from typing import Text
import yaml
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, calinski_harabasz_score, davies_bouldin_score

from src.utils.logs import get_logger

def plot_scores(a,b, db, ca, sc, config):
    fig, ax = plt.subplots(nrows= 1, ncols=3, figsize=(15,4))
    ax[0].plot(range(a, b), db, "bo-", label= 'Davies_Bouldin_Score')
    ax[1].plot(range(a, b), ca, "rx-", label = 'Calinski_Harabasz_Score')
    ax[2].plot(range(a, b), sc, "g.-", label = 'Silhouette_Score')
    ax[0].set_xlabel("$k$", fontsize=14)
    ax[1].set_xlabel("$k$", fontsize=14)
    ax[2].set_xlabel("$k$", fontsize=14)
    ax[0].set_ylabel('Davies Bouldin Score', fontsize=14)
    ax[1].set_ylabel('Calinski Harabasz Score', fontsize=14)
    ax[2].set_ylabel('Silhouette Score', fontsize=14)
    plt.savefig(config['elbow']['graph_path'])

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
    data_transformed = data_rfm[["log_R", "log_F", "log_M"]]

    Scores = {'Davies_Bouldin_Score': [],
              'Calinski_Harabasz_Score': [],
              'Silhouette_Score': []}

    for k in range(3, 7):
        kmeans = KMeans(n_clusters=k).fit(data_transformed)
        Scores['Davies_Bouldin_Score'].append(davies_bouldin_score(data_transformed,
                                                                   kmeans.labels_))
        Scores['Calinski_Harabasz_Score'].append(calinski_harabasz_score(data_transformed,
                                                                         kmeans.labels_))
        Scores['Silhouette_Score'].append(silhouette_score(data_transformed,
                                                           kmeans.labels_))

    logger.info('Save Elbow')
    plot_scores(3, 7, Scores['Davies_Bouldin_Score'], Scores['Calinski_Harabasz_Score'],
                Scores['Silhouette_Score'], config)

    logger.info('Save Data')
    norm_path = config['elbow']['norm_path']
    rfm_path = config['elbow']['rfm_path']
    data_transformed.to_csv(norm_path, index=False)
    data_rfm.to_csv(rfm_path, index=False)

if __name__ == '__main__':

    args_parser = argparse.ArgumentParser()
    args_parser.add_argument('--config', dest='config', required=True)
    args = args_parser.parse_args()

    elbow_model(config_path=args.config)