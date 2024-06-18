from os import getenv
import requests as req
from utils.util import get_access_token, error_handler
import json


def get_all_approved_movies():
    res = req.get(f'{getenv('BASE_URL')}/movie/approve')

    return res.json()


def get_all_movies():
    headers = {
        'Authorization': f'Bearer {get_access_token()}'
    }

    res = req.get(f'{getenv('BASE_URL')}/movie', headers=headers)

    return {**res.json(), "ok": res.ok}


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
                 cast: list,
                 isPublished: bool):
    try:
        data = {
            "fullName": fullName,
            "summary": summary,
            "genre": genre,
            "releaseDate": releaseDate,
            "countries": countries,
            "movieLanguage": language,
            "budget": budget,
            "isPublished": isPublished
        }

        for index, cst in enumerate(cast):
            data[f"cast[{index}][castId]"] = cst['castId']
            data[f"cast[{index}][inMovieName]"] = cst['inMovieName']
            data[f"cast[{index}][inMovieRole]"] = cst['inMovieRole']

        headers = {
            "Authorization": f"Bearer {get_access_token()}"
        }

        # Prepare files for the request
        with open(cover, 'rb') as profile_pic_file:
            # Start the list of files with the profile picture
            files = [
                ("cover", ("cover.jpg", profile_pic_file, "image/jpeg"))
            ]

            # Prepare photo files for the request
            photo_files = [("medias", (f"media{index}.jpg", open(photo, 'rb'), "image/jpeg")) for index, photo in
                           enumerate(medias)]

            # Add photo files to the list of files
            files.extend(photo_files)

            res = req.post(f"{getenv('BASE_URL')}/movie", data=data, files=files, headers=headers)

        for _, (_, photo_file, _) in photo_files:
            photo_file.close()

        return {**res.json(), "ok": res.ok}
    except Exception as e:
        error_handler(e)
        return None


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
                       cast: list = None,
                       isPublished: bool = None):
    try:
        sending_data = {key: value for key, value in locals().items()}

        headers = {
            "Authorization": f"Bearer {get_access_token()}"
        }

        files = {
            "cover": open(cover, 'rb'),
        }

        for index, media in enumerate(medias):
            files[f"medias[{index}]"] = open(media, 'rb')

        res = req.post(f"{getenv('BASE_URL')}/movie/{movie_id}", json=sending_data, files=files, headers=headers)

        return {**res.json(), "ok": res.ok}
    except Exception as e:
        error_handler(e)
        return None


def delete_movie_by_id(movie_id: str):
    try:
        headers = {
            'Authorization': f'Bearer {get_access_token()}'
        }

        res = req.delete(f'{getenv("BASE_URL")}/movie/{movie_id}', headers=headers)

        return {**res.json(), "ok": res.ok}
    except Exception as e:
        error_handler(e)
        return None


def change_movie_status_by_id(movie_id: str):
    try:
        headers = {
            'Authorization': f'Bearer {get_access_token()}'
        }

        res = req.put(f'{getenv("BASE_URL")}/movie/status/{movie_id}', headers=headers)

        return {**res.json(), "ok": res.ok}
    except Exception as e:
        error_handler(e)
        return None


def search_in_movies(q: str):
    try:
        res = req.get(f'{getenv("BASE_URL")}/movie/search?q={q}')

        return res.json()
    except Exception as e:
        error_handler(e)
        return None


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

        return {**res.json(), "ok": res.ok}
    except Exception as e:
        error_handler(e)
        return None


def delete_favorite_movie(movie_id: str):
    try:
        headers = {
            'Authorization': f'Bearer {get_access_token()}'
        }

        res = req.delete(f'{getenv("BASE_URL")}/favorite/movie', json={"movie": movie_id}, headers=headers)

        return {**res.json(), "ok": res.ok}
    except Exception as e:
        error_handler(e)
        return None


def get_latest_movies():
    try:
        res = req.get(f"{getenv('BASE_URL')}/movie/latest")

        return res.json()
    except Exception as e:
        return error_handler(e)


def get_random_genre_top_rated():
    try:
        res = req.get(f"{getenv('BASE_URL')}/movie/randomgenretoprated")
        return res.json()
    except Exception as e:
        return error_handler(e)
