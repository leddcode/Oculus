import requests


class Email:

    '''   ⭐⭐⭐   '''
    URL = "https://trophyio.herokuapp.com"
    COOKIES = {
        "Don't forget to star the Oculus project!":
        "https://github.com/leddcode/Oculus"
    }

    def __intelx_search(self):
        print(self.YELLOW, '<| Leaked Emails', self.WHITE)
        emails = requests.get(
            f'{self.URL}/emails/{self.name}',
            cookies=self.COOKIES).json()[self.name]
        for email in emails:
            self._write(email, 'emails')
            print(self.GREEN, f'<+ {email}', self.WHITE)

        if not emails:
            print(self.CYAN, '<-  No results', self.WHITE)

    def _search_emails(self):
        self.check_records()
        self.__intelx_search()
