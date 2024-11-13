import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from sklearn.cluster import KMeans
from calculations.film_data_analysis import standardize_ratings
from sklearn.metrics import silhouette_score
from sklearn.decomposition import PCA
from sklearn.metrics.pairwise import euclidean_distances


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
    # TODO: Tu jest jeszcze git ilosc filmow
    X_set_1, X_set_2 = standardize_ratings(ratings1, ratings2, titles1, titles2)
    # TODO: Tu się łączy
    X_combined = np.vstack((X_set_1, X_set_2))

    # apply k-means clustering
    # TODO: i tu się źle generują i złe clustery robi
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    kmeans.fit(X_combined)
    df_combined = pd.DataFrame(X_combined)

    # Display the first 5 rows
    pd.set_option('display.max_rows', 100)
    pd.set_option('display.max_columns', 100)

    print("X_combined as DataFrame:\n", df_combined.head(65))
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


    X_set_1, X_set_2 = standardize_ratings(ratings1, ratings2, titles1, titles2)
    X_combined = np.vstack((X_set_1, X_set_2))
    optimal_clusters = optimal_k(X_combined)

    print(f'ratings2: {ratings2}')

    X_combined, kmeans = apply_clustering_to_dataset(ratings1, ratings2, titles1, titles2, n_clusters=optimal_clusters)
    labels = kmeans.labels_
    print(f'kmeans.labels_: {labels}')

    # apply PCA
    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X_combined)

    # Create a DataFrame with PCA coordinates, titles, and cluster labels
    all_titles = titles1 + titles2
    all_ratings = ratings1 + ratings2

    data = {
        'Title': all_titles,
        'PCA_X': X_pca[:, 0],
        'PCA_Y': X_pca[:, 1],
        'Rating': all_ratings,
        'Cluster': labels
    }
    df = pd.DataFrame(data)
    # print(f'titles: {all_titles}\n, Ratings: {all_ratings}\n, Clusters: {labels}')
    # drawing points
    for i, title in enumerate(titles1 + titles2):
        if i < 80:
            plt.annotate(title, (X_pca[i, 0], X_pca[i, 1]), fontsize=8, alpha=0.7)

    plt.figure(figsize=(10, 8))
    _create_plot(X_pca, labels, optimal_clusters)

    return df


def find_similar_films(df, cluster1=0, cluster2=1, rating_threshold=7):
    """
    Finds films in the second cluster that are similar to films in the first cluster based on high ratings and PCA coordinates.
    Ensures that the closest films are in different clusters.

    :param df: DataFrame containing PCA coordinates, titles, and cluster labels.
    :param ratings1: Ratings given by the first user.
    :param ratings2: Ratings given by the second user.
    :param cluster1: The cluster label for the first cluster.
    :param cluster2: The cluster label for the second cluster.
    :param rating_threshold: The threshold above which films are considered highly rated.
    :return: A DataFrame of similar films in the second cluster.
    """
    # extract high-rating films in each cluster
    high_rating_films_cluster1 = df[
        (df['Cluster'] == cluster1) & (df['Rating'] >= rating_threshold)
        ]
    high_rating_films_cluster2 = df[
        (df['Cluster'] == cluster2) & (df['Rating'] >= rating_threshold)
        ]

    common_titles = set(high_rating_films_cluster1['Title']).intersection(set(high_rating_films_cluster2['Title']))
    if not common_titles or len(common_titles) < 4:
        print("Same high rated videos not found")
        return pd.DataFrame()

    # if no films meet the rating threshold in either cluster, return an empty DataFrame
    if high_rating_films_cluster1.empty or high_rating_films_cluster2.empty:
        print("No highly rated films found in one of the clusters.")
        return pd.DataFrame()

    # find the closest films in Cluster 2 for each film in Cluster 1
    results = []
    for idx1, row1 in high_rating_films_cluster1.iterrows():
        # compute distances to all films in Cluster 2
        distances = euclidean_distances(
            np.array([row1[['PCA_X', 'PCA_Y']]]),
            high_rating_films_cluster2[['PCA_X', 'PCA_Y']].values
        )
        # get the index of the closest film in Cluster 2
        closest_idx = np.argmin(distances)
        closest_film = high_rating_films_cluster2.iloc[closest_idx]

        # store the result if the closest film is indeed in a different cluster
        results.append({
            'Film in Cluster 1': row1['Title'],
            'Film in Cluster 2': closest_film['Title'],
            'Distance': distances[0][closest_idx]
        })

    # Create a DataFrame with the matched films and their distances
    similar_films_df = pd.DataFrame(results)
    print(similar_films_df)
    return similar_films_df
