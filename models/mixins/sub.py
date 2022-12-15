from concurrent.futures import ThreadPoolExecutor

import requests


class Sub:

    def __crtsh_search(self):
        print(f"{self.p_plain('PROC')} Certificate Search\n")

        url = f'https://crt.sh/?q=.{self.name}&output=json'
        for cert in requests.get(url).json():
            for sd in cert['name_value'].split('\n'):
                if sd not in self.cert_subdomains and '*' not in sd:
                    self.cert_subdomains.append(sd)
                    self._write(sd, 'certificate_search')
                    print(f'{self.CYAN}       {sd}{self.WHITE}')

        if not self.cert_subdomains:
            print(f'{self.CYAN}       No results{self.WHITE}')

    def __create_sub_pool(self):
        print(f"\n{self.p_warn('PROC')} Brute-Force\n")
        with open(self.SUB_LIST, 'r') as wl:
            with ThreadPoolExecutor(max_workers=self.threads) as executor:
                self.executor = executor
                words = wl.read().splitlines()
                total = len(words)
                for w in words:
                    sd = f'{w}.{self.name}'
                    if sd not in self.cert_subdomains:
                        self.futures.append(self.executor.submit(
                            self._make_request, f'{self.protocol}://{sd}', total))
                    else:
                        self.count_requests += 1

    def _search_subs(self):
        print(f"\n{self.p_plain('PROC')} Searching for {self.search_type}")
        self.__crtsh_search()
        self.__create_sub_pool()
