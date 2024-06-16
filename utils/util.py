import redis
from os import getenv


def error_handler(*err):
    print("<==ERROR HANDLER START==>")
    print(err)
    print("<==ERROR HANDLER END==>")


def connect_to_redis_db():
    """
    This function tries to connect to redis database using credentials in .env file
    :return: Database Sample
    """
    try:
        return redis.Redis(host=getenv('REDIS_HOST'), port=getenv('REDIS_PORT'), db=0)
    except Exception as e:
        error_handler(e, 'connect_to_redis_db')
        return None


def save_to_db(key: str, value: any, expiration_time: int = 0):
    """
    This function gets key:value data and saves it to redis database
    :param key: key of the pair
    :param value: value of the pair
    :param expiration_time: expiration time in hours, default is 0
    :return: None
    """
    r = connect_to_redis_db()
    try:
        if expiration_time:
            r.set(key, value, ex=expiration_time*360)
        else:
            r.set(key, value)
    except Exception as e:
        error_handler(e, 'save_to_db')


def get_from_db(key: str):
    """
    This function gets key of the target pair and return its value
    :param key: key of the pair
    :return: value of the pair
    """
    r = connect_to_redis_db()
    try:
        value = r.get(key)
        if value:
            return value
        else:
            return ""
    except Exception as e:
        error_handler(e, 'get_from_db')
        return None


def delete_from_db(key: str):
    """
    This function would get key of the target pair and delete the value from the redis database
    :param key: target pair's key
    :return: None
    """
    r = connect_to_redis_db()
    try:
        r.delete(key)
    except Exception as e:
        error_handler(e, 'delete_from_db')


def save_access_token(access_token: str):
    """
    This function gets access_token and saves it to redis database
    :param access_token: access token received from backend
    :return: None
    """
    save_to_db('access_token', access_token, 48)


def get_access_token():
    """
    This function return stored access token in redis database
    :return: user access token
    """
    try:
        return get_from_db('access_token').decode('utf-8')
    except Exception as e:
        return ""


def log_out():
    """
    This function would delete the access token from redis db
    :return: None
    """
    try:
        delete_from_db('access_token')
    except Exception as e:
        error_handler(e, 'log_out')


def is_admin():
    try:
        from api_services.auth import get_me
        user = get_me()['user']

        return True if user['role'] == 'ADMIN' else False
    except Exception as e:
        error_handler(e, 'is_admin')
        return None
