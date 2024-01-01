import random
import sys

from concurrent.futures import FIRST_COMPLETED, wait

from models.mixins.bucket import Bucket
from models.mixins.colour import Colour
from models.mixins.config import Config
from models.mixins.dir import Dir
from models.mixins.emails import Email
from models.mixins.env import Env
from models.mixins.mx import Mx
from models.mixins.request import Request
from models.mixins.scan import Scan
from models.mixins.shodaner import Shodaner
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
    Scan,
    Shodaner,
    Sub,
    Writer
):

    def __init__(self):
        self.port = 443
        self.threads = 15
        self.ports_open = 0
        self.count_requests = 0
        self.name = None
        self.option = None
        self.protocol = None
        self.status_bar = None
        self.search_type = None
        self.executor = '1337'
        self.parts = []
        self.futures = []
        self.keywords = []
        self.extensions = []
        self.permutations = []
        self.chosen_options = []
        self.cert_subdomains = []
        self.excluded_lengths = []
        self.response_length_list = []
        self.cookies = {}
        self.headers = {'User-Agent': self.__get_user_agent()}
        self.auto_update = {
            'cookies': True
        }
        super().__init__()

    def set_name(self, url):
        self.name = self.__check_url(url)
        if self.name:
            return self.__set_parts()

    def __get_additional_lookup_parameters(self):
        if 2 in self.chosen_options:
            print(
                f'       {self.YELLOW}Enter file extensions separated with comma, or leave blank (Ex: php,aspx){self.WHITE}')
            extensions = input('       Extensions       ::  ')
            if extensions:
                self.extensions = [ext.strip()
                                   for ext in extensions.split(",")]
        if any(opt in (5, 6, 7, 8) for opt in self.chosen_options):
            print(
                f'       {self.YELLOW}Enter additional keywords separated with comma, or leave blank (Ex: word1,word2,word3){self.WHITE}')
            keywords = input('       Keywords         ::  ')
            if keywords:
                self.keywords = [k.strip() for k in keywords.split(",")]

    def __is_existing_option(self, option: str):
        if option.strip().isnumeric() and int(option) in self.OPTIONS.keys():
            return True

    def set_search_option(self, options):
        chosen_options = [
            int(o.strip()) for o in options.split(',') if self.__is_existing_option(o)]
        if chosen_options:
            self.chosen_options = chosen_options
            
        self.__get_additional_lookup_parameters()
        return self.chosen_options

    def set_threads(self, threads):
        if threads:
            self.__apply_threads(threads)

    def set_excluded_length(self, lengths):
        if lengths:
            try:
                self.excluded_lengths = [l.strip()
                                         for l in lengths.split(',') if l]
            except Exception:
                pass

    def stop_executor(self):
        try:
            self.executor.shutdown(wait=False, cancel_futures=True)
            # self.executor._threads.clear()
            self.executor = '1337'
            [f.cancel() for f in self.futures]
            sys.exit()
        except Exception:
            '''Crash'''
            sys.exit()

    def __set_parts(self):
        self.parts = self.name.split('.')
        if len(self.parts) > 1:
            return True

    def __get_user_agent(self):
        user_agents = open(self.USER_AGENTS_LIST).read().splitlines()
        return random.choice(user_agents)

    def __set_cookie(self, cookie):
        try:
            c_key, c_value = cookie.split("=", maxsplit=1)
            self.cookies[c_key.strip()] = c_value.strip()
        except:
            pass

    def set_headers(self, h_key, h_value):
        if h_key.lower() == 'cookie':
            cookies = h_value.split(';')
            for c in cookies:
                self.__set_cookie(c)
        else:
            self.headers[h_key] = h_value

    def __apply_threads(self, threads):
        try:
            threads = int(threads)
            if threads > 0:
                self.threads = threads
        except Exception:
            print(f'       Default Threads  ::  {self.threads}')

    def __connect_via_HTTP(self, url):
        try:
            res = self._request(f'http://{url}')
            if res.status_code not in (400, 404):
                self.protocol = 'http'
                self.port = 80
                print(f'{self.GREEN}[HTTP]{self.WHITE}')
                return url
        except Exception:
            print(f'{self.RED}[HTTP]{self.WHITE}')
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
        print(f"{self.p_cyan('PROC')} Connecting ", end='')
        try:
            res = self._request(f'https://{url}')
            if res.status_code not in (400, 404):
                self.protocol = 'https'
                print(f'{self.GREEN}[HTTPS]{self.WHITE}')
                return url
            else:
                print('       Bad Domain?!')
        except Exception:
            print(f'{self.RED}[HTTPS]{self.WHITE}', end='')
            return self.__connect_via_HTTP(url)

    def search(self):
        for opt in self.chosen_options:
            self.option = opt
            self.search_type = self.OPTIONS[opt]
            try:
                if opt == 1:
                    self._search_envs()
                elif opt == 2:
                    self._search_dirs()
                elif opt == 3:
                    self._search_subs()
                elif opt == 4:
                    self._search_emails()
                elif opt in (5, 6, 7, 8):
                    self._cloud_enum()
                elif opt == 9:
                    self._scan(f'{self.protocol}://{self.name}/')
                while self.futures:
                    done, self.futures = wait(
                        self.futures, return_when=FIRST_COMPLETED)
            except KeyboardInterrupt:
                self.stop_executor()
            except Exception as e:
                print(f'{self.CLEAR}{self.p_fail("OOPS")} {e}')
            finally:
                self.futures = []
                self.permutations = []
                self.response_length_list = []
                self.count_requests = 0
                print('\n\n')
