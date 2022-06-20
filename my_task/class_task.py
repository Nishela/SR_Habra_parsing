from .base_task import BaseTask
from soup import SoupBuilder
from models import AuthorPage, PostPage


class MyTask:

    @classmethod
    def run(cls, url: str, soup_builder: SoupBuilder, model: AuthorPage | PostPage):
        soup = soup_builder(url)
        model.parse(soup)

