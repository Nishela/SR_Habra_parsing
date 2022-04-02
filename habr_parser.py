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
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.3 Safari/605.1.15',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    }

    def __init__(self, main_page_url='https://habr.com/ru/all/', tag='a', attr_name='class',
                 attr_value='tm-article-snippet__title-link'):
        self.main_page_url = main_page_url
        self.tag = tag
        self.attr_name = attr_name
        self.attr_value = attr_value

    def get_response(self, post_url=''):
        url = self.main_page_url if not post_url else post_url
        try:
            response = requests.get(url, headers=self.headers)
            if response.status_code in range(200, 227):
                return response
        except Exception as err:
            print('Вот что я поймал -->', err)

    def get_soup(self, url=''):
        response = self.get_response(url)
        try:
            soup = bs4.BeautifulSoup(response.text, 'lxml')
            return soup
        except AttributeError:
            print('Response == None!')

    def get_post_link(self, soup):
        if soup:
            all_posts_links = (post.attrs.get('href', '') for post in
                               soup.find_all(self.tag, {self.attr_name: self.attr_value}))
            for link in all_posts_links:
                yield link

    def get_post_data(self, post_link):
        post_url_full = urljoin(self.main_page_url, post_link)
        response = self.get_response(post_url_full)
        return response

    @staticmethod
    def save_html(response):
        alias = response.url.strip('/').split('/')[-1]
        with open(f'{POSTS_DIR}/post_{alias}.html', 'wb') as file:
            file.write(response.content)

    def run(self):
        soup = self.get_soup()
        for post_link in self.get_post_link(soup):
            response = self.get_post_data(post_link)
            self.save_html(response)


if __name__ == '__main__':
    parser = HabrParser()
    parser.run()
    print('finish!')
