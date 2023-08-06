from threading import Lock
from urllib3.exceptions import InsecureRequestWarning

import requests

requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)


class Request:
    LOCK = Lock()

    def _request(self, url):
        return requests.get(url, headers=self.headers, timeout=self.TIMEOUT, verify=False, allow_redirects=False)

    def _make_request(self, url, total=None):
        self.count_requests += 1
        try:
            res = self._request(url)
            length = str(len(res.text))
            if res.status_code not in self.BAD_CODES and length not in self.excluded_lengths:
                status = self.colour_status(res.status_code)
                if length not in self.response_length_list:
                    self.response_length_list.append(length)
                    status = ''

                if self.option == 5 and 'x-amz-bucket-region' in res.headers:
                    status = res.headers['x-amz-bucket-region']
                elif self.option == 7 and res.status_code > 401:
                    return

                self._write(url, f'{res.status_code}{status}')
                self.LOCK.acquire()
                print(
                    f'{self.CLEAR}       {self.colour_code(res.status_code, status)}C:{res.status_code}   L:{length:<10}  {url}{self.WHITE}'
                )
                self.LOCK.release()
        except KeyboardInterrupt:
            self.stop_executor()
        except Exception:
            '''Bad Request'''

        if self.status_bar in ('y', 'Y', 'yes', 'Yes', 'go', 'sure', 'wtf'):
            pr = str(round(self.count_requests * 100 / total, 1)) + '%'
            self.LOCK.acquire()
            print(f'{self.p_warn("SENT")} {pr:<8}R:{self.count_requests}', end='\r')
            self.LOCK.release()

    def _check_futures(self):
        for f in self.futures:
            f.result()
