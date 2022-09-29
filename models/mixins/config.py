class Config:
    OPTIONS = {
        1: 'environments',
        2: 'directories',
        3: 'subdomains',
        4: 'emails',
        5: 'S3 Buckets',
        6: 'Azure Blob Containers',
        7: 'Firebase Databases',
        8: 'Response Misconfigurations'
    }

    TESTS_WITH_THREADS = (1, 2, 3, 5, 6, 7)

    BAD_CODES = (400, 404, 411, 500, 501, 502, 503, 504)

    ENV_LIST = 'wordlists/env_wordlist.txt'
    DIR_LIST = 'wordlists/dir_wordlist.txt'
    SUB_LIST = 'wordlists/sub_wordlist.txt'
    CLOUD_LIST = 'wordlists/cloud_wordlist.txt'

    TIMEOUT = 4
