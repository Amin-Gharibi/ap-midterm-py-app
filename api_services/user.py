import requests as req
from os import getenv
from utils.util import get_access_token, error_handler


def get_all_users():
    try:
        headers = {
            "Authorization": f"Bearer {get_access_token()}"
        }
        res = req.get(f'{getenv("BASE_URL")}/user', headers=headers)

        return {**res.json(), "ok": res.ok}
    except Exception as e:
        error_handler(e)
        return None


def get_users_wait_list():
    try:
        headers = {
            "Authorization": f"Bearer {get_access_token()}"
        }
        res = req.get(f'{getenv("BASE_URL")}/user/waitlist', headers=headers)

        return {**res.json(), "ok": res.ok}
    except Exception as e:
        error_handler(e)
        return None


def get_user_by_id(user_id: str):
    try:
        headers = {
            "Authorization": f"Bearer {get_access_token()}"
        }
        res = req.get(f'{getenv("BASE_URL")}/user/{user_id}', headers=headers)

        return {**res.json(), "ok": res.ok}
    except Exception as e:
        error_handler(e)
        return None


def update_user(user_id: str,
                email: str = None,
                username: str = None,
                currentPassword: str = None,
                updatingPassword: str = None,
                fullName: str = None,
                role: str = None,
                profilePic=None):
    try:
        sending_data = {key: value for key, value in locals().items()}

        headers = {
            "Authorization": f"Bearer {get_access_token()}"
        }

        files = None
        if profilePic:
            files = {'profilePic': open(profilePic, 'rb')}

        res = req.put(f'{getenv("BASE_URL")}/user/{user_id}', json=sending_data, headers=headers, files=files)

        return {**res.json(), "ok": res.ok}
    except Exception as e:
        error_handler(e)
        return None


def delete_user(user_id: str):
    try:
        headers = {
            "Authorization": f"Bearer {get_access_token()}"
        }

        res = req.delete(f'{getenv("BASE_URL")}/user/{user_id}', headers=headers)

        return {**res.json(), "ok": res.ok}
    except Exception as e:
        error_handler(e)
        return None


def approve_user(user_id: str):
    try:
        headers = {
            "Authorization": f"Bearer {get_access_token()}"
        }

        res = req.put(f'{getenv("BASE_URL")}/user/approve/{user_id}', headers=headers)

        return {**res.json(), "ok": res.ok}
    except Exception as e:
        error_handler(e)
        return None


def reject_user(user_id: str):
    try:
        headers = {
            "Authorization": f"Bearer {get_access_token()}"
        }

        res = req.put(f'{getenv("BASE_URL")}/user/reject/{user_id}', headers=headers)

        return {**res.json(), "ok": res.ok}
    except Exception as e:
        error_handler(e)
        return None


def ban_user(user_id: str):
    try:
        headers = {
            "Authorization": f"Bearer {get_access_token()}"
        }

        res = req.put(f'{getenv("BASE_URL")}/user/ban/{user_id}', headers=headers)

        return {**res.json(), "ok": res.ok}
    except Exception as e:
        error_handler(e)
        return None


def unban_user(user_id: str):
    try:
        headers = {
            "Authorization": f"Bearer {get_access_token()}"
        }

        res = req.put(f'{getenv("BASE_URL")}/user/unban/{user_id}', headers=headers)

        return {**res.json(), "ok": res.ok}
    except Exception as e:
        error_handler(e)
        return None


def change_user_role(user_id: str, role: str):
    try:
        headers = {
            "Authorization": f"Bearer {get_access_token()}"
        }

        res = req.put(f'{getenv("BASE_URL")}/user/role/{user_id}', headers=headers)

        return res.json()
    except Exception as e:
        error_handler(e)
        return None


def search_user(query):
    try:
        headers = {
            "Authorization": f"Bearer {get_access_token()}"
        }

        res = req.get(f'{getenv("BASE_URL")}/user/search?q={query}', headers=headers)

        return {**res.json(), "ok": res.ok}
    except Exception as e:
        error_handler(e)
        return None
