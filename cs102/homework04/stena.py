import pandas as pd
import pymorphy2
import requests
import config
import string
#from gensim.corpora.dictionary import Dictionary
from gensim.corpora import Dictionary
from gensim.models import LdaModel
from pandas.io.json import json_normalize


def get_wall(
        owner_id: str = '',
        domain: str = '',
        offset: int = 0,
        count: int = 10,
        filter: str = 'all',
        extended: int = 0,
        fields: str = '',
        v: str = '5.103'
) -> pd.DataFrame:
    """
    Возвращает список записей со стены пользователя или сообщества.

    @see: https://vk.com/dev/wall.get

    :param owner_id: Идентификатор пользователя или сообщества, со стены которого необходимо получить записи.
    :param domain: Короткий адрес пользователя или сообщества.
    :param offset: Смещение, необходимое для выборки определенного подмножества записей.
    :param count: Количество записей, которое необходимо получить (0 - все записи).
    :param filter: Определяет, какие типы записей на стене необходимо получить.
    :param extended: 1 — в ответе будут возвращены дополнительные поля profiles и groups, содержащие информацию о пользователях и сообществах.
    :param fields: Список дополнительных полей для профилей и сообществ, которые необходимо вернуть.
    :param v: Версия API.
    """
    code = """return API.wall.get({
        "owner_id": "%s",
        "domain": "%s",
        "offset": "%d",
        "count": "%d",
        "filter": "%s",
        "extended": "%d",
        "fields": "%s",
        "v": "%d"
    });""" % (owner_id, domain, offset, count, filter, extended, fields, v)

    response = requests.post(
        url="https://api.vk.com/method/execute",
        data={
            "code": code,
            "access_token": config.VK_CONFIG['access_token'],
            "v": "5.103"
        }
    )
    return response.json()['response']['items']

def analiz(domain = 'itmostudents', count = 10):
    morph = pymorphy2.MorphAnalyzer()
    wall = get_wall(
        owner_id='',
        domain = domain,
        offset=0,
        count=count,
        filter="owner",
        extended=0,
        fields="")
    morphed_post = []
    for post in wall:
        morphed_post = []
        if post == None:
            continue
        post.translate(str.maketrans('', '', string.punctuation))
        for word in post['text'].split():
            word = morph.parse(str(word))
            morphed_post.append(word.normalized)
        morphed_post.append(morphed_post)
    common_dictionary = Dictionary(morphed_post)
    common_corpus = [common_dictionary.doc2bow(text) for text in morphed_post]
    lda = LdaModel(common_corpus, num_topics=15)

print(analiz('feelinc', 0))