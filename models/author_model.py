from urllib.parse import urljoin

from config import AUTHOR_INFO_DIR

class AuthorPage:
    @classmethod
    def parse(cls, domain_url, soup) -> tuple:
        name = soup.find('span', {'class': 'tm-user-card__name tm-user-card__name'}).text
        # return file_name, title, author_name, author_url, content

    @staticmethod
    def _get_author_info(domain_url, soup) -> tuple:
        name = soup.find('span', {'class': 'tm-user-card__name tm-user-card__name'}).text
        other_info = soup.find('a', {'class': 'tm-user-card__nickname'})
        nickname = other_info.text.strip(),
        url = urljoin(domain_url, other_info.attrs.get('href'))

        # return name, author_url

    @staticmethod
    def _filename_generator(author_name, title):
        return f'{AUTHOR_INFO_DIR}/{author_name} - {title}.txt'
