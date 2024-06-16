from wsgiref import headers

import requests as req
from os import getenv
from utils.util import get_access_token, error_handler


def create_cast(fullName: str,
                biography: str,
                birthDate: str,
                birthPlace: str,
                profilePic: str,
                photos: tuple,
                height: str):
    try:
        sending_data = {key: value for key, value in locals().items()}

        headers = {
            "Authorization": f"Bearer {get_access_token()}"
        }

        files = {
            "profilePic": open(profilePic, 'rb'),
        }

        for index, photo in enumerate(photos):
            files[f"photos[{index}]"] = open(photo, 'rb')

        res = req.post(f"{getenv('BASE_URL')}/cast", json=sending_data, files=files, headers=headers)

        return {**res.json(), "ok": res.ok}
    except Exception as e:
        error_handler(e)
        return None


def get_all_casts():
    try:
        headers = {
            'Authorization': f'Bearer {get_access_token()}'
        }
        res = req.get(f"{getenv('BASE_URL')}/cast", headers=headers)

        return {**res.json(), "ok": res.ok}
    except Exception as e:
        return error_handler(e)


def delete_cast(cast_id: str):
    try:
        headers = {
            'Authorization': f'Bearer {get_access_token()}'
        }
        res = req.delete(f"{getenv('BASE_URL')}/cast/{cast_id}", headers=headers)

        return {**res.json(), "ok": res.ok}
    except Exception as e:
        return error_handler(e)


def search_cast(q: str):
    try:
        res = req.get(f"{getenv('BASE_URL')}/cast/search?q={q}")

        return {**res.json(), "ok": res.ok}
    except Exception as e:
        return error_handler(e)


def get_top_rated_cast():
    try:
        res = req.get(f"{getenv('BASE_URL')}/cast/toprated")

        return res.json()
    except Exception as e:
        return error_handler(e)