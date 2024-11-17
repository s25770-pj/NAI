#!/usr/bin/env python3
from functions.clustering import prepare_ratings_matrix


def main():
    print(prepare_ratings_matrix(target_user_name='Kacper Pecka'))


if __name__ == '__main__':
    # if len(sys.argv) != 3:
    #     print("Usage: python script.py <name1> <name2>")
    #     sys.exit(1)

    main()
