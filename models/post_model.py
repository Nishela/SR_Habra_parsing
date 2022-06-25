from urllib.parse import urljoin

from config import POSTS_DIR


class PostPage:

    @classmethod
    def parse(cls, domain_url, soup, *args) -> tuple:
        title = soup.find('h1', {'class': 'tm-article-snippet__title tm-article-snippet__title_h1'}).text
        author_name, author_url = cls._get_author_info(domain_url, soup)
        content = '\n'.join(line.text.strip() for line in soup.find_all('p'))
        file_name = cls._filename_generator(author_name, title)
        return file_name, title, author_name, author_url, content

    @staticmethod
    def _get_author_info(domain_url, soup) -> tuple:
        author_info = soup.find('a', {'class': 'tm-user-info__username'})
        name = author_info.text.strip()
        author_url = urljoin(domain_url, author_info.attrs.get('href'))
        return name, author_url

    @staticmethod
    def _filename_generator(author_name, title):
        return f'{POSTS_DIR}/{author_name} - {title}.txt'
