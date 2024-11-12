#!/usr/bin/env python3
import sys

from calculations.clustering import plot_clusters
from calculations.film_data_analysis import get_ratings_and_titles


def main():
    plot_clusters(*get_ratings_and_titles(sys.argv[1], sys.argv[2]))


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python script.py <name1> <name2>")
        sys.exit(1)

    main()