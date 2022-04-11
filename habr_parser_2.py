# TODO: зайти на хабр, найти все внутренние ссылки.
# TODO: Перейти на эти страницы и повторить действие 1.
# TODO: Применить модуль queue
# TODO: сделать универсальный декоратор, который бы делал delay
# TODO: Нужен декоратор ожидаемых статус кодов
# TODO: Нужен некоторый класс. Таск должен быть коллабл класс, в котором будут реализованы методы.
# TODO: Если статья - создать текстовый документ в котором заголовок статьи, юрл, имя автора, ссылка на автора, и текст статьи (чистый, без тегов).
# TODO: Если страница автора - создать ТД в котором будет ссылка на автора, его имя, список заголовков его статьи.

import requests

import bs4

from urllib.parse import urlparse, urljoin


class HabraParser:
    def __init__(self, start_url, delay=1):
        self.start_url = start_url
        self.main_domain = urlparse(self.start_url).netloc
        self.delay = delay
        self.done_urls = set()
        self.tasks = []
        self.tasks.append(self.get_task(self.start_url, self.get_all_links))

    def start(self):
        while self.tasks:
            task = self.tasks.pop(0)
            data = task()
            print(1)

    def get_task(self, url, callback):
        def task():
            return callback(url)

        return task

    def get_response(self, url):
        response = requests.get(url)
        self.done_urls.add(url)
        return response

    def get_soup(self, url):
        soup = bs4.BeautifulSoup(self.get_response(url).text, 'lxml')
        return soup

    def get_all_links(self, url):
        soup = self.get_soup(url)
        all_links = soup.find_all('a')
        links = self.get_hrefs(all_links)
        for link in links:
            if link not in self.done_urls:
                self.tasks.append(self.get_task(link, self.get_all_links))

    def get_hrefs(self, all_links):
        hrefs = {self.href_cleaner(link.attrs.get('href', None)) for link in all_links}
        return hrefs

    def href_cleaner(self, href):
        result = urljoin(self.start_url, href)
        if self.main_domain == urlparse(result).netloc:
            return result


if __name__ == '__main__':
    parser = HabraParser('https://habr.com/ru/all/')
    parser.start()
