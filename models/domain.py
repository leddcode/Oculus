from concurrent.futures import ThreadPoolExecutor

import requests

from utils import strings


class Domain:
    OPTIONS = {
        '1': 'environments',
        '2': 'directories',
        '3': 'subdomains'
    }

    BAD_CODES = (400, 404, 500, 501, 502, 503, 504)

    def __init__(self):
        self.threads = 15
        self.timeout = 4
        self.count_requests = 0
        self.default_env_list_path = 'wordlists/env_wordlist.txt'
        self.default_dir_list_path = 'wordlists/dir_wordlist.txt'
        self.default_sub_list_path = 'wordlists/sub_wordlist.txt'
        self.name = ''
        self.search_type = ''
        self.executor = '1337'
        self.parts = []
        self.futures = []
        self.permutations = []
        self.response_length_list = []

    def set_name(self, url):
        self.name = self.__check_url(url)
        if self.name:
            return self.__set_parts()

    def set_search_option(self, option):
        if option in self.OPTIONS.keys():
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

    def __apply_threads(self, threads):
        try:
            threads = int(threads)
            if threads > 0:
                self.threads = threads
        except Exception:
            print('\n <- Bad input. Continue with default value.')

    def __check_url(self, url):
        url = url.strip()
        try:
            res = requests.get(f'https://{url}', timeout=self.timeout)
            if res.status_code not in (400, 404):
                return url
        except Exception:
            print(' <- Bad Domain!')

    def __set_parts(self):
        self.parts = self.name.split('.')
        if len(self.parts) > 1:
            return True

    def __add_permutations(self, i, word, part, parts):
        for char in ('-', '_', '.', ''):
            parts[i] = f'{word}{char}{part}'
            self.permutations.append('https://' + '.'.join(parts))
            parts[i] = f'{part}{char}{word}'
            self.permutations.append('https://' + '.'.join(parts))

    def __permutate_env_urls(self):
        with open(self.default_env_list_path, 'r') as wl:
            words = wl.read()
            for w in words.splitlines():
                parts = self.parts[:]
                for i in range(len(self.parts) - 1):
                    part = parts[i]
                    self.__add_permutations(i, w, part, parts)
                    parts = self.parts[:]

    def __make_request(self, url):
        self.count_requests += 1
        res = requests.get(url, timeout=self.timeout)
        if res.status_code not in self.BAD_CODES:
            status = strings.Helper.status(res.status_code)
            length = len(res.text)
            if length not in self.response_length_list:
                self.response_length_list.append(length)
                status = '' * 20
            print(
                strings.Helper.colour(res.status_code, status),
                f' <+  {res.status_code}  {length:<12}  {url:<50}  {status}',
                strings.Helper.WHITE
            )

        progress = round(self.count_requests / len(self.futures) * 40) * '█'
        print(
            strings.Helper.YELLOW,
            f' <|  {progress:<40}  ::  {len(self.futures)} | {self.count_requests}',
            strings.Helper.WHITE,
            end='\r'
        )

    def __create_env_pool(self,):
        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            self.executor = executor
            for url in self.permutations:
                self.futures.append(
                    self.executor.submit(self.__make_request, url))

    def __create_dir_pool(self):
        with open(self.default_dir_list_path, 'r') as wl:
            with ThreadPoolExecutor(max_workers=self.threads) as executor:
                self.executor = executor
                words = wl.read().splitlines()
                for w in words:
                    self.futures.append(self.executor.submit(
                        self.__make_request, f'https://{self.name}/{w}'))

    def __create_sub_pool(self):
        with open(self.default_sub_list_path, 'r') as wl:
            with ThreadPoolExecutor(max_workers=self.threads) as executor:
                self.executor = executor
                words = wl.read().splitlines()
                for w in words:
                    self.futures.append(self.executor.submit(
                        self.__make_request, f'https://{w}.{self.name}'))

    def __search_envs(self):
        print(' <| Creating possible urls')
        self.__permutate_env_urls()

        print(f' <| Searching for {self.search_type}\n')
        self.__create_env_pool()

    def __search_dirs(self):
        print(f' <| Searching for {self.search_type}\n')
        self.__create_dir_pool()

    def __search_subs(self):
        print(f' <| Searching for {self.search_type}\n')
        self.__create_sub_pool()

    def search(self):
        print(strings.solid_line)
        try:
            if self.search_type == 'environments':
                self.__search_envs()
            elif self.search_type == 'directories':
                self.__search_dirs()
            elif self.search_type == 'subdomains':
                self.__search_subs()
        except Exception as e:
            print('Oops...', e)
