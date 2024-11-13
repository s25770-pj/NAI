import json
import numpy as np

from sklearn.preprocessing import StandardScaler
from sklearn.feature_extraction.text import TfidfVectorizer


# load the dataset
with open('data/dataset.json', 'r') as f:
    dataset = json.load(f)

def get_ratings_and_titles(name1, name2):
    """
    extracts the film titles and ratings for two given users from the dataset.

    :param name1: Name of the first user.
    :param name2: Name of the second user.
    :return: A dictionary containing:
        - 'titles1': List of movie titles rated by the first user.
        - 'titles2': List of movie titles rated by the second user.
        - 'ratings1': List of ratings given by the first user.
        - 'ratings2': List of ratings given by the second user.
    """
    # extract titles
    titles1 = [title for obj in dataset if obj['name'] == f'{name1}' for title in obj['ratings']]
    titles2 = [title for obj in dataset if obj['name'] == f'{name2}' for title in obj['ratings']]

    # extract ratings
    ratings1 = [rating for obj in dataset if obj['name'] == f'{name1}' for rating in obj['ratings'].values()]
    ratings2 = [rating for obj in dataset if obj['name'] == f'{name2}' for rating in obj['ratings'].values()]
    return ratings1, ratings2, titles1, titles2


def convert_titles_into_vectors(titles):
    """
    converts a list of movie titles into vectors.

    :param titles: List of movie titles.
    :return: A sparse matrix of TF-IDF vectors representing the movie titles.
    """
    titles = [str(title) for title in titles]

    vectorizer = TfidfVectorizer(stop_words='english')
    return vectorizer.fit_transform(titles)


def create_rating_sets(ratings1, ratings2):
    """
    converts the ratings into column vectors (reshape into 2D arrays).

    :param ratings1: Ratings of the first user.
    :param ratings2: Ratings of the second user.
    :return: Two numpy arrays (rating_set_1 and rating_set_2) of shape (n_samples, 1).
    """
    rating_set_1 = np.array(ratings1).reshape(-1, 1)
    rating_set_2 = np.array(ratings2).reshape(-1, 1)
    return rating_set_1, rating_set_2


def concatenate_ratings(ratings1, ratings2, titles1, titles2):
    """
    concatenates the vectors of movie titles with the ratings for both users.

    :param ratings1: Ratings of the first user.
    :param ratings2: Ratings of the second user.
    :param titles1: Movie titles rated by the first user.
    :param titles2: Movie titles rated by the second user.
    :return: Two numpy arrays (X_set_1 and X_set_2) containing the concatenated data for both users.
    """
    rating_set_1, rating_set_2 = create_rating_sets(ratings1, ratings2)
    titles = titles1 + titles2
    title_vectors = convert_titles_into_vectors(titles)

    X_set_1 = np.hstack((title_vectors[:len(titles1)].toarray(), rating_set_1))

    if len(titles2) > 0:
        X_set_2 = np.hstack((title_vectors[len(titles1):len(titles1) + len(titles2)].toarray(), rating_set_2))
    else:
        X_set_2 = np.empty((0, title_vectors.shape[1]))  # Empty array if titles2 is empty

    return X_set_1, X_set_2


def standardize_ratings(ratings1, ratings2, titles1, titles2):
    """
    standardizes the ratings for both users.

    :param ratings1: Ratings of the first user.
    :param ratings2: Ratings of the second user.
    :param titles1: Movie titles rated by the first user.
    :param titles2: Movie titles rated by the second user.
    :return: Two numpy arrays (X_set_1 and X_set_2) with standardized ratings.
    """
    # concatenate ratings and titles for both users
    X_set_1, X_set_2 = concatenate_ratings(ratings1, ratings2, titles1, titles2)

    # Separate ratings and titles (assuming ratings are numerical and titles are strings)
    ratings1_data = X_set_1[:, -1].reshape(-1, 1)
    ratings2_data = X_set_2[:, -1].reshape(-1, 1)

    scaler = StandardScaler()

    # scale ratings
    if len(ratings1_data) > 0:
        X_set_1[:, -1] = scaler.fit_transform(ratings1_data).flatten()

    if len(ratings2_data) > 0:
        X_set_2[:, -1] = scaler.fit_transform(ratings2_data).flatten()

    return X_set_1, X_set_2

