from collections import namedtuple
from urllib.parse import urljoin

from config import AUTHOR_INFO_DIR


class AuthorPage:
    @classmethod
    def parse(cls, domain_url, soup, soup_builder) -> tuple:
        author_info = cls._get_author_info(domain_url, soup)
        file_name = cls._filename_generator(author_info.name, author_info.nickname)
        author_posts_urls = cls.get_author_posts(author_info.url, soup, soup_builder)
        return file_name, *author_info, author_posts_urls

    @staticmethod
    def _get_author_info(domain_url, soup) -> namedtuple:
        name = soup.find('span', {'class': 'tm-user-card__name tm-user-card__name'})
        name = name.text if name else 'No name'
        other_info = soup.find('a', {'class': 'tm-user-card__nickname'})
        nickname = other_info.text.strip(),
        url = urljoin(domain_url, other_info.attrs.get('href'))
        return namedtuple('Author', 'name nickname url')(name, *nickname, url)

    @staticmethod
    def get_author_posts(author_page_url, soup, soup_builder):
        all_a_objects = soup.find_all('a', {'class': 'tm-tabs__tab-link'})
        posts_link = (item.attrs.get('href', '') for item in all_a_objects if item.contents[0].strip() == 'Публикации')
        full_url = urljoin(author_page_url, *posts_link)
        posts_soup = soup_builder(full_url)
        posts_info = posts_soup.find_all('a', {'class': 'tm-article-snippet__title-link'})
        posts_urls = (item.attrs.get('href') for item in posts_info)
        result = '\n'.join(urljoin(author_page_url, url) for url in posts_urls)
        return result

    @staticmethod
    def _filename_generator(author_name, title):
        return f'{AUTHOR_INFO_DIR}/{author_name} - {title}.txt'
