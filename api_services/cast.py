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
        data = {
            "fullName": fullName,
            "biography": biography,
            "birthDate": birthDate,
            "birthPlace": birthPlace,
            "height": height
        }

        headers = {
            "Authorization": f"Bearer {get_access_token()}"
        }

        # Prepare files for the request
        with open(profilePic, 'rb') as profile_pic_file:
            # Start the list of files with the profile picture
            files = [
                ("profilePic", ("profilePic.jpg", profile_pic_file, "image/jpeg"))
            ]

            # Prepare photo files for the request
            photo_files = [("photos", (f"photo{index}.jpg", open(photo, 'rb'), "image/jpeg")) for index, photo in enumerate(photos)]

            # Add photo files to the list of files
            files.extend(photo_files)

            res = req.post(f"{getenv('BASE_URL')}/cast", data=data, files=files, headers=headers)

        for _, (_, photo_file, _) in photo_files:
            photo_file.close()

        return {**res.json(), "ok": res.ok}
    except Exception as e:
        error_handler(e)
        return None


def edit_cast(cast_id: str,
              fullName: str = None,
              biography: str = None,
              birthDate: str = None,
              birthPlace: str = None,
              profilePic: str = None,
              photos: tuple = None,
              height: str = None):
    try:
        data = {
            "fullName": fullName,
            "biography": biography,
            "birthDate": birthDate,
            "birthPlace": birthPlace,
            "height": height
        }

        headers = {
            "Authorization": f"Bearer {get_access_token()}"
        }

        # Prepare profile picture for the request
        files = []
        if profilePic:
            files.append(("profilePic", ("profilePic.jpg", open(profilePic, 'rb'), "image/jpeg")))

        # Prepare photo files for the request
        if photos and len(photos):
            photo_files = [("photos", (f"photo{index}.jpg", open(photo, 'rb'), "image/jpeg")) for index, photo in enumerate(photos)]
            # Add photo files to the list of files
            files.extend(photo_files)

        res = req.put(f"{getenv('BASE_URL')}/cast/{cast_id}", data=data, files=files, headers=headers)

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


def get_one_cast(cast_id: str):
    try:
        res = req.get(f"{getenv('BASE_URL')}/cast/{cast_id}")

        return res.json()
    except Exception as e:
        return error_handler(e)


def get_cast_movies(cast_id: str):
    try:
        res = req.get(f"{getenv('BASE_URL')}/cast/movies/{cast_id}")

        return res.json()
    except Exception as e:
        return error_handler(e)
