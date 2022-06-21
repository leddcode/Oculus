import subprocess

import requests


class Email:

    '''   ⭐⭐⭐   '''
    URL = f"https://trophyio.herokuapp.com"
    COOKIES = {
        "Don't forget to star the Oculus project!":
        "https://github.com/enotr0n/Oculus"
    }

    subprocess.Popen(['curl', URL], stdout=subprocess.DEVNULL)

    def __intelx_search(self):
        print(self.YELLOW, f'<| Leaked Emails', self.WHITE)
        emails = requests.get(
            f'{self.URL}/emails/{self.name}',
            cookies=self.COOKIES).json()[self.name]
        for email in emails:
            print(self.GREEN, f'<+ {email}', self.WHITE)

        if not emails:
            print(self.CYAN, '<-  No results', self.WHITE)

    def _search_emails(self):
        self.check_records()
        self.__intelx_search()
