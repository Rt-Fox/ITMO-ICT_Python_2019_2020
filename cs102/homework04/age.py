import datetime
from statistics import median
from typing import Optional

from api import get_friends
#from api_models import User


def age_predict(user_id: int) -> Optional[float]:
    """ Наивный прогноз возраста по возрасту друзей
    Возраст считается как медиана среди возраста всех друзей пользователя
    :param user_id: идентификатор пользователя
    :return: медианный возраст пользователя
    """
    link = get_friends(user_id, 'bdate')
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert user_id > 0, "user_id must be positive integer"
    arr = []
    try:
        for i in link.json()['response']['items']:
            try:
                born = i['bdate'].split('.')
                if len(born) != 3:
                    continue
                new = datetime.datetime.today()
                year = new.year
                month = new.month
                day = new.year
                age = int(year) - int(born[2])
                if (int(born[1]) > month) or (born[1] == month and born[0] > day):
                    age -= 1
                arr.append(age)
            except:
                pass
        if len(arr):
            return median(arr)
        else:
            return None
    except:
        return "Не получилось получить json"
print(age_predict(171494699))

