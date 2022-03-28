import os

import requests
import bs4
from urllib.parse import urljoin

# TODO: написать красиво парсер, который запрашивает главную страницу.
#  Берет все статьи с главной, ходит по ним и для каждой статьи создает html документ.
#  Имя документа - alias страницы.


BASE_DIR = os.path.abspath(os.curdir)
POSTS_DIR = os.path.join(BASE_DIR, 'posts')


class HabrParser:
    def __init__(self, main_page_url='https://habr.com/ru/all/', tag='a', attr_name='class',
                 attr_value='tm-article-snippet__title-link'):
        self.main_page_url = main_page_url
        self.tag = tag
        self.attr_name = attr_name
        self.attr_value = attr_value

    def send_request(self, url=''):
        if not url:
            url = self.main_page_url
        return requests.get(url)

    def get_post_link(self, response):
        soup = bs4.BeautifulSoup(response.text, 'lxml')
        all_posts_links = (post.attrs.get('href', '') for post in
                           soup.find_all(self.tag, {self.attr_name: self.attr_value}))
        for link in all_posts_links:
            yield link

    def get_post_page_data(self, post_link):
        post_url_full = urljoin(self.main_page_url, post_link)
        response = self.send_request(post_url_full)
        return response

    @staticmethod
    def save_html(response):
        alias = response.url.strip('/').split('/')[-1]
        with open(f'{POSTS_DIR}/post_{alias}.html', 'wb') as file:
            file.write(response.content)

    def run(self):
        resp = self.send_request()
        for link in self.get_post_link(resp):
            response = self.get_post_page_data(link)
            self.save_html(response)


if __name__ == '__main__':
    parser = HabrParser()
    parser.run()
