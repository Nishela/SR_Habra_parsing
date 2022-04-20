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
