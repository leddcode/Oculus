import requests


class Email:

    '''   ⭐⭐⭐   '''
    URL = "https://trophy.onrender.com"
    COOKIES = {
        "Don't forget to star the Oculus project!":
        "https://github.com/leddcode/Oculus"
    }

    def __intelx_search(self):
        print(f"\n{self.p_warn('PROC')} Leaked Emails Lookup")
        emails = requests.get(
            f'{self.URL}/emails/{self.name}',
            cookies=self.COOKIES).json()[self.name]
        for email in emails:
            self._write(email, 'emails')
            print(f'{self.GREEN}       {email}{self.WHITE}')
        if not emails:
            print(f'{self.CYAN}       No results{self.WHITE}')

    def _search_emails(self):
        self.check_records()
        self.__intelx_search()
