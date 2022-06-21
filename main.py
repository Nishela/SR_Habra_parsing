import queue
from urllib.parse import urlparse, urljoin

from my_task import MyTask
from soup import SoupBuilder


class HabraParser:
    def __init__(self, start_url, delay=1):
        self.start_url = start_url
        self.delay = delay
        self.start_url_netloc = urlparse(self.start_url).netloc
        self.my_queue = queue.Queue()
        self.my_queue.put(self.get_task(self.start_url))

    def start(self):
        while not self.my_queue.empty():
            task = self.my_queue.get()
            all_urls = task()
            for url in all_urls:
                full_url = urljoin(self.start_url, url)
                if self.start_url_netloc == urlparse(full_url).netloc:
                    self.my_queue.put(self.get_task(full_url))

    @staticmethod
    def get_task(url):
        # TODO: сделать выбор модели по url
        return MyTask(url, soup_builder)


if __name__ == '__main__':
    soup_builder = SoupBuilder()
    parser = HabraParser('https://habr.com/ru/all/')
    parser.start()
