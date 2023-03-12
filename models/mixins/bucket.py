from concurrent.futures import ThreadPoolExecutor
from itertools import combinations

import requests


class Bucket:

    # Template key is the self.option parameter (the chosen test)
    TEMPLATE = {
        5: "https://{}.s3.amazonaws.com",
        6: "https://{}.blob.core.windows.net",
        7: "https://{}.firebaseio.com/.json",
        8: "https://storage.googleapis.com/{}"
    }

    def __init__(self):
        self.azure_targets = []

    def __get_keywords(self):
        keywords = [w for w in self.name.split(
            '.')[:-1] if len(w) > 3] + self.keywords
        print(
            f" with following keywords: {self.GREEN}{', '.join(keywords)}{self.WHITE}")
        if len(keywords) > 1:
            combs = combinations(keywords, 2)
            for comb in combs:
                for sign in ('', '-', '_'):
                    keywords.extend(
                        [f'{sign}'.join(comb), f'{sign}'.join(reversed(comb))])
        return keywords

    # Azure Blobs
    def __permutate_containers(self):
        """
        Takes a list of blob URLs and returns a list of possible container URLs.
        """
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
                return url
        except:
            '''Bad Request'''

    def __azure_blob_pool(self):
        results = self.executor.map(self.__azure_request, self.permutations)
        total = len(self.permutations)
        print(self.p_info("INFO"), f"Total payloads: {total}\n")
        for result in results:
            self.count_requests += 1
            if result:
                print(f'{self.CYAN}       {result} {" " * 30}{self.WHITE}')
            if self.status_bar in ('y', 'Y', 'yes', 'Yes', 'go', 'sure', 'wtf'):
                pr = str(round(self.count_requests * 100 / total, 1)) + '%'
                self.LOCK.acquire()
                print(
                    f'{self.p_warn("SENT")} {pr:<8}R:{self.count_requests}', end='\r')
                self.LOCK.release()
        self.count_requests = 0

    def __azure_pool(self):
        print(f"\n{self.p_cyan('PROC')} Blobs Lookup")
        self.__azure_blob_pool()  # First find blob urls
        if self.azure_targets:
            print(f"{self.CLEAR}\n{self.p_cyan('PROC')} Containers Lookup")
            self.__permutate_containers()
            self.__cloud_pool()
        else:
            print(f"{self.CLEAR}{self.p_plain('~~~~')} No Blobs")

    # Common - cloud
    def __add_permutations(self, template, word, keyword):
        for char in ('-', '_', '.', ''):
            self.permutations.append(template.format(word + char + keyword))
            self.permutations.append(template.format(keyword + char + word))

    def __permutate_urls(self, template):
        self.permutations = []
        with open(self.CLOUD_LIST, 'r') as wl:
            words = wl.read().splitlines()
            for keyword in self.__get_keywords():
                self.permutations.append(template.format(keyword))
                for w in words:
                    self.__add_permutations(template, w, keyword)

    def __cloud_pool(self):
        total = len(self.permutations)
        print(self.p_info("INFO"), f"Total payloads: {total}\n")
        for url in self.permutations:
            self.futures.append(self.executor.submit(
                self._make_request, url, total))

    def __create_cloud_pool(self):
        print(f"\n{self.p_cyan('PROC')} Building permutations", end='')
        self.__permutate_urls(self.TEMPLATE[self.option])
        print(f"{self.p_cyan('PROC')} Searching for {self.search_type}")
        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            self.executor = executor
            if self.option in (5, 7, 8):
                self.__cloud_pool()
            elif self.option == 6:
                self.__azure_pool()

    def _cloud_enum(self):
        self.__create_cloud_pool()
