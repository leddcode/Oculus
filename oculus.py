import requests

from models.domain import Domain
from utils import strings

if __name__ == '__main__':
    domain = Domain()
    search_type = None
    print(strings.banner_speed)
    print(strings.solid_line)

    print(' <| Checking the version...')

    res = requests.get(
        'https://raw.githubusercontent.com/enotr0n/Oculus/main/utils/strings.py')

    if strings.banner_speed not in res.text:
        print(strings.Helper.RED, '<| New version available!')
        print(
            f" <| Run {strings.Helper.PURPLE}'git pull' {strings.Helper.RED}command to update.{strings.Helper.WHITE}\n")
    else:
        print(
            f"{strings.Helper.GREEN} <| You are running the latest version.{strings.Helper.WHITE}\n")

    try:
        while not domain.name:
            url = input(' <: Domain name: ')
            if not domain.set_name(url):
                print(' <x Check the domain URL and try again.')

        while not search_type:
            print(strings.search_types)
            option = input('    Run      >_')
            search_type = domain.set_search_option(option)
            if not search_type:
                print(' <x The option does not exist.')

        threads = input('    Threads  >_')
        domain.set_threads(threads)

        print(f'\n    Request Timeout  ::  {domain.timeout}')
        print(f'    Protocol         ::  {domain.protocol}')
        print(f'    User-Agent       ::  {domain.headers["User-Agent"]}\n\n')
        domain.search()

    except KeyboardInterrupt:
        domain.stop_executor()
        print(' <| Bye Bye ;)')
