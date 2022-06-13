# -*- coding: utf-8 -*-

import urllib.request
import re
import requests


user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36"
headers={'User-Agent':user_agent}


def analyse_page(page, word):
    # проверяем на корректность и доступность ссылки"
    try:
        page = 'http://' + page
        # читаем текст на странице
        urllib.request.urlopen(page)
        request=urllib.request.Request(page, None, headers)
        response = urllib.request.urlopen(request)
        data = response.read().decode('UTF-8')
        # считаем количество упоминаний искомого слова в тексте
        word_counts = len(re.findall(word, data))
        return word_counts
    except ValueError:
        return None
    except urllib.error.HTTPError:
        return None
    except urllib.error.URLError:
        return None

        
def analyse_link(link, word):
    headers={'User-Agent':user_agent} 
    # проверяем на корректность и доступность ссылки"
    try:
        # читаем текст на странице
        urllib.request.urlopen(link)
        request=urllib.request.Request(link, None, headers)
        response = urllib.request.urlopen(request)
        data = response.read().decode('UTF-8')
        # считаем количество упоминаний искомого слова в тексте
        word_counts = len(re.findall(word, data))
        return word_counts
    except ValueError:
        return None
    except urllib.error.HTTPError:
        return None
    except urllib.error.URLError:
        return None


def main(word): 
    # загружаем по API с сайта Роскомсвободы реестр запрещенной информации (данные на сайте обновляются каждые три часа)
    req = requests.get('https://reestr.rublacklist.net/api/v2/current/csv')
    data = req.content.decode() 
    data_lines = []
    for row in data.splitlines():
         # cоздаем список списков в виде [['ip', 'page', 'link', 'gos_organ', 'postanovlenie', 'date'], [...], [...], ...]
        data_lines.append(row.rsplit(sep=',', maxsplit=5))
    # создает словарь с ключом "page" и значением "количество упоминаний слова на странице"
    result_pages = {}
    # создает словарь с ключом "link" и значением "количество упоминаний слова по ссылке"
    result_links = {}
    for row in data_lines:
        result_pages[row[1]] = analyse_page(row[1], word)
        result_links[row[2]] = analyse_page(row[2], word)
    return result_pages, result_links


if __name__ == '__main__':
    main("война") # в качестве аргумента искомое слово