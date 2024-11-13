#!/usr/bin/env python3
import sys

from calculations.clustering import plot_clusters, find_similar_films
from calculations.film_data_analysis import get_ratings_and_titles


def main():
    ratings1, ratings2, titles1, titles2 = get_ratings_and_titles(sys.argv[1], sys.argv[2])
    print(f'ratings1: {ratings1} ratings2: {ratings2}, titles1: {titles1} titles2: {titles2}')
    df = plot_clusters(ratings1, ratings2, titles1, titles2)
    find_similar_films(df)


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python script.py <name1> <name2>")
        sys.exit(1)

    main()
