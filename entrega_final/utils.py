import pandas as pd
import numpy as np
import cupy as cp
from cuml import UMAP
from cuml.cluster.hdbscan import HDBSCAN
from cuml.feature_extraction.text import TfidfVectorizer
from tqdm import tqdm

def reducir_dimensiones(
    embeddings: np.ndarray,
    umap_kwargs: dict,
    verbose: bool = True
) -> pd.DataFrame:

    dim_model = UMAP(**umap_kwargs)
    if verbose:
        print("Reduciendo la dimension de los embeddings...")
    reduced_embeddings = dim_model.fit_transform(embeddings)
    if verbose:
        print("Dimension de embeddings reducida!")
    return reduced_embeddings


def generar_clusters(
    embeddings: np.ndarray,
    hdbscan_kwargs: dict,
    verbose: bool = True
):
    cluster_model = HDBSCAN(**hdbscan_kwargs)
    if verbose:
        print("Generando clusters...")
    clusters = cluster_model.fit_predict(embeddings)
    if verbose:
        print("Clusters generados!")
    return clusters


def keywords_keybert(
    modelo,
    data: pd.DataFrame,
    unique_clusters: list,
    keybert_args: dict,
    verbose: bool = True
) -> pd.DataFrame:

    if verbose:
        print(f"Obteniendo keywords...")

    top_words_per_cluster = {}

    for cluster in tqdm(unique_clusters, total=len(unique_clusters)):
        cluster_data = ". ".join(data[data.cluster == cluster]["review"])
        top_words = modelo.extract_keywords(
            cluster_data,
            **keybert_args
        )
        top_words = [kw[0] for kw in top_words]
        top_words_per_cluster[cluster] = top_words

    if verbose:
        print(f"Keywords generados...")

    return pd.DataFrame(
        list(top_words_per_cluster.items()),
        columns=["cluster", "keywords"]
    )


def palabras_importantes_por_cluster(
    data: pd.DataFrame,
    cluster_num: int,
    n_words: int,
    tfidf_kwargs: dict
) -> list:
    cluster_data = data[data.cluster == cluster_num]["review"]

    vectorizer = TfidfVectorizer(**tfidf_kwargs)
    tfidf_matrix = vectorizer.fit_transform(cluster_data)

    feature_names = vectorizer.get_feature_names()
    sum_tfidf_scores = tfidf_matrix.sum(axis=0)
    avg_tfidf_scores = sum_tfidf_scores / tfidf_matrix.shape[0]
    avg_tfidf_scores_cp = cp.array(avg_tfidf_scores)
    top_n_indices = cp.argsort(avg_tfidf_scores_cp.ravel())[::-1][:n_words]
    top_n_words = [feature_names[i] for i in cp.asnumpy(top_n_indices)]
    
    return top_n_words


def palabras_importantes_general(
    data: pd.DataFrame,
    unique_clusters: list,
    n_words: int,
    tfidf_kwargs: dict,
    verbose: bool = True
) -> pd.DataFrame:
    if verbose:
        print(f"Obteniendo el top {n_words} de palabras...")

    top_words_per_cluster = {}

    for cluster in tqdm(unique_clusters, total=len(unique_clusters)):
        top_words = palabras_importantes_por_cluster(data=data, cluster_num=cluster, n_words=n_words, tfidf_kwargs=tfidf_kwargs)
        top_words_per_cluster[cluster] = top_words

    if verbose:
        print(f"Top {n_words} de palabras obtenido...")

    return pd.DataFrame(
        list(top_words_per_cluster.items()),
        columns=["cluster", "keywords"]
    )