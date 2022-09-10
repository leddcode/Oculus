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
    print(random.choice(strings.banners), strings.solid_line)

    print(' <| Checking the version...')

    try:
        res = requests.get(
            'https://raw.githubusercontent.com/leddcode/Oculus/main/utils/strings.py')

        if strings.version not in res.text:
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

        while not domain.chosen_options:
            print(strings.search_types)
            options = input('    Run      >_')
            chosen_options = domain.set_search_option(options)
            if not domain.chosen_options:
                print("\n <- The chosen option does not exist.")
                print('    Multiple options should be separated by commas.')
                print('    Ex: 3,1,5')

        threads = input('\n    Threads  >_')
        domain.set_threads(threads)

        print(f'\n    Request Timeout  ::  {domain.TIMEOUT}')
        print(f'    Protocol         ::  {domain.protocol}')
        print(f'    User-Agent       ::  {domain.headers["User-Agent"]}\n\n')
        domain.search()

    except KeyboardInterrupt:
        domain.stop_executor()
        print(' <| Bye Bye ;)')
