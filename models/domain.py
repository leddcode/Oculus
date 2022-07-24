import random

from models.mixins.bucket import Bucket
from models.mixins.colour import Colour
from models.mixins.config import Config
from models.mixins.dir import Dir
from models.mixins.emails import Email
from models.mixins.env import Env
from models.mixins.mx import Mx
from models.mixins.request import Request
from models.mixins.sub import Sub
from models.mixins.writer import Writer


class Domain(
    Bucket,
    Colour,
    Config,
    Dir,
    Email,
    Env,
    Mx,
    Request,
    Sub,
    Writer
):

    def __init__(self):
        self.threads = 15
        self.count_requests = 0
        self.name = None
        self.protocol = None
        self.option = None
        self.search_type = None
        self.executor = '1337'
        self.parts = []
        self.futures = []
        self.permutations = []
        self.cert_subdomains = []
        self.response_length_list = []
        self.headers = self.__get_headers()
        super().__init__()

    def set_name(self, url):
        self.name = self.__check_url(url)
        if self.name:
            return self.__set_parts()

    def set_search_option(self, option):
        if option in self.OPTIONS.keys():
            self.option = option
            self.search_type = self.OPTIONS[option]
        return self.search_type

    def set_threads(self, threads):
        if threads:
            self.__apply_threads(threads)

    def stop_executor(self):
        try:
            self.executor.shutdown(wait=False, cancel_futures=True)
            # self.executor._threads.clear()
            self.executor = '1337'
            [f.cancel() for f in self.futures]
        except Exception:
            print(f'\n\n\n')

    def __set_parts(self):
        self.parts = self.name.split('.')
        if len(self.parts) > 1:
            return True

    def __get_user_agent(self):
        user_agents = open('utils/user_agents.txt').read().splitlines()
        return random.choice(user_agents)

    def __get_headers(self):
        ua = self.__get_user_agent()
        return {'User-Agent': ua}

    def __apply_threads(self, threads):
        try:
            threads = int(threads)
            if threads > 0:
                self.threads = threads
        except Exception:
            print('\n <- Bad input. Continue with default value.')

    def __connect_via_HTTP(self, url):
        try:
            res = self._request(f'http://{url}')
            if res.status_code not in (400, 404):
                self.protocol = 'http'
                print(
                    f' ==> {self.GREEN}HTTP{self.WHITE}')
                return url
            else:
                ''' <- Bad Domain?!'''
        except Exception:
            print(f' ==> {self.RED}HTTP{self.WHITE}')
            ''' <- Bad Domain?!'''

    def __normalize_url(self, url):
        url = url.strip()
        if url.startswith('https://') or url.startswith('http://'):
            url = url[url.find('//') + 2:]
        if url.endswith('/'):
            url = url[:-1]
        return url

    def __check_url(self, url):
        url = self.__normalize_url(url)
        print(' <| Checking host connection', end='')
        try:
            res = self._request(f'https://{url}')
            if res.status_code not in (400, 404):
                self.protocol = 'https'
                print(
                    f' ==> {self.GREEN}HTTPS{self.WHITE}')
                return url
            else:
                print(' <- Bad Domain?!')
        except Exception:
            print(f' ==> {self.RED} HTTPS{self.WHITE}', end='')
            return self.__connect_via_HTTP(url)

    def search(self):
        try:
            if self.option == 1:
                self._search_envs()
            elif self.option == 2:
                self._search_dirs()
            elif self.option == 3:
                self._search_subs()
            elif self.option == 4:
                self._search_emails()
            elif self.option in (5, 6, 7):
                self._cloud_enum()
        except Exception as e:
            print('Oops...', e)
        finally:
            print()
