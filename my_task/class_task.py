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
            self.model.parse(soup)
        return soup

    # @staticmethod
    def get_all_links(self, soup):
        all_links = {self._filter_links(item.attrs.get('href')) for item in soup.find_all('a')}
        links = all_links.difference(soup.url_cache)
        return links

    # @staticmethod
    def _filter_links(self, link):
        domain = urlparse(self.url).netloc
        full_link = urljoin(self.url, link)
        if domain == urlparse(full_link).netloc:
            return full_link

    def __call__(self):
        soup = self.run()
        return self.get_all_links(soup)
