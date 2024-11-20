import requests
import json


api_key = "da2b34ef"


def search_film_by_title(title, api_key=api_key):
    r = requests.get(f'http://www.omdbapi.com/?apikey={api_key}&t={title}')
    return r.json()


def get_unique_titles():
    # TODO: do przebudowania (zmieniona baza)
    with open('../data/dataset.json', 'r') as f:
        dataset = json.load(f)

    titles = []

    for obj in dataset:
        for title in obj['ratings']:
            if title not in titles:
                titles.append(title)
    return titles


def check_titles_uniqueness():
    titles = get_unique_titles()
    for title in titles:
        film = search_film_by_title(title)
        if film['Response'] == 'False':
            print(f'title: {title}')
            print(film),
