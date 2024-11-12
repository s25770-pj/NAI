from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import numpy as np
from calculations.film_data_analysis import standardize_ratings
from sklearn.metrics import silhouette_score
from sklearn.decomposition import PCA


def apply_clustering_to_dataset(ratings1, ratings2, titles1, titles2, n_clusters=2):
    """
   applies KMeans clustering on the dataset.

   :param ratings1: Ratings of the first user.
   :param ratings2: Ratings of the second user.
   :param titles1: Movie titles rated by the first user.
   :param titles2: Movie titles rated by the second user.
   :param n_clusters: Number of clusters for the KMeans algorithm (default is 2).
   :return: A tuple containing:
       - X_combined: The combined dataset (ratings and title vectors).
       - kmeans: The fitted KMeans object.
   """
    X_set_1, X_set_2 = standardize_ratings(ratings1, ratings2, titles1, titles2)
    X_combined = np.vstack((X_set_1, X_set_2))

    # apply k-means clustering
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    kmeans.fit(X_combined)
    return X_combined, kmeans


def optimal_k(X_combined):
    """
    determines the optimal number of clusters using silhouette score.

    :param X_combined: The dataset for clustering.
    :return: The optimal number of clusters based on silhouette score.
    """
    # TODO: nie wiem czy to sie przyda, poczatkowo mialo to miec mozliwosc porownywania wszystkich na raz
    max_score = -1
    best_k = 2

    # try number of clusters from 2 to 10 and find the best silhouette score
    for k in range(2, 11):
        kmeans = KMeans(n_clusters=k, random_state=42)
        kmeans.fit(X_combined)
        score = silhouette_score(X_combined, kmeans.labels_)
        if score > max_score:
            max_score = score
            best_k = k

    return best_k


def plot_clusters(ratings1, ratings2, titles1, titles2):
    """
    plots the clusters formed by applying KMeans on the combined dataset.

    :param ratings1: Ratings of the first user.
    :param ratings2: Ratings of the second user.
    :param titles1: Movie titles rated by the first user.
    :param titles2: Movie titles rated by the second user.
    """
    def _create_plot(X_pca, labels, optimal_clusters):
        # scatter plot with clusters
        plt.scatter(X_pca[:, 0], X_pca[:, 1], c=labels, cmap='viridis', marker='o', s=100)

        # setup plot
        plt.title(f"Clustering Movies into {optimal_clusters} Clusters", fontsize=14, pad=20)
        plt.xlabel('Principal Component 1', fontsize=12, labelpad=15)
        plt.ylabel('Principal Component 2', fontsize=12, labelpad=15)
        plt.colorbar(label='Cluster', shrink=0.8, aspect=20)
        plt.tight_layout()
        plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)
        plt.savefig('plot.png', bbox_inches='tight')
        plt.close()


    def _annotate_each_point():
        for i, title in enumerate(titles1 + titles2):
            if i < 80:
                plt.annotate(title, (X_pca[i, 0], X_pca[i, 1]), fontsize=8, alpha=0.7)

        plt.figure(figsize=(10, 8))


    # standardize and combine ratings and titles
    X_set_1, X_set_2 = standardize_ratings(ratings1, ratings2, titles1, titles2)
    X_combined = np.vstack((X_set_1, X_set_2))

    # determine optimal number of clusters
    optimal_clusters = optimal_k(X_combined)
    print(f"Optimal number of clusters: {optimal_clusters}")

    # apply clustering
    X_combined, kmeans = apply_clustering_to_dataset(ratings1, ratings2, titles1, titles2, n_clusters=optimal_clusters)
    labels = kmeans.labels_

    # apply PCA
    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X_combined)

    _annotate_each_point()
    _create_plot(X_pca, labels, optimal_clusters)