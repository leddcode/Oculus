from concurrent.futures import ThreadPoolExecutor


class Bucket:

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

    def _search_s3_buckets(self):
        print(f' <| Building permutations\n')
        self.__create_s3_pool()
                   
    '''Azure Blobs'''

    def __add_azure_blobs_permutations(self, word, keyword, all_words):
        for char in ('-', '_', '.', ''):
            query_1 = f'{word}{char}{keyword}'
            query_2 = f'{keyword}{char}{word}'
            for w in all_words:
                self.permutations.append(
                    f'https://{query_1}.blob.core.windows.net/{w}/?restype=container&comp=list')
                self.permutations.append(
                    f'https://{query_2}.blob.core.windows.net/{w}/?restype=container&comp=list')

    def __permutate_azure_blobs_urls(self):
        self.permutations = []
        with open(self.CLOUD_LIST, 'r') as wl:
            words = wl.read().splitlines()
            for keyword in self.__get_keywords():
                for w in words:
                    self.permutations.append(
                        f'https://{keyword}.blob.core.windows.net/{w}/?restype=container&comp=list')
                    self.__add_azure_blobs_permutations(w, keyword, words)

    '''Cloud - General'''
    
    def __permutate_cloud_urls(self):
        if self.search_type == self.OPTIONS['5']:
            self.__permutate_s3_urls()
        elif self.search_type == self.OPTIONS['6']:
            self.__permutate_azure_blobs_urls()

    def __create_cloud_pool(self):
        print(f' <| Building permutations\n')
        self.__permutate_cloud_urls()
        print(f' <| Searching for {self.search_type}\n')
        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            self.executor = executor
            for url in self.permutations:
                self.futures.append(self.executor.submit(
                    self._make_request, url))

    def _cloud_enum(self):
        self.__create_cloud_pool()
