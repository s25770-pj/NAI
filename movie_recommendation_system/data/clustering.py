import json
import numpy as np

from sklearn.preprocessing import StandardScaler
from sklearn.feature_extraction.text import TfidfVectorizer


with open('dataset.json', 'r') as f:
    dataset = json.load(f)

def get_titles_and_ratings(name1, name2):
    film_titles1 = [title for obj in dataset if obj['name'] == f'{name1}' for title in obj['ratings']]
    film_titles2 = [title for obj in dataset if obj['name'] == f'{name2}' for title in obj['ratings']]
    all_titles = film_titles1 + film_titles2

    film_ratings1 = [title for obj in dataset if obj['name'] == f'{name1}' for title in obj['ratings'].values()]
    film_ratings2 = [title for obj in dataset if obj['name'] == f'{name2}' for title in obj['ratings'].values()]
    return {'film_titles1': film_titles1,
            'film_titles2': film_titles2,
            'film_ratings1': film_ratings1,
            'film_ratings2': film_ratings2,
            'all_titles': all_titles}


def convert_titles_into_vectors(titles):
    vectorizer = TfidfVectorizer(stop_words='english')
    return vectorizer.fit_transform(titles)


def create_rating_sets(ratings1, ratings2):
    rating1 = np.array(ratings1).reshape(-1, 1)
    rating2 = np.array(ratings2).reshape(-1, 1)
    return rating1, rating2


def concatenate_ratings(ratings1, ratings2, titles1, titles2):
    rating_set_1, rating_set_2 = create_rating_sets(ratings1, ratings2)
    titles = titles1 + titles2
    X = convert_titles_into_vectors(titles)

    X_set_1 = np.hstack((X[:len(titles1)].toarray(), rating_set_1))
    X_set_2 = np.hstack((X[len(titles2):].toarray(), rating_set_2))
    return X_set_1, X_set_2

def standardize_ratings(ratings1, ratings2, titles1, titles2):
    X_set_1, X_set_2 = concatenate_ratings(ratings1, ratings2, titles1, titles2)
    scaler = StandardScaler()
    X_set_1[:, -1] = scaler.fit_transform(X_set_1[:, -1].reshape(-1, 1)).flatten()
    X_set_2[:, -1] = scaler.transform(X_set_2[:, -1].reshape(-1, 1)).flatten()

