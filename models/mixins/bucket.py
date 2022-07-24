from concurrent.futures import ThreadPoolExecutor

import requests


class Bucket:

    def __init__(self):
        self.azure_targets = []

    def __get_keywords(self):
        keywords = [w for w in self.name.split('.')[:-1] if len(w) > 3]
        if len(keywords) > 1:
            tmp = keywords[:]
            for sign in ('', '-', '_'):
                keywords.extend(
                    [f'{sign}'.join(tmp), f'{sign}'.join(reversed(tmp))])
        return keywords

    '''S3 Buckets'''

    def __add_s3_permutations(self, word, keyword):
        for char in ('-', '_', '.', ''):
            self.permutations.append(
                f'https://{word}{char}{keyword}.s3.amazonaws.com/')
            self.permutations.append(
                f'https://{keyword}{char}{word}.s3.amazonaws.com/')

    def __permutate_s3_urls(self):
        self.permutations = []
        with open(self.CLOUD_LIST, 'r') as wl:
            words = wl.read().splitlines()
            for keyword in self.__get_keywords():
                self.permutations.append(
                    f'https://{keyword}.s3.amazonaws.com/')
                for w in words:
                    self.__add_s3_permutations(w, keyword)

    '''Azure Blobs'''

    def __add_azure_blobs_permutations(self, word, keyword):
        for char in ('-', '_', '.', ''):
            self.permutations.append(
                f'https://{word}{char}{keyword}.blob.core.windows.net')
            self.permutations.append(
                f'https://{keyword}{char}{word}.blob.core.windows.net')

    def __permutate_azure_blobs_urls(self):
        self.permutations = []
        with open(self.CLOUD_LIST, 'r') as wl:
            words = wl.read().splitlines()
            for keyword in self.__get_keywords():
                self.permutations.append(
                    f'https://{keyword}.blob.core.windows.net')
                for w in words:
                    self.__add_azure_blobs_permutations(w, keyword)

    def __permutate_blob_containers(self):
        self.permutations = []
        with open(self.CLOUD_LIST, 'r') as wl:
            words = wl.read().splitlines()
            for target in self.azure_targets:
                for w in words:
                    self.permutations.append(
                        f'{target}/{w}/?restype=container&comp=list')

    def __azure_request(self, url):
        try:
            res = requests.get(
                url,
                headers=self.headers,
                timeout=self.TIMEOUT)
            if res.status_code:
                self._write(url, f'{res.status_code}')
                if res.status_code == 400:
                    self.azure_targets.append(url)
                return res.status_code, url
        except Exception:
            '''Bad Request'''

    def __azure_blob_pool(self):
        results = self.executor.map(self.__azure_request, self.permutations)
        total = len(self.permutations)
        for result in results:
            self.count_requests += 1
            if result:
                print(
                    f'{self.CYAN} <+  {result[0]}  {result[1]} {" " * 30}{self.WHITE}')
            progress = round(self.count_requests / total * 40)
            bar = f"{self.YELLOW}{progress * '■'}{self.WHITE}{(40 - progress) * '■'}"
            self.LOCK.acquire()
            print(
                f'\r <|  {bar:<40}  ::  {total} | {self.count_requests}',
                ' ' * 30,
                end='\r'
            )

        self.count_requests = 0

    def __azure_pool(self):
        print(' <| Blobs\n')
        self.__azure_blob_pool()
        if self.azure_targets:
            print('\n\n <| Containers\n')
            self.__permutate_blob_containers()
            self.__cloud_pool()
        else:
            print(' <- No Blobs\n')

    '''Firebase'''

    def __add_firebase_permutations(self, word, keyword):
        for char in ('-', '_', '.', ''):
            self.permutations.append(
                f'https://{word}{char}{keyword}.firebaseio.com/.json')
            self.permutations.append(
                f'https://{keyword}{char}{word}.firebaseio.com/.json')

    def __permutate_firebase_urls(self):
        self.permutations = []
        with open(self.CLOUD_LIST, 'r') as wl:
            words = wl.read().splitlines()
            for keyword in self.__get_keywords():
                self.permutations.append(
                    f'https://{keyword}.firebaseio.com/.json')
                for w in words:
                    self.__add_firebase_permutations(w, keyword)

    '''Cloud - Common'''

    def __cloud_pool(self):
        total = len(self.permutations)
        for url in self.permutations:
            self.futures.append(self.executor.submit(
                self._make_request, url, total))

    def __permutate_cloud_urls(self):
        if self.option == 5:
            self.__permutate_s3_urls()
        elif self.option == 6:
            self.__permutate_azure_blobs_urls()
        elif self.option == 7:
            self.__permutate_firebase_urls()

    def __create_cloud_pool(self):
        print(' <| Building permutations\n')
        self.__permutate_cloud_urls()
        print(f' <| Searching for {self.search_type}\n')
        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            self.executor = executor
            if self.option in (5, 7):
                self.__cloud_pool()
            elif self.option == 6:
                self.__azure_pool()

    def _cloud_enum(self):
        self.__create_cloud_pool()
