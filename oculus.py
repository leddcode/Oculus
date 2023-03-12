# -*- coding: utf-8 -*-
"""
Be easy and interactive ;)

@author: leddcode
"""
import random

import requests

from models.domain import Domain
from utils import strings

if __name__ == '__main__':
    domain = Domain()
    print(random.choice(strings.banners)) 

    try:
        res = requests.get(
            'https://raw.githubusercontent.com/leddcode/Oculus/main/utils/strings.py', timeout=3)

        if strings.version not in res.text:
            print(f"{domain.p_info('INFO')} You are running an outdated version.")
    except:
        pass

    try:
        while not domain.name:
            url = input(f"{domain.p_warn('INIT')} Target  >_ ")
            if not domain.set_name(url):
                print(f"{domain.p_fail('FAIL')} Check the domain name and try again (Ex. google.com)")

        while not domain.chosen_options:
            print(strings.search_types)
            options = input('       Run              ::  ')
            chosen_options = domain.set_search_option(options)
            if not domain.chosen_options:
                print('       The chosen option does not exist.')
                print('       Multiple options should be separated by commas.')
                print('       Ex: 3,1,5')

        if [t for t in domain.chosen_options if t not in domain.TESTS_WITHOUT_THREADS]:
            threads = input('       Threads          ::  ')
            domain.set_threads(threads)
            lengths = input('       Exclude lengths  ::  ')
            domain.set_excluded_length(lengths)
            domain.status_bar = input('       Status Bar (y/N) ::  ')

        print(f'       Request Timeout  ::  {domain.TIMEOUT}')
        print(f'       Protocol         ::  {domain.protocol}')
        print(f'       User-Agent       ::  {domain.headers["User-Agent"]}')
        domain.search()

    except KeyboardInterrupt:
        domain.stop_executor()
        print('       Bye Bye ;)')
