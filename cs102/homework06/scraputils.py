from time import sleep

import requests
from bs4 import BeautifulSoup

from random import choice


def extract_news(parser):
    """ Extract news from a given web page """
    news_list = []
    cmt_list = parser.findAll('td', {'class': 'subtext'})
    pnt_list = parser.findAll('span', {'class': 'score'})
    ttl_list = parser.findAll('a', {'class': 'storylink'})
    ath_list = parser.findAll('a', {'class': 'hnuser'})
    print(len(ath_list), 'done')
    for i in range(len(pnt_list)):
        lst = cmt_list[i].find_all('a')[-1].text.split()
        lst2 = pnt_list[i].text.split()
        k = {'author': ath_list[i].text, 'comments': lst[0], 'points': lst2[0], 'title': ttl_list[i].text,
             'url': ttl_list[i]['href']}
        news_list.append(k)
    return news_list


def extract_next_page(parser):
    """ Extract next page URL """
    return parser.find('a', {'class': 'morelink'})['href']


def get_news(url, n_pages=1, stop = 0):
    """ Collect news from a given web page """
    useragents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36']
        # proxies = ['200.73.128.198:3128', '51.255.198.111:9999', '151.253.165.70:8080', '139.99.105.186:80',
        #        '51.255.198.111:8080', '51.15.166.107:3128', '163.172.109.132:65420', '43.245.216.69:53281',
        #        '80.187.140.26:8080', '118.97.100.83:35220', '5.8.203.76:48026', '195.138.73.54:44610',
        #        '51.38.71.101:8080', '51.255.198.111:8080', '103.251.225.13:34052', '36.89.65.253:36486',
        #        '103.68.18.118:8080', '54.38.110.35:47640', '51.255.198.111:9999', '46.235.53.26:3128',
        #        '82.200.233.4:3128', '177.22.225.237:3128', '189.10.3.186:3128', '191.37.49.226:3128',
        #        '81.31.230.72:8080', '188.120.232.181:8118', '195.154.255.110:8118', '139.99.105.186:80',
        #        '51.15.166.107:3128', '139.59.59.63:8080', '176.9.119.170:8080', '139.59.99.234:8080']

    news = []
    i = 0
    while n_pages > stop:
        print('страница: ', n_pages)
        # proxy = {'http': 'http://' + proxies[i]}
        # i = (i + 1) % len(proxies)
        useragent = {'User-Agent': choice(useragents)}
        response = requests.get(url, headers=useragent, proxies = None)
        soup = BeautifulSoup(response.text, "html.parser")
        news_list = extract_news(soup)
        next_page = extract_next_page(soup)
        print(next_page)
        url = 'https://news.ycombinator.com/' + next_page
        news.extend(news_list)
        n_pages -= 1
        x = choice([7, 8, 9, 10])
        sleep(x)
        print(n_pages)
    return news, url
