from os import getenv
import requests as req
from utils.util import get_access_token, error_handler


def get_wait_list_comments():
    try:
        headers = {
            "Authorization": f"Bearer {get_access_token()}"
        }

        res = req.get(f"{getenv('BASE_URL')}/comment", headers=headers)

        return {**res.json(), "ok": res.ok}
    except Exception as e:
        error_handler(e)
        return None


def get_my_comments():
    try:
        headers = {
            "Authorization": f"Bearer {get_access_token()}"
        }

        res = req.get(f"{getenv('BASE_URL')}/comment/me", headers=headers)

        return res.json()
    except Exception as e:
        error_handler(e)
        return None


def get_page_comments(page_id: str):
    try:
        res = req.get(f"{getenv('BASE_URL')}/comment/page/{page_id}")

        return res.json()
    except Exception as e:
        error_handler(e)
        return None


def get_comment_by_id(comment_id: str):
    try:
        headers = {
            "Authorization": f"Bearer {get_access_token()}"
        }

        res = req.get(f"{getenv('BASE_URL')}/comment/{comment_id}", headers=headers)

        return res.json()
    except Exception as e:
        error_handler(e)
        return None


def create_comment(body: str,
                   page: str,
                   pageModel: str,
                   rate: int = None,
                   parentComment: str = None):
    try:

        sending_data = {key: value for key, value in locals().items()}

        headers = {
            "Authorization": f"Bearer {get_access_token()}"
        }

        res = req.post(f"{getenv('BASE_URL')}/comment", json=sending_data, headers=headers)

        return {**res.json(), "ok": res.ok}
    except Exception as e:
        error_handler(e)
        return None


def delete_comment(comment_id: str):
    try:
        headers = {
            "Authorization": f"Bearer {get_access_token()}"
        }

        res = req.delete(f"{getenv('BASE_URL')}/comment/{comment_id}", headers=headers)

        return {**res.json(), "ok": res.json()}
    except Exception as e:
        error_handler(e)
        return None


def approve_comment(comment_id: str):
    try:
        headers = {
            "Authorization": f"Bearer {get_access_token()}"
        }

        res = req.put(f"{getenv('BASE_URL')}/comment/approve/{comment_id}", headers=headers)

        return {**res.json(), "ok": res.ok}
    except Exception as e:
        error_handler(e)
        return None


def like_comment(comment_id: str):
    try:
        headers = {
            "Authorization": f"Bearer {get_access_token()}"
        }

        res = req.put(f"{getenv('BASE_URL')}/comment/like/{comment_id}", headers=headers)

        return {**res.json(), "ok": res.ok}
    except Exception as e:
        error_handler(e)
        return None


def dislike_comment(comment_id: str):
    try:
        headers = {
            "Authorization": f"Bearer {get_access_token()}"
        }

        res = req.put(f"{getenv('BASE_URL')}/comment/dislike/{comment_id}", headers=headers)

        return {**res.json(), "ok": res.ok}
    except Exception as e:
        error_handler(e)
        return None
