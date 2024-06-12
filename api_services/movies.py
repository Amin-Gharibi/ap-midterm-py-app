from os import getenv
import requests as req
from utils.util import get_access_token, error_handler


def get_all_approved_movies():
    res = req.get(f'{getenv('BASE_URL')}/movie/approve')

    return res.json()


def get_all_movies():
    headers = {
        'Authorization': f'Bearer {get_access_token()}'
    }

    res = req.get(f'{getenv('BASE_URL')}/movie', headers=headers)

    return res.json()


def get_movie_by_id(movie_id):
    res = req.get(f'{getenv('BASE_URL')}/movie/{movie_id}')

    return res.json()


def create_movie(fullName: str,
                 summary: str,
                 genre: str,
                 releaseDate: str,
                 countries: str,
                 language: str,
                 budget: str,
                 cover: str,
                 medias: list,
                 cast: list):

    sending_data = {key: value for key, value in locals().items()}

    headers = {
        'Authorization': f'Bearer {get_access_token()}'
    }

    res = req.post(f'{getenv("BASE_URL")}/movie', json=sending_data, headers=headers)

    return res.json()


def update_movie_by_id(movie_id: str,
                       fullName: str = None,
                       summary: str = None,
                       genre: str = None,
                       releaseDate: str = None,
                       countries: str = None,
                       language: str = None,
                       budget: str = None,
                       cover: str = None,
                       medias: list = None,
                       cast: list = None):

    sending_data = {key: value for key, value in locals().items() if key != 'movie_id' and value is not None}

    headers = {
        'Authorization': f'Bearer {get_access_token()}'
    }

    res = req.put(f'{getenv("BASE_URL")}/movie/{movie_id}', json=sending_data, headers=headers)

    return res.json()


def delete_movie_by_id(movie_id: str):
    headers = {
        'Authorization': f'Bearer {get_access_token()}'
    }

    res = req.delete(f'{getenv("BASE_URL")}/movie/{movie_id}', headers=headers)

    return res.json()


def change_movie_status_by_id(movie_id: str):
    headers = {
        'Authorization': f'Bearer {get_access_token()}'
    }

    res = req.put(f'{getenv("BASE_URL")}/movie/status/{movie_id}', headers=headers)

    return res.json()


def search_in_movies(q: str):
    res = req.get(f'{getenv("BASE_URL")}/movie/search?q={q}')

    return res.json()


def get_favorite_movies():
    try:
        headers = {
            'Authorization': f'Bearer {get_access_token()}'
        }

        res = req.get(f'{getenv("BASE_URL")}/favorite/movie', headers=headers)

        return res.json()
    except Exception as e:
        error_handler(e)
        return None

def add_favorite_movie(movie_id: str):
    try:
        headers = {
            'Authorization': f'Bearer {get_access_token()}'
        }

        res = req.post(f'{getenv("BASE_URL")}/favorite/movie', json={"movie": movie_id}, headers=headers)

        return res.json()
    except Exception as e:
        error_handler(e)
        return None


def delete_favorite_movie(movie_id: str):
    try:
        headers = {
            'Authorization': f'Bearer {get_access_token()}'
        }

        res = req.delete(f'{getenv("BASE_URL")}/favorite/movie', json={"movie": movie_id}, headers=headers)

        return res.json()
    except Exception as e:
        error_handler(e)
        return None
