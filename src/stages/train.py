import argparse
import pandas as pd
from typing import Text
import yaml
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

from src.utils.logs import get_logger


def train_model(config_path: Text) -> None:
    """Train model.
    Args:
        config_path {Text}: path to config
    """

    with open(config_path) as conf_file:
        config = yaml.safe_load(conf_file)

    logger = get_logger('TRAIN', log_level=config['base']['log_level'])

    logger.info('Load featured data')
    data_norm = pd.read_csv(config['elbow']['norm_path'], encoding=config['data_load']['encoding'])
    data_rfm = pd.read_csv(config['elbow']['rfm_path'], encoding=config['data_load']['encoding'])

    n_clusters = config['train']['n_clusters']
    kmeans = KMeans(n_clusters=n_clusters, random_state=1)
    kmeans.fit(data_norm)
    data_rfm["cluster"] = kmeans.predict(data_norm)

    #sns.heatmap(data_rfm[['Recency', 'Frequency', 'Monetary']].corr(), cmap="Reds")

    # get centroids
    centroids = kmeans.cluster_centers_
    cen_x = [i[0] for i in centroids]
    cen_y = [i[1] for i in centroids]

    ## add to dataframe
    data_rfm['cen_x'] = data_rfm.cluster.map({0: cen_x[0], 1: cen_x[1], 2: cen_x[2]})
    data_rfm['cen_y'] = data_rfm.cluster.map({0: cen_y[0], 1: cen_y[1], 2: cen_y[2]})

    # define and map colors
    colors = ['#DF2020', '#81DF20', '#2095DF']
    data_rfm['c'] = data_rfm.cluster.map({0: colors[0], 1: colors[1], 2: colors[2]})

    # Plot clusters
    plt.figure(figsize=(12, 10))
    plt.scatter(data_rfm.log_F, data_rfm.log_M, c=data_rfm.c, alpha=0.6, s=25)
    plt.xlabel('Frequency', fontsize=15)
    plt.ylabel('Monetary', fontsize=15)

    plt.savefig(config['train']['graph_path'])


if __name__ == '__main__':

    args_parser = argparse.ArgumentParser()
    args_parser.add_argument('--config', dest='config', required=True)
    args = args_parser.parse_args()

    train_model(config_path=args.config)