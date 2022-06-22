import bs4
import requests

from decorators import deco_status_code, deco_delay


class SoupBuilder:
    def __init__(self):
        self.url_cache = set()

    @deco_delay(delay=1)
    @deco_status_code(expected_code=200)
    def get_response(self, url):
        response = requests.get(url)
        self.url_cache.add(url)
        return response

    @staticmethod
    def get_soup(response):
        soup = bs4.BeautifulSoup(response.text, 'lxml')
        return soup

    def __call__(self, url):
        response = self.get_response(url)
        soup = self.get_soup(response)
        return soup
