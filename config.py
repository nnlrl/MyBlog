import os


class AttrDict(dict):

    def __init__(self, *args, **kwargs) -> None:
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self


BLOG_URL = 'https://example.com'
REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379')
