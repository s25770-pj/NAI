import json
import numpy as np


with open('../data/dataset.json', 'r') as f:
    dataset = json.loads(f.read())


def euclidean_distance(user_ratings, other_ratings):
    """
    Calculate Euclidean distance between two users' ratings, ignoring NaNs.

    :param user_ratings: Searching user ratings.
    :param other_ratings: Other user ratings.
    :return: Distance between films:
    """
    mask = ~np.isnan(user_ratings) & ~np.isnan(other_ratings)
    if not np.any(mask):
        return float('inf')
    return np.sqrt(np.nansum((user_ratings[mask] - other_ratings[mask]) ** 2))
