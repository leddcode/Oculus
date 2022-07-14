from concurrent.futures import ThreadPoolExecutor


class Dir:

    def __create_dir_pool(self):
        with open(self.DIR_LIST, 'r') as wl:
            with ThreadPoolExecutor(max_workers=self.threads) as executor:
                self.executor = executor
                words = wl.read().splitlines()
                total = len(words)
                for w in words:
                    self.futures.append(self.executor.submit(
                        self._make_request, f'{self.protocol}://{self.name}/{w}', total))

    def _search_dirs(self):
        print(f' <| Searching for {self.search_type}\n')
        self.__create_dir_pool()
