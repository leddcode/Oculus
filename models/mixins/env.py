from concurrent.futures import ThreadPoolExecutor


class Env:

    def __add_permutations(self, i, word, part, parts):
        for char in ('-', '_', '.', ''):
            parts[i] = f'{word}{char}{part}'
            self.permutations.append(f'{self.protocol}://' + '.'.join(parts))
            parts[i] = f'{part}{char}{word}'
            self.permutations.append(f'{self.protocol}://' + '.'.join(parts))

    def __permutate_env_urls(self):
        with open(self.ENV_LIST, 'r') as wl:
            for w in wl.read().splitlines():
                parts = self.parts[:]
                for i in range(len(self.parts) - 1):
                    part = parts[i]
                    self.__add_permutations(i, w, part, parts)
                    parts = self.parts[:]

    def __create_env_pool(self):
        print(f"\n{self.p_warn('PROC')} Creating possible urls")
        self.__permutate_env_urls()
        print(f"{self.p_warn('PROC')} Searching for {self.search_type}\n")
        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            self.executor = executor
            total = len(self.permutations)
            for url in self.permutations:
                self.futures.append(
                    self.executor.submit(self._make_request, url, total))

    def _search_envs(self):
        self.__create_env_pool()
