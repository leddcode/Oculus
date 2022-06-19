class Config:
    OPTIONS = {
        '1': 'environments',
        '2': 'directories',
        '3': 'subdomains',
        '4': 'emails'
    }

    BAD_CODES = (400, 404, 411, 500, 501, 502, 503, 504)

    ENV_LIST = 'wordlists/env_wordlist.txt'
    DIR_LIST = 'wordlists/dir_wordlist.txt'
    SUB_LIST = 'wordlists/sub_wordlist.txt'

    TIMEOUT = 4
