class Config:
    OPTIONS = {
        1: 'environments',
        2: 'directories',
        3: 'subdomains',
        4: 'emails',
        5: 'S3 Buckets',
        6: 'Azure Blob Containers',
        7: 'Firebase Databases',
        8: 'GCP Buckets',
        9: 'General Information and Misconfigurations'
    }

    TESTS_WITHOUT_THREADS = (4,)

    BAD_CODES = (400, 404, 411, 500, 501, 502, 503, 504)

    ENV_LIST = 'wordlists/env_wordlist.txt'
    DIR_LIST = 'wordlists/dir_wordlist.txt'
    SUB_LIST = 'wordlists/sub_wordlist.txt'
    CLOUD_LIST = 'wordlists/cloud_wordlist.txt'
    USER_AGENTS_LIST = 'utils/user_agents.txt'

    TIMEOUT = 4
