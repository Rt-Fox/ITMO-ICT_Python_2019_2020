import requests
import telebot
import datetime
from telebot import apihelper
from bs4 import BeautifulSoup
import config

bot = telebot.TeleBot(config.access_token)
# apihelper.proxy = config.proxy

days = ['/monday', '/tuesday', '/wednesday', '/thursday', '/friday', '/saturday', '/sunday']
Xday = ['1day', '2day', '3day', '4day', '5day', '6day', '7day']
wrong = 'Ошибка, повторите запрос правильно.'
wrong2 = 'Ошибка, повторите запрос, проверив номер группы и четность недели. (формат /monday %(0-2) X1111) {ps 0 чет и нечет, 1 чет, 2 нечет}'
wrong3 = 'Ошибка, повторите запрос, проверив номер группы. (формат /near X1111)'
wrong4 = 'Ошибка, повторите запрос, проверив номер группы. (формат /tommorow X1111)'
wrong5 = 'Ошибка, повторите запрос, проверив номер группы. (формат /all X1111)'
cache = dict()  # кэш


def get_page(group: str, week):
    if abs(int(week)) > 2:
        return 0
    if f'{group}_{week}' in cache.keys():
        web_page = cache[f'{group}_{week}']
    else:
        if week:
            week = str(week) + '/'
        url = '{domain}/{group}/{week}raspisanie_zanyatiy_{group}.htm'.format(
            domain=config.domain,
            week=week,
            group=group)
        response = requests.get(url)
        web_page = response.text
        if 'Расписание не найдено' in web_page:
            return None
        else:
            cache[f'{group}_{week}'] = web_page
    return web_page


def parse_schedule(web_page, day):
    soup = BeautifulSoup(web_page, "html5lib")

    # Получаем таблицу с расписанием на понедельник
    schedule_table = soup.find("table", attrs={"id": day})
    if schedule_table is None:
        return None

    # Время проведения занятий
    times_list = schedule_table.find_all("td", attrs={"class": "time"})
    times_list = [time.span.text for time in times_list]

    # Место проведения занятий
    locations_list = schedule_table.find_all("td", attrs={"class": "room"})
    locations_list = [room.span.text for room in locations_list]

    # Название дисциплин и имена преподавателей
    lessons_list = schedule_table.find_all("td", attrs={"class": "lesson"})
    lessons_list = [lesson.text.split('\n\n') for lesson in lessons_list]
    lessons_list = [', '.join([info for info in lesson_info if info]) for lesson_info in lessons_list]

    return times_list, locations_list, lessons_list


