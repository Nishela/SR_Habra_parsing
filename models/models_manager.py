import re

from .author_model import AuthorPage
from .post_model import PostPage

__all__ = (
    'ModelsManager',
)


class ModelsManager:
    _available_models = {
        'post': PostPage,
        'users': AuthorPage,
    }

    @classmethod
    def get_model(cls, url):
        if data_type := re.findall(r'post(?=/\d+/$)|users(?=/\S+/$)', url):
            return cls._available_models.get(data_type[0])
        return
