from os import getenv
import requests as req
from utils.util import get_access_token, error_handler


def get_all_articles():
    try:
        headers = {
            "Authorization": f"Bearer {get_access_token()}"
        }

        res = req.get(f"{getenv('BASE_URL')}/article", headers=headers)

        return {**res.json(), "ok": res.ok}
    except Exception as e:
        error_handler(e)
        return None


def get_all_published_articles():
    try:
        res = req.get(f"{getenv('BASE_URL')}/article/published")

        return res.json()
    except Exception as e:
        error_handler(e)
        return None


def get_article_by_id(article_id: str):
    try:
        headers = {
            "Authorization": f"Bearer {get_access_token()}"
        }

        res = req.get(f"{getenv('BASE_URL')}/article/{article_id}", headers=headers)

        return res.json()
    except Exception as e:
        error_handler(e)
        return None


def get_my_articles():
    try:
        headers = {
            "Authorization": f"Bearer {get_access_token()}"
        }

        res = req.get(f"{getenv('BASE_URL')}/article/me", headers=headers)

        return res.json()
    except Exception as e:
        error_handler(e)
        return None


def create_article(title: str, body: str, cover: str, isPublished: bool):
    try:
        sending_data = {
            "title": title,
            "body": body,
            "isPublished": isPublished
        }

        headers = {
            "Authorization": f"Bearer {get_access_token()}"
        }

        files = None
        if cover:
            files = {'cover': open(cover, 'rb')}

        form_data = {key: str(value) for key, value in sending_data.items()}

        res = req.post(f"{getenv('BASE_URL')}/article", data=form_data, files=files, headers=headers)

        return {**res.json(), "ok": res.ok}
    except Exception as e:
        error_handler(e)
        return None


def delete_article(article_id: str):
    try:
        headers = {
            "Authorization": f"Bearer {get_access_token()}"
        }

        res = req.delete(f"{getenv('BASE_URL')}/article/{article_id}", headers=headers)

        return {**res.json(), 'ok': res.ok}
    except Exception as e:
        error_handler(e)
        return None


def update_article(article_id: str,
                   title: str = None,
                   body: str = None,
                   cover: str = None):
    try:
        headers = {
            "Authorization": f"Bearer {get_access_token()}"
        }

        res = req.put(f"{getenv('BASE_URL')}/article/{article_id}", headers=headers)

        return res.json()
    except Exception as e:
        error_handler(e)
        return None


def change_article_status(article_id: str):
    try:
        headers = {
            "Authorization": f"Bearer {get_access_token()}"
        }

        res = req.put(f"{getenv('BASE_URL')}/article/status/{article_id}", headers=headers)

        return {**res.json(), 'ok': res.ok}
    except Exception as e:
        error_handler(e)
        return None

def search_in_articles(q: str = ""):
    try:
        headers = {
            "Authorization": f"Bearer {get_access_token()}"
        }

        res = req.get(f"{getenv('BASE_URL')}/article/search?q={q}", headers=headers)

        return res.json()
    except Exception as e:
        error_handler(e)
        return None


def get_favorite_articles():
    try:
        headers = {
            "Authorization": f"Bearer {get_access_token()}"
        }

        res = req.get(f"{getenv('BASE_URL')}/favorite/article", headers=headers)

        return res.json()
    except Exception as e:
        error_handler(e)
        return None


def create_favorite_article(article_id: str):
    try:
        headers = {
            "Authorization": f"Bearer {get_access_token()}"
        }

        res = req.post(f"{getenv('BASE_URL')}/favorite/article", json={"article": article_id}, headers=headers)

        return res.json()
    except Exception as e:
        error_handler(e)
        return None


def delete_favorite_article(article_id: str):
    try:
        headers = {
            "Authorization": f"Bearer {get_access_token()}"
        }

        res = req.delete(f"{getenv('BASE_URL')}/favorite/article", json={"article": article_id}, headers=headers)

        return res.json()
    except Exception as e:
        error_handler(e)
