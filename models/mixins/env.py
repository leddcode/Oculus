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
            words = wl.read()
            for w in words.splitlines():
                parts = self.parts[:]
                for i in range(len(self.parts) - 1):
                    part = parts[i]
                    self.__add_permutations(i, w, part, parts)
                    parts = self.parts[:]

    def __create_env_pool(self):
        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            self.executor = executor
            for url in self.permutations:
                self.futures.append(
                    self.executor.submit(self._make_request, url))

    def _search_envs(self):
        print(' <| Creating possible urls')
        self.__permutate_env_urls()

        print(f' <| Searching for {self.search_type}\n')
        self.__create_env_pool()