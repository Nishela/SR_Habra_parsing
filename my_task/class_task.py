from dataclasses import dataclass
from typing import Any

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

    @staticmethod
    def get_all_links(soup):
        all_links = set(soup.find_all('a'))
        links = all_links.difference(soup.url_cache)
        return links

    def __call__(self):
        soup = self.run()
        return self.get_all_links(soup)
