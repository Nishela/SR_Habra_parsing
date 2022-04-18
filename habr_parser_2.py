# TODO: зайти на хабр, найти все внутренние ссылки.
# TODO: Перейти на эти страницы и повторить действие 1.
# TODO: Применить модуль queue
# TODO: сделать универсальный декоратор, который бы делал delay
# TODO: Нужен декоратор ожидаемых статус кодов
# TODO: Нужен некоторый класс. Таск должен быть коллабл класс, в котором будут реализованы методы.
# TODO: Если статья - создать текстовый документ в котором заголовок статьи, юрл, имя автора, ссылка на автора, и текст статьи (чистый, без тегов).
# TODO: Если страница автора - создать ТД в котором будет ссылка на автора, его имя, список заголовков его статьи.

import queue

from urllib.parse import urlparse

from class_task import MyTask


class HabraParser:
    def __init__(self, start_url, delay=1):
        self.start_url = start_url
        self.delay = delay
        self.main_domain = urlparse(self.start_url).netloc
        self.my_queue = queue.Queue()
        self.my_queue.put(self.get_task(self.start_url))

    def start(self):
        while not self.my_queue.empty():
            task = self.my_queue.get()
            all_urls = task()
            for url in all_urls:
                self.my_queue.put(self.get_task(url))

    def get_task(self, url):
        return MyTask(url, self.main_domain, self.delay)


if __name__ == '__main__':
    parser = HabraParser('https://habr.com/ru/all/')
    parser.start()
