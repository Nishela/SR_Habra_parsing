import os

import requests
import bs4
import re

from urllib.parse import urljoin, urlparse

from decorators import deco_status_code, deco_delay

BASE_DIR = os.path.abspath(os.curdir)
POSTS_DIR = os.path.join(BASE_DIR, 'posts_content')
AUTHOR_INFO_DIR = os.path.join(BASE_DIR, 'author_content')


class PostPage:
    def __init__(self, url, soup):
        self.url = url
        self.soup = soup

    def get_info(self):
        title = self.soup.find('h1', {'class': 'tm-article-snippet__title'}).text
        author_info = self.soup.find('a', {'class': 'tm-user-info__username'})
        author_name = author_info.text.strip()
        author_link = urljoin(self.url, author_info.attrs.get('href', ''))
        content = self.soup.find_all('p')
        return title, author_name, author_link, content

    def save_info(self):
        title, author_name, author_link, content = self.get_info()
        with open(f'{POSTS_DIR}/{author_name} - {title}.txt', 'w', encoding='utf-8') as file:
            file.write(f'{title}\n{author_name}\n{author_link}\n')
            for line in content:
                file.write(f'{line.text}\n')


class AuthorPage:
    def __init__(self, url, soup):
        self.url = url
        self.soup = soup

    def get_info(self):
        author_info = self.soup.find('div', {'class': 'tm-user-card__title tm-user-card__title'})
        childrens = author_info.findChildren(['span', 'a'])
        author_name = childrens[0].text
        author_link = childrens[1].attrs.get('href', '')
        full_author_link = urljoin(self.url, author_link)
        return author_name, full_author_link

    def save_info(self):
        author_name, author_link = self.get_info()
        all_posts_titles = self.get_posts_list()
        with open(f'{AUTHOR_INFO_DIR}/{author_name}.txt', 'w', encoding='utf-8') as file:
            file.write(f'{author_name}\n{author_link}\n\n')
            for title in all_posts_titles:
                file.write(f'{title}\n')

    def get_posts_href(self):
        posts_info = self.soup.find_all('a', {'class': 'tm-tabs__tab-link'})
        posts_href = (item.get('href', '') for item in posts_info if item.contents[0].strip() == 'Публикации')
        full_url = urljoin(self.url, *posts_href)
        return full_url

    def get_soup(self):
        new_soup = Chief(self.get_posts_href())()
        return new_soup

    def get_posts_list(self):
        posts_soup = self.get_soup()
        all_posts = posts_soup.find_all('a', {'class': 'tm-article-snippet__title-link'})
        all_posts_titles = [post.text for post in all_posts]
        return all_posts_titles


class MyTask:
    done_urls = set()

    def __init__(self, url, main_domain, delay):
        self.url = url
        self.main_domain = main_domain
        self.delay = delay
        self.soup = None

    def __call__(self):
        all_links = self.get_all_links()
        self.check_url()
        return all_links

    def get_hrefs(self, all_links):
        hrefs = {self.href_cleaner(link.attrs.get('href', '')) for link in all_links}
        return hrefs

    def href_cleaner(self, href):
        result = urljoin(self.url, href)
        if self.main_domain == urlparse(result).netloc:
            return result

    def get_all_links(self):
        self.soup = Chief(self.url)()
        all_links = self.soup.find_all('a')
        links = [link for link in self.get_hrefs(all_links) if link not in self.done_urls]
        return links

    def check_url(self):
        if re.findall(r'/post/\d+/$', self.url):
            PostPage(self.url, self.soup).save_info()
        elif re.findall(r'/users/\S+/$', self.url):
            AuthorPage(self.url, self.soup).save_info()


class Chief:
    def __init__(self, url):
        self.url = url

    @deco_delay(delay=1)
    def get_response(self):
        response = requests.get(self.url)
        return response

    def get_soup(self):
        soup = bs4.BeautifulSoup(self.get_response().text, 'lxml')
        return soup

    def __call__(self, *args, **kwargs):
        return self.get_soup()
