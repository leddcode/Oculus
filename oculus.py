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
        print(f"{domain.p_info('INFO')} User-Agent set to {domain.GREEN}{domain.headers['User-Agent']}{domain.WHITE}")
        print(f"{domain.p_info('INFO')} Cookies auto update is {domain.GREEN}ON{domain.WHITE}")

        to_turn_off = input(f"\n{domain.p_warn('INIT')} Turn off cookies auto update? (y/N) >_ ")
        if to_turn_off and to_turn_off.strip().lower() in ('y', 'yes'):
            domain.auto_update['cookies'] = False
            print(f"{domain.p_info('INFO')} Cookies auto update is {domain.RED}OFF{domain.WHITE}\n")

        to_show = input(f"{domain.p_warn('INIT')} Show possible false positives? (Y/n) >_ ")
        if to_show and to_show.strip().lower() in ('n', 'no', 'not'):
            domain.to_show_false_positives = False
            print(f"{domain.p_info('INFO')} Printing possible false positives is {domain.RED}OFF{domain.WHITE}\n")

        to_set_headers = input(f"{domain.p_warn('INIT')} Do you want to set headers?   (y/N) >_ ")
        if to_set_headers and to_set_headers.strip().lower() in ('y', 'yes'):
            while True:
                print(f"{domain.p_warn('INIT')} Add a request header or leave blank (Ex. Content-Type:application/json)")
                header = input(f"{domain.p_warn('INIT')} Header  >_ ")
                if header:
                    try:
                        k, v = header.split(":", maxsplit=1)
                        domain.set_headers(k.strip(), v.strip())
                    except:
                        print(f"{domain.p_fail('FAIL')} Bad header!")
                else:
                    break

        print(f"\n{domain.p_info('INFO')} Headers")
        for k, v in domain.headers.items():
            print(f"       {domain.GREEN}{k}{domain.WHITE}: {v}")
        if domain.cookies:
            print(f"\n{domain.p_info('INFO')} Cookies")
            for k, v in domain.cookies.items():
                print(f"       {domain.GREEN}{k}{domain.WHITE}: {v}")

        while not domain.name:
            url = input(f"\n{domain.p_warn('INIT')} Target  >_ ")
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
        domain.search()

    except KeyboardInterrupt:
        domain.stop_executor()
        print('       Bye Bye ;)')
