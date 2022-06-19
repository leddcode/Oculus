import requests


class Email:

    def __intelx_search(self):
        print(
            self.YELLOW,
            f'<| Leaked Emails',
            self.WHITE
        )

        '''   ⭐⭐⭐  '''
        url = f"https://trophyio.herokuapp.com"
        cookies = {
            "Don't forget to star the Oculus project!":
            "https://github.com/enotr0n/Oculus"
        }
        requests.get(f'{url}/console/oculus?emails')
        emails = requests.get(
            f'{url}/emails/{self.name}', cookies=cookies).json()[self.name]
        for email in emails:
            print(
                self.GREEN,
                f'<+ {email}',
                self.WHITE
            )

        if not emails:
            print(
                self.CYAN,
                '<-  No results',
                self.WHITE
            )

    def _search_emails(self):
        self.check_records()
        self.__intelx_search()
