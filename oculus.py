import sys

from models.domain import Domain
from utils import strings

if __name__ == '__main__':
    domain = Domain()
    search_type = None
    print(strings.banner_speed)
    print(strings.solid_line)

    try:

        while not domain.name:
            url = input(' <: Domain name: ')
            if not domain.set_name(url):
                print(' <x Check the domain URL and try again.')

        while not search_type:
            print(strings.search_types)
            option = input('    Option   _')
            search_type = domain.set_search_option(option)
            if not search_type:
                print(' <x The option does not exist.')

        threads = input('    Threads  _')
        domain.set_threads(threads)
        domain.search()

    except KeyboardInterrupt:
        domain.stop_executor()
        print(' <| Bye Bye ;)')
