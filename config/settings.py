import os

__all__ = (
    'BASE_DIR',
    'POSTS_DIR',
    'AUTHOR_INFO_DIR',
)

BASE_DIR = os.path.abspath(os.curdir)
POSTS_DIR = os.path.join(BASE_DIR, 'posts_content')
AUTHOR_INFO_DIR = os.path.join(BASE_DIR, 'author_content')
