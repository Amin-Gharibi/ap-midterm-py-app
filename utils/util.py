import redis
from os import getenv


def format_description(description: str):
    """
    This function gets the whole description and each 100 chars it appends an \n
    :param description: str
    :return: str
    """
    result = ''
    for index, char in enumerate(description):
        if index > 300:
            break
        result += char
        if not (index + 1) % 30:
            result += '\n'

    return result


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
            r.set(key, value, ex=expiration_time*60)
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
            raise Exception("Key not found in db!")
    except Exception as e:
        error_handler(e, 'get_from_db')
        return None


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
    return get_from_db('access_token').decode('utf-8')
