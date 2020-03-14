import pandas as pd
import requests
from time import sleep
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import config


def get(url, params={}, timeout=5, max_retries=5, backoff_factor=0.3):
    """ Выполнить GET-запрос
    :param url: адрес, на который необходимо выполнить запрос
    :param params: параметры запроса
    :param timeout: максимальное время ожидания ответа от сервера
    :param max_retries: максимальное число повторных запросов
    :param backoff_factor: коэффициент экспоненциального нарастания задержки
    """
    delay = 0.3
    for _ in range(max_retries):
        try:
            response = requests.get(url=url, params=params, timeout=timeout)
        except:
            sleep(delay)
            delay += backoff_factor * delay
        if response:
            return response


def get_friends(user_id, fields=''):
    """ Вернуть данных о друзьях пользователя
    :param user_id: идентификатор пользователя, список друзей которого нужно получить
    :param fields: список полей, которые нужно получить для каждого пользователя
    """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert isinstance(fields, str), "fields must be string"
    assert user_id > 0, "user_id must be positive integer"
    domain = config.VK_CONFIG['domain']
    access_token = config.VK_CONFIG['access_token']
    version = config.VK_CONFIG['version']

    response = get(f"{domain}/friends.get?access_token={access_token}&user_id={user_id}&fields={fields}&v={version}")
    return response
