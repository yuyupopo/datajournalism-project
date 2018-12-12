import os

from christmas.common.util import colored


class TokenMeta(type):
    def __getitem__(cls, val):
        return cls.__tokens__[val]


class OpenAPIToken(object, metaclass=TokenMeta):

    __tokens__ = {}

    @classmethod
    def add_token(cls, token_name, alias=None):
        token = os.getenv(token_name, None)
        if token is None:
            err_msg = 'Token {} is not defined as environmnet variable'.format(
                token_name)
            print(colored(err_msg))

        if not alias:
            alias = token_name

        if alias in cls.__tokens__:
            raise AttributeError('{} already exists'.format(alias))

        cls.__tokens__[alias] = token

        return OpenAPIToken

