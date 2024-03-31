import time

import requests

from custom_exception import MyException


class CustomRequest:
    def __init__(self):
        self.sess = requests.Session()
        headers = {
            'Content-type': 'text/html;charset=UTF-8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0',
        }
        self.sess.headers.update(headers)

    def get(self, request_url: str) -> requests.Response:
        return self._do_request(request_url)

    def _do_request(self, request_url: str) -> requests.Response:
        try_count = 0
        while try_count < 5:
            some_result = self.sess.get(request_url)
            if some_result.status_code == 200:
                return some_result
            try_count += 1
            time.sleep(2)
        raise MyException()
