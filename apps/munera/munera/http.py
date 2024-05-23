from logboek.propagators import TraceContextPropegator
from requests import Response
from requests import Session as BaseSession
from requests.adapters import HTTPAdapter


MAX_RETRIES = 2
REQUEST_TIMEOUT = 5
USER_AGENT = "Munera/1.0.0"


class Session(BaseSession):
    def __init__(self, base_url: str):
        super().__init__()

        self._base_url = base_url
        self._propegator = TraceContextPropegator()

        self.headers["User-Agent"] = USER_AGENT

        self.mount("https://", HTTPAdapter(max_retries=MAX_RETRIES))
        self.mount("http://", HTTPAdapter(max_retries=MAX_RETRIES))

    def request(self, method: str, url: str, *args, **kwargs) -> Response:
        url = f"{self._base_url}{url}"
        kwargs.setdefault("timeout", REQUEST_TIMEOUT)

        headers = {}
        self._propegator.inject(headers)

        return super().request(method, url, headers=headers, *args, **kwargs)


def create_http_client(base_url: str = "") -> Session:
    return Session(base_url)
