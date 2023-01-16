from concurrent.futures import ThreadPoolExecutor


class Dir:

    def __get_total(self, words):
        total = len(words)
        if self.extensions:
            urls_with_ext = list(filter(lambda w: '.' not in w, words))
            total += len(urls_with_ext) * len(self.extensions)
        return total

    def __search_with_extension(self, w, total):
        if (w and self.extensions
            and '.' not in w
            and w[0].isalnum()
            and w[-1].isalnum()):
            for ext in self.extensions:
                self.futures.append(self.executor.submit(
                    self._make_request,
                    f'{self.protocol}://{self.name}/{w}.{ext}', total)
                )

    def __create_dir_pool(self):
        with open(self.DIR_LIST, 'r', encoding='utf-8', errors='ignore') as wl:
            with ThreadPoolExecutor(max_workers=self.threads) as executor:
                self.executor = executor
                words = [''] + wl.read().splitlines()
                total = self.__get_total(words)
                print(self.p_info("INFO"), f"Total payloads: {total}\n")
                for w in words:
                    self.futures.append(self.executor.submit(
                        self._make_request, f'{self.protocol}://{self.name}/{w}', total))
                    self.__search_with_extension(w, total)

    def _search_dirs(self):
        print(f"\n{self.p_cyan('PROC')} Searching for {self.search_type}")
        self.__create_dir_pool()
