#!/usr/bin/env python3
#Authors: Jakub Pobłocki s25770, Kacper Pecka s25668

#All necessary information is available at:
#https://github.com/s25770-pj/NAI/blob/main/Z3/README.md

import json
import asyncio
from functions.clustering import prepare_ratings_matrix
from GUI.gui import run_gui


def main():
    with open('data/dataset.json', 'r', encoding='utf-8') as f:
        dataset = json.load(f)
    #print(prepare_ratings_matrix(target_user_name='Kacper Pecka'))
    asyncio.run(run_gui(dataset, prepare_ratings_matrix))

if __name__ == '__main__':
    # if len(sys.argv) != 3:
    #     print("Usage: python script.py <name1> <name2>")
    #     sys.exit(1)

    main()
