import requests as req
from os import getenv
from utils.util import save_access_token, get_access_token, error_handler


def register(email: str,
             username: str,
             password: str,
             role: str):
    try:
        sending_data = {key: value for key, value in locals().items()}

        res = req.post(f'{getenv('BASE_URL')}/auth/register', json=sending_data)

        return {"message": res.json()['message'] or 'Something Went Wrong!'}
    except Exception as e:
        error_handler(e)


def validate_register_otp(email: str,
                          username: str,
                          password: str,
                          role: str,
                          code: str):
    try:
        sending_data = {key: value for key, value in locals().items()}

        res = req.post(f'{getenv('BASE_URL')}/auth/register/otp', json=sending_data)

        if res.status_code == 201:
            save_access_token(res.json()['accessToken'])

        return {"message": res.json()['message'] or 'Something Went Wrong!'}
    except Exception as e:
        error_handler(e)


def login(identifier: str, password: str):
    try:
        sending_data = {key: value for key, value in locals().items()}

        res = req.post(f'{getenv('BASE_URL')}/auth/login', json=sending_data)

        return {"message": res.json()['message'] or 'Something Went Wrong!', "ok": res.ok}
    except Exception as e:
        error_handler(e)
        return False


def validate_login_otp(identifier: str, password: str, code: str):
    try:
        sending_data = {key: value for key, value in locals().items()}

        res = req.post(f'{getenv('BASE_URL')}/auth/login/otp', json=sending_data)

        if res.status_code == 200:
            save_access_token(res.json()['accessToken'])

        return {"message": res.json()['message'] or 'Something Went Wrong!', "ok": res.ok}
    except Exception as e:
        error_handler(e)


def get_me():
    try:
        headers = {
            'Authorization': f'Bearer {get_access_token()}'
        }
        res = req.get(f'{getenv('BASE_URL')}/auth/me', headers=headers)
        if res.status_code != 200:
            return False
        return res.json()
    except Exception as e:
        error_handler(e)
        return False
