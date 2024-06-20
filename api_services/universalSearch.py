import requests as req
from os import getenv
from utils.util import error_handler


def universal_search(q: str):
    try:
        res = req.get(f"{getenv('BASE_URL')}/universalSearch?q={q}")

        return res.json()
    except Exception as e:
        return error_handler(e)
