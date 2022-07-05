# Задача 2
# В нашей школе мы не можем разглашать персональные данные пользователей, но чтобы преподаватель и ученик
# смогли объяснить нашей поддержке, кого они имеют в виду (у преподавателей, например, часто учится несколько Саш),
# мы генерируем пользователям уникальные и легко произносимые имена. Имя у нас состоит из прилагательного,
# имени животного и двузначной цифры. В итоге получается, например, "Перламутровый лосось 77". Для генерации таких
# имен мы и решали следующую задачу: Получить с русской википедии список всех животных (https://inlnk.ru/jElywR) и
# вывести количество животных на каждую букву алфавита.
# Результат должен получиться в следующем виде: А: 642 Б: 412  В:....

import sys
import requests
import time
from bs4 import BeautifulSoup
from multiprocessing import Process, Manager


def connection():
    url = 'https://ru.wikipedia.org/wiki/Категория:Животные_по_алфавиту'
    try:
        page = requests.get(url).text
    except:
        sys.stdout.write('\b' * 16)  # cleans 'Please, wait...' message from the screen
        print('Что-то пошло не так. Пожалуйста, проверьте подключение и повторите попытку.')
        return
    return page


# Функция, которая захватывает все необходимые ссылки со страницы
def list_of_urls(page):
    soup = BeautifulSoup(page, 'html.parser')
    if not soup:
        return
    try:
        urls = soup.find('div', id='mw-pages').find_all('a')
    except AttributeError:
        sys.stdout.write('\b' * 16)
        print('Предоставленная вами ссылка неверна.')
        return
    return urls


# Функция, которая специально получает URL-адрес следующей страницы и список URL-адресов, представляющих животных.
def new_url_and_animals(urls):
    if urls:
        url = 'https://ru.wikipedia.org/' + urls[-1].get('href')
        return url, urls


def main(dictionary):
    page = connection()
    if not page:
        return
    elif not new_url_and_animals(list_of_urls(page)):
        return
    while True:
        url, animals = new_url_and_animals(list_of_urls(page))
        for animal in animals:
            if animal.text[0] == 'A':
                return dictionary  # условие - остановиться, когда мы доберемся до английского алфавита
            else:
                if animal.text != 'Предыдущая страница' and animal.text != 'Следующая страница':
                    if animal.text[0] in dictionary.keys():  # условие, чтобы избежать ошибок вики, таких как английские первые буквы
                        dictionary[animal.text[0]] += 1
        page = requests.get(url).text


def printing_dictionary(d: dict):
    sys.stdout.write('\b' * 17)
    for key, value in d.items():
        print(f'{key}: {value}')


# Функция, представляющая процесс загрузки во время работы основной основной функции
def progress_line():
    for counter in range(4):
        if counter == 4 or counter == 0:
            sys.stdout.write('Идет загрузка')
        time.sleep(0.3)
        sys.stdout.write('.')
        counter += 1
        if counter == 4:
            sys.stdout.write('\b' * 16)


if __name__ == '__main__':
    manager = Manager()
    dictionary = manager.dict({a: 0 for a in [chr(ord("А") + m) for m in range(32)]})
    process = Process(target=main, args=(dictionary,))
    process.start()
    while process.is_alive():
        progress_line()
    if any(dictionary.values()):  # чтобы не печатать пустой словарь, если что-то пошло не так.
        printing_dictionary(dictionary)