def get_parity(day: datetime.date) -> int:
    """ Возвратить четность недели для данной даты """
    first_day = datetime.date(datetime.date.today().year, 9, 1)
    if day.month < 9:
        first_day = datetime.date(datetime.date.today().year - 1, 9, 1)
    if first_day.weekday() == 6:
        # если 1 сентября приходится на воскресенье, первым днем считается 2 сентября
        first_day = datetime.date(datetime.date.today().year, 9, 2)
    else:
        while first_day.weekday() != 0:
            # нахождение понедельника недели, содержащей 1 сентября
            first_day.day = first_day.day - 1
    dataa = day - first_day
    return -1 * ((dataa.days // 7) % 2 - 2)


@bot.message_handler(commands=['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'])
def get_schedule(message, week=0):
    """ Получить расписание на указанный день """
    if 2 <= len(message.text.split()) <= 3:
        if len(message.text.split()) == 3:
            # указанна дата, и интересующая неделя
            day, week, group = message.text.split()
            uuu = days.index(day)
            group = group.capitalize()
            web_page = get_page(group, week)
        else:
            # без учета четности
            day, group = message.text.split()
            uuu = days.index(day)
            web_page = get_page(group, week)
        if web_page:
            schedule = parse_schedule(web_page, Xday[uuu])
            if schedule:
                times_lst, locations_lst, lessons_lst = schedule
                resp = ''
                for time, location, lesson in zip(times_lst, locations_lst, lessons_lst):
                    resp += '<b>{}</b>, {}, {}\n'.format(time, location, lesson)
                bot.send_message(message.chat.id, resp, parse_mode='HTML')
            else:
                bot.send_message(message.chat.id, 'В этот день, пар нет!', parse_mode='HTML')
        else:
            bot.send_message(message.chat.id, wrong2, parse_mode='HTML')
    else:
        bot.send_message(message.chat.id, wrong, parse_mode='HTML')


@bot.message_handler(commands=['near'])
def get_near_lesson(message):
    """ Получить ближайшее занятие """
    if len(message.text.split()) != 2:
        bot.send_message(message.chat.id, wrong3, parse_mode='HTML')
        return None
    _, group = message.text.split()
    day = datetime.datetime.today().date()
    times = datetime.datetime.today().time()
    week = get_parity(day)
    uuu = datetime.datetime.today().weekday()
    hour = times.hour
    minute = times.minute
    if uuu == 6:  # в воскресенье нет ни у кого пар
        uuu = 0
    flag = False
    web_page = get_page(group, week)
    if not (web_page):
        bot.send_message(message.chat.id, wrong3, parse_mode='HTML')
        return None
    schedule = parse_schedule(web_page, Xday[uuu])
    # проверяются пары на день
    if schedule:
        times_lst, locations_lst, lessons_lst = schedule
        for time, location, lesson in zip(times_lst, locations_lst, lessons_lst):
            if hour < int(time[6:8]) or (hour == int(time[6:8]) and minute < int(time[9:11])):
                # если текущее время меньше времени конца пары, выводится эта пара
                resp = 'Ближайшая пара:\n\n<b>Cегодня</b>\n\n'
                resp += '<b>{}</b>, {}, {}\n'.format(time, location, lesson)
                flag = True
                break
    if flag == True:
        bot.send_message(message.chat.id, resp, parse_mode='HTML')
    else:
        uuu = (uuu + 1)
        schedule = parse_schedule(web_page, Xday[uuu])
        while schedule == None:
            if (uuu < 5):
                uuu += uuu
                schedule = parse_schedule(web_page, Xday[uuu])
            else:
                uuu = 0
                week = -(week - 3)
                web_page = get_page(group, week)
                schedule = parse_schedule(web_page, Xday[uuu])
        resp = 'Ближайшая пара: '
        times_lst, locations_lst, lessons_lst = schedule
        for time, location, lession in zip(times_lst, locations_lst, lessons_lst):
            resp += '<b>{}</b>, {}, {}\n'.format(time, location, lession)
            bot.send_message(message.chat.id, resp, parse_mode='HTML')
            break


@bot.message_handler(commands=['tommorow'])
def get_tommorow(message):
    if len(message.text.split()) != 2:
        bot.send_message(message.chat.id, wrong, parse_mode='HTML')
        return None
    """ Получить расписание на следующий день """
    _, group = message.text.split()
    uuu = datetime.datetime.today().weekday()
    week = get_parity(datetime.date.today())
    # меняется четность недели
    if uuu == 6:
        week = -(week - 3)
        uuu = 0
    else:
        uuu = uuu + 1
    Xday = ['1day', '2day', '3day', '4day', '5day', '6day', '7day']
    web_page = get_page(group, week)
    if web_page:
        schedule = parse_schedule(web_page, Xday[uuu])
        if schedule:
            times_lst, locations_lst, lessons_lst = schedule
            resp = ''
            for time, location, lession in zip(times_lst, locations_lst, lessons_lst):
                resp += '<b>{}</b>, {}, {}\n'.format(time, location, lession)
            bot.send_message(message.chat.id, resp, parse_mode='HTML')
        else:
            bot.send_message(message.chat.id, 'В этот день, пар нет!', parse_mode='HTML')
    else:
        bot.send_message(message.chat.id, wrong4, parse_mode='HTML')


@bot.message_handler(commands=['all'])
def get_all_schedule(message):
    """ Получить расписание на всю нынешнюю неделю для указанной группы """
    if len(message.text.split()) != 2:
        bot.send_message(message.chat.id, wrong, parse_mode='HTML')
        return None
    _, group = message.text.split()
    week = get_parity(datetime.date.today())
    web_page = get_page(group, week)
    for i in Xday:

        if web_page:
            schedule = parse_schedule(web_page, i)
            if schedule:
                times_lst, locations_lst, lessons_lst = schedule
                resp = '{} \n'.format(days[Xday.index(i)])
                for time, location, lession in zip(times_lst, locations_lst, lessons_lst):
                    resp += '<b>{}</b>, {}, {}\n'.format(time, location, lession)
                bot.send_message(message.chat.id, resp, parse_mode='HTML')
            else:
                bot.send_message(message.chat.id, '{} \n В этот день, пар нет!'.format(days[Xday.index(i)]),
                                 parse_mode='HTML')
        else:
            bot.send_message(message.chat.id, wrong5, parse_mode='HTML')
            break


if __name__ == '__main__':
    bot.polling(none_stop=True)
