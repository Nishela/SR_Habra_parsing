import queue
from urllib.parse import urlparse

from models import ModelsManager
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
                if url:
                    self.my_queue.put(self.get_task(url))

    @staticmethod
    def get_task(url):
        model = ModelsManager.get_model(url)
        return MyTask(url, soup_builder, model)


if __name__ == '__main__':
    soup_builder = SoupBuilder()
    parser = HabraParser('https://habr.com/ru/all/')
    parser.start()
