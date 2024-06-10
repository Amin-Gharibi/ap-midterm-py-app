import requests as req
from os import getenv
from utils.util import save_access_token, get_access_token


def register(email: str,
             username: str,
             password: str,
             role: str):

    sending_data = {key: value for key, value in locals().items()}

    res = req.post(f'{getenv('BASE_URL')}/auth/register', json=sending_data)

    return {"message": res.json()['message'] or 'Something Went Wrong!'}


def validate_register_otp(email: str,
                          username: str,
                          password: str,
                          role: str,
                          code: str):

    sending_data = {key: value for key, value in locals().items()}

    res = req.post(f'{getenv('BASE_URL')}/auth/register/otp', json=sending_data)

    if res.status_code == 201:
        save_access_token(res.json()['accessToken'])

    return {"message": res.json()['message'] or 'Something Went Wrong!'}


def login(identifier: str, password: str):
    sending_data = {key: value for key, value in locals().items()}

    res = req.post(f'{getenv('BASE_URL')}/auth/login', json=sending_data)

    return {"message": res.json()['message'] or 'Something Went Wrong!'}


def validate_login_otp(identifier: str, password: str, code: str):
    sending_data = {key: value for key, value in locals().items()}

    res = req.post(f'{getenv('BASE_URL')}/auth/login/otp', json=sending_data)

    if res.status_code == 200:
        save_access_token(res.json()['accessToken'])

    return {"message": res.json()['message'] or 'Something Went Wrong!'}


def get_me():
    return {"message": "this function will be filled later"}
