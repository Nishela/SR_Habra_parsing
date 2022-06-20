import bs4
import requests


from decorators import deco_status_code, deco_delay


class SoupBuilder:
    # TODO: добавить кеш юрлов

    @deco_delay(delay=1)
    @deco_status_code(expected_code=200)
    def get_response(self, url):
        response = requests.get(url)
        return response

    def get_soup(self, response):
        soup = bs4.BeautifulSoup(self.get_response(response).text, 'lxml')
        return soup

    def __call__(self, url):
        response = self.get_response(url)
        soup = self.get_soup(response)
