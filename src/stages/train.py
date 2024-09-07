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
    data = pd.read_csv(config['data_load']['dataset_prepare'], encoding=config['data_load']['encoding'])
    data_norm = pd.read_csv(config['elbow']['norm_path'], encoding=config['data_load']['encoding'])
    data_rfm = pd.read_csv(config['elbow']['rfm_path'], encoding=config['data_load']['encoding'])

    n_clusters = config['train']['n_clusters']
    max_iter = config['train']['max_iter']
    random_state = config['base']['random_state']
    kmeans = KMeans(n_clusters=n_clusters, max_iter=max_iter, random_state=random_state)
    kmeans.fit(data_norm)
    data_rfm["cluster"] = kmeans.predict(data_norm)

    #fig = sns.heatmap(data_rfm[['Recency', 'Frequency', 'Monetary']].corr(), cmap="Reds")
    #fig.savefig("heatmap.png")

    # get centroids
    centroids = kmeans.cluster_centers_
    cen_x = [i[0] for i in centroids]
    cen_y = [i[1] for i in centroids]

    ## add to dataframe
    data_rfm['cen_x'] = data_rfm.cluster.map({0: cen_x[0], 1: cen_x[1], 2: cen_x[2]})
    data_rfm['cen_y'] = data_rfm.cluster.map({0: cen_y[0], 1: cen_y[1], 2: cen_y[2]})

    # define and map colors
    colors = ['#DF2020', '#81DF20', '#2095DF', '#8e7cc3']
    data_rfm['c'] = data_rfm.cluster.map({0: colors[0], 1: colors[1], 2: colors[2], 3: colors[3]})

    df_cluster = pd.merge(data, data_rfm, on='CustomerID', how='right')
    rfm_path = config['train']['cluster_path']
    df_cluster.to_csv(rfm_path, index=False)


    # Crear el gráfico de pastel
    logger.info('save pie population data graph')

    grouped = df_cluster.groupby('cluster')
    group_counts = grouped.size()
    plt.pie(group_counts, labels=group_counts.index, autopct='%1.1f%%')
    plt.title("Poblacion por cluster", fontsize=18)
    plt.savefig(config['train']['pie_poblacion_graph_path'])

    logger.info('save pie total sales data graph')

    grouped = df_cluster.groupby('cluster')['Total_sales'].sum()
    plt.title("Total de compras por cluster", fontsize=18)
    plt.pie(grouped, labels=grouped.index, autopct='%1.1f%%')
    plt.savefig(config['train']['pie_compras_graph_path'])

    logger.info('save 3d graph')
    generate3d(config, data_rfm)


def generate3d(config, data_rfm):
    fig = plt.figure(figsize=(12, 12))
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(data_rfm.log_R, data_rfm.log_M, data_rfm.log_F, c=data_rfm.c, cmap='viridis')
    ax.set_xlabel('log_R')
    ax.set_ylabel('log_M')
    ax.set_zlabel('log_F')
    ax.set_xlabel('Recency', fontsize=12)
    ax.set_ylabel('Monetary', fontsize=12)
    ax.set_zlabel('Frequency', fontsize=12)
    plt.savefig(config['train']['graph_path'])


if __name__ == '__main__':

    args_parser = argparse.ArgumentParser()
    args_parser.add_argument('--config', dest='config', required=True)
    args = args_parser.parse_args()

    train_model(config_path=args.config)