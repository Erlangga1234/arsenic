import base64
from typing import Dict, TypeVar, Union, Optional

import attr


TDefault = TypeVar('TDefault')


def lowercase_dict(data: Dict[str, str]) -> Dict[str, str]:
    return {key.lower(): value for key, value in data.items()}


@attr.s
class Headers:
    data: Dict[str, str] = attr.ib(convert=lowercase_dict, default=attr.Factory(dict))

    def get(self, key: str, default: TDefault=None) -> Union[str, TDefault]:
        return self.data.get(key.lower(), default)


@attr.s
class Request:
    method: str = attr.ib()
    url: str = attr.ib()
    headers: Dict[str, str] = attr.ib(default=attr.Factory(lambda: {}))
    body: Optional[bytes] = attr.ib(default=None)


@attr.s
class Response:
    status: int = attr.ib()
    body: bytes = attr.ib()
    headers: Headers = attr.ib()


@attr.s
class Engine:
    http_session= attr.ib()
    start_process = attr.ib()
    sleep = attr.ib()


@attr.s
class BasicAuth:
    username = attr.ib()
    password = attr.ib()

    def get_headers(self):
        raw_token = f'{self.username}:{self.password}'
        token = base64.b64encode(raw_token.encode('ascii')).decode('ascii')
        return {
            'Authorization': f'Basic {token}'
        }
