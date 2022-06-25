import logging
import os
from typing import ClassVar

from pydantic import BaseSettings, Field

__all__ = (
    'BASE_DIR',
    'POSTS_DIR',
    'AUTHOR_INFO_DIR',
    'my_logger'
)


class LoggerSettings(BaseSettings):
    format: str = Field('%(asctime)s - %(name)s.%(funcName)s - %(levelname)s - %(message)s')
    datefmt: str = Field('%Y-%m-%d %H:%M:%S')
    level: int = Field(logging.INFO)
    handlers: ClassVar = Field(default_factory=logging.StreamHandler)


BASE_DIR = os.path.abspath(os.curdir)
POSTS_DIR = os.path.join(BASE_DIR, 'posts_content')
AUTHOR_INFO_DIR = os.path.join(BASE_DIR, 'author_content')

LOGGER_SETTINGS = LoggerSettings().dict()
logging.basicConfig(**LOGGER_SETTINGS)
my_logger = logging.getLogger('my_logger')
