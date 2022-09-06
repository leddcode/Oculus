from concurrent.futures import ThreadPoolExecutor


class Dir:

    def __get_total(self, words):
        total = len(words)
        if self.extensions:
            urls_with_ext = list(filter(lambda w: '.' not in w, words))
            total += len(urls_with_ext) * len(self.extensions)
        return total

    def __search_with_extension(self, w, total):
        if self.extensions and '.' not in w:
            for ext in self.extensions:
                self.futures.append(self.executor.submit(
                    self._make_request,
                    f'{self.protocol}://{self.name}/{w}.{ext}', total)
                )

    def __create_dir_pool(self):
        with open(self.DIR_LIST, 'r') as wl:
            with ThreadPoolExecutor(max_workers=self.threads) as executor:
                self.executor = executor
                words = wl.read().splitlines()
                total = self.__get_total(words)
                for w in words:
                    self.futures.append(self.executor.submit(
                        self._make_request, f'{self.protocol}://{self.name}/{w}', total))
                    self.__search_with_extension(w, total)

    def _search_dirs(self):
        print(f' <| Searching for {self.search_type}\n')
        self.__create_dir_pool()
