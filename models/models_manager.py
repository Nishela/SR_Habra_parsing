import re

from .post_model import PostPage
from .author_model import AuthorPage

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

    # @property
    # def availavle_models(self):
    #     return self._available_models
