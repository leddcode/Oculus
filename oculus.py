# -*- coding: utf-8 -*-
"""
Be easy and interactive ;)

@author: leddcode
"""

import requests

from models.domain import Domain
from utils import strings

if __name__ == '__main__':
    domain = Domain()
    print(strings.banner_speed)
    print(strings.solid_line)

    print(' <| Checking the version...')

    try:
        res = requests.get(
            'https://raw.githubusercontent.com/leddcode/Oculus/main/utils/strings.py')

        if strings.banner_speed not in res.text:
            print(Domain.RED, '<| New version available!')
            print(
                f" <| Run {Domain.PURPLE}'git pull' {Domain.RED}command to update{Domain.WHITE}\n")
        else:
            print(
                f"{Domain.GREEN} <| You are running the latest version{Domain.WHITE}\n")
    except Exception:
        print(' <- Version checks failed')

    try:
        while not domain.name:
            url = input(' <: Domain name: ')
            if not domain.set_name(url):
                print(' <- Check the Domain Name and try again (Ex. google.com)')

        while not domain.search_type:
            print(strings.search_types)
            option = input('    Run      >_')
            search_type = domain.set_search_option(int(option))
            if not domain.search_type:
                print('\n <- The option does not exist.')

        threads = input('    Threads  >_')
        domain.set_threads(threads)

        print(f'\n    Request Timeout  ::  {domain.TIMEOUT}')
        print(f'    Protocol         ::  {domain.protocol}')
        print(f'    User-Agent       ::  {domain.headers["User-Agent"]}\n\n')
        domain.search()

    except KeyboardInterrupt:
        domain.stop_executor()
        print(' <| Bye Bye ;)')
