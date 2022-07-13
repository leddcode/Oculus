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

    def __add_s3_permutations(self, word, keyword):
        for char in ('-', '_', '.', ''):
            query = f'{word}{char}{keyword}'
            self.permutations.append(
                f'https://{query}.s3.amazonaws.com/')
            query = f'{keyword}{char}{word}'
            self.permutations.append(
                f'https://{query}.s3.amazonaws.com/')

    def __permutate_s3_urls(self):
        with open(self.CLOUD_LIST, 'r') as wl:
            words = wl.read()
            for keyword in self.__get_keywords():
                self.permutations.append(
                    f'https://{keyword}.s3.amazonaws.com/')
                for w in words.splitlines():
                    self.__add_s3_permutations(w, keyword)

    def __create_s3_pool(self):
        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            self.executor = executor
            self.__permutate_s3_urls()
            print(f' <| Searching for {self.search_type}\n')
            for url in self.permutations:
                self.futures.append(self.executor.submit(
                    self._make_request, url))

    def _search_s3_buckets(self):
        print(f' <| Building permutations\n')
        self.__create_s3_pool()
