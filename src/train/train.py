import pandas as pd
from sklearn.cluster import (
    KMeans,
    SpectralClustering,
    AgglomerativeClustering,
    AffinityPropagation,
    Birch,
    DBSCAN,
    OPTICS,
)
from sklearn.mixture import GaussianMixture
from typing import Text


class UnSupportedClusteringMethod(Exception):
    def __init__(self, clustering_method):
        self.msg = f"Unsupported clustering method {clustering_method}"
        super().__init__(self.msg)


def get_supported_clustering_methods():
    """Return supported clustering methods
    Returns:
        List: supported clustering methods
    """

    return {
        "kmeans": KMeans,
        "dbscan": DBSCAN,
        "hierarchical": AgglomerativeClustering,
        "birch": Birch,
        "affinity": AffinityPropagation,
        "spectral": SpectralClustering,
        "gaussian": GaussianMixture,
        "optics": OPTICS,
    }


def train(
    df: pd.DataFrame,
    estimator_name: Text,
    n_clusters: int,
    max_iter: int,
    random_state: int,
) -> pd.DataFrame:
    """Train model.
    Args:
        df {pd.DataFrame}: dataframe
        estimator_name {Text}: clustering method
    Returns:
        trained_model
    """

    supported_clustering_methods = get_supported_clustering_methods()
    NO_N_METHODS = ["dbscan", "optics", "affinity", "birch"]

    if estimator_name not in supported_clustering_methods:
        raise UnSupportedClusteringMethod(estimator_name)

    estimator = supported_clustering_methods[estimator_name]

    if estimator in NO_N_METHODS:
        model = estimator()
    elif estimator == "gaussian":
        model = estimator(n_components=n_clusters, random_state=random_state)
    else:
        model = estimator(
            n_clusters=n_clusters, max_iter=max_iter, random_state=random_state
        )

    model.fit(df)

    return model
