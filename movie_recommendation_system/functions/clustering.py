import json
import numpy as np

from sklearn.cluster import KMeans
from sklearn.impute import SimpleImputer
from euclidean_score import euclidean_distance


with open('../data/dataset.json', 'r') as f:
    dataset = json.loads(f.read())

def prepare_ratings_matrix(target_user_name, n_clusters=3):
    all_movies = set()
    ratings = []

    # collect all unique movies rated by any user
    for user in dataset.values():
        all_movies.update(user.keys())

    all_movies = list(all_movies)

    # prepare ratings matrix where each row represents a user and each column represents a movie
    for user in dataset.values():
        current_user_ratings = [user.get(movie, np.nan) for movie in all_movies]
        ratings.append(current_user_ratings)

    ratings_matrix = np.array(ratings)

    # impute missing values (NaNs) with column (movie) means for clustering
    imputer = SimpleImputer(strategy='mean')
    ratings_matrix_imputed = imputer.fit_transform(ratings_matrix)

    # apply K-Means clustering on the imputed ratings data
    kmeans = KMeans(n_clusters=n_clusters, random_state=0)
    kmeans.fit(ratings_matrix_imputed)

    # get the target user index and their cluster label
    target_user_idx = list(dataset.keys()).index(target_user_name)
    target_cluster_label = kmeans.labels_[target_user_idx]

    # find all users in the same cluster as the target user
    cluster_members_indices = [i for i, label in enumerate(kmeans.labels_) if label == target_cluster_label]

    # get cluster members' ratings and compute average ratings for each movie
    cluster_ratings = ratings_matrix[cluster_members_indices]

    # calculate average ratings with careful handling of NaNs
    with np.errstate(all='ignore'):
        avg_ratings_cluster = np.nanmean(cluster_ratings, axis=0)

    # set a default score for movies that have no ratings at all in the cluster
    global_mean_rating = np.nanmean(ratings_matrix)
    avg_ratings_cluster = np.where(np.isnan(avg_ratings_cluster), global_mean_rating, avg_ratings_cluster)

    # get ratings of the target user to identify movies they haven't rated
    target_user_ratings = ratings_matrix[target_user_idx]
    unseen_movies_idx = np.where(np.isnan(target_user_ratings))[0]

    # collect ratings for unseen movies
    unseen_ratings = [(movie_idx, avg_ratings_cluster[movie_idx]) for movie_idx in unseen_movies_idx]

    # sort movies by rating for high-rated and low-rated recommendations
    high_rated_movies = sorted(unseen_ratings, key=lambda x: x[1], reverse=True)
    low_rated_movies = sorted(unseen_ratings, key=lambda x: x[1])

    # recommend the top 5 liked and disliked movies
    top_likes = [all_movies[movie[0]] for movie in high_rated_movies[:5]]
    top_dislikes = [all_movies[movie[0]] for movie in low_rated_movies[:5]]

    return top_likes, top_dislikes


def find_closest_user(ratings_matrix, target_user_idx=0):
    """find the index of the user in ratings_matrix closest to the target user."""
    target_ratings = ratings_matrix[target_user_idx]
    closest_user_idx = None
    min_distance = float('inf')

    for i in range(1, ratings_matrix.shape[0]):
        distance = euclidean_distance(target_ratings, ratings_matrix[i])
        if distance < min_distance:
            min_distance = distance
            closest_user_idx = i

    return closest_user_idx
