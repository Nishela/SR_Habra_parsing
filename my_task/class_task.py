from dataclasses import dataclass
from typing import Any
from urllib.parse import urlparse, urljoin

from soup import SoupBuilder


@dataclass
class MyTask:
    url: str
    soup_builder: SoupBuilder
    model: Any = None

    def run(self):
        soup = self.soup_builder(self.url)
        if self.model:
            parsed_data = self.model.parse(self.url, soup)
            self.save(parsed_data)
        return soup

    def get_all_links(self, soup):
        all_links = {self._filter_links(item.attrs.get('href')) for item in soup.find_all('a')}
        links = all_links.difference(self.soup_builder.url_cache)
        return links

    def _filter_links(self, link):
        domain = urlparse(self.url).netloc
        full_link = urljoin(self.url, link)
        if domain == urlparse(full_link).netloc:
            return full_link

    @staticmethod
    def save(data):
        filename, *args = data
        with open(filename, 'w', encoding='utf-8') as file:
            for itm in args:
                file.write(itm)

    def __call__(self):
        soup = self.run()
        return self.get_all_links(soup)
