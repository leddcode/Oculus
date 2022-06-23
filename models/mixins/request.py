from threading import Lock

import requests


class Request:
    LOCK = Lock()

    def _make_request(self, url):
        self.count_requests += 1

        try:
            res = requests.get(
                url,
                headers=self.headers,
                timeout=self.TIMEOUT)
            if res.status_code not in self.BAD_CODES:
                status = self.colour_status(res.status_code)
                length = len(res.text)
                if length not in self.response_length_list:
                    self.response_length_list.append(length)
                    status = '' * 20
                self.LOCK.acquire()
                print(
                    self.colour_code(res.status_code, status),
                    f'<+  {res.status_code}  {length:<12}  {url:<50}  {status}',
                    self.WHITE
                )
                self.LOCK.release()
        except Exception:
            '''Bad Request'''

        progress = round(self.count_requests / len(self.futures) * 40) * '█'
        self.LOCK.acquire()
        print(
            f'\r {self.YELLOW}<|  {progress:<40}  ::  {len(self.futures)} | {self.count_requests}{self.WHITE}',
            ' ' * 30,
            end='\r'
        )
        self.LOCK.release()
