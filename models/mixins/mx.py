from dns.resolver import resolve


class Mx:

    def __get_mx_data(self):
        try:
            records = resolve(self.name, 'MX')
            for rdata in records:
                self._write(f'<+ {rdata}', 'records')
                print(
                    self.GREEN,
                    f'<+ {rdata}'
                )
        except Exception:
            self._write('<- No MX Records Found', 'records')
            print(
                self.RED,
                '<- No MX Records Found'
            )

    def __get_dmarc_record(self):
        try:
            dmarc_record = resolve(
                f'_dmarc.{self.name}', 'TXT')
            for rec in dmarc_record:
                if 'v=DMARC1' in str(rec):
                    self._write(f'<+ DMARC Record: {rec}', 'records')
                    print(
                        self.GREEN,
                        f'<+ DMARC Record: {rec}'
                    )
                if 'p=none' in str(rec):
                    self._write('<- DMARC Quarantine/Reject policy not enabled', 'records')
                    print(
                        self.RED,
                        '<- DMARC Quarantine/Reject policy not enabled'
                    )
        except Exception:
            self._write("<- DMARC Record not published", 'records')
            print(
                self.RED,
                "<- DMARC Record not published"
            )

    def __get_spf_record(self):
        try:
            records = resolve(self.name, 'TXT')
            for rec in records:
                if 'v=spf1' in str(rec):
                    return str(rec)
        except Exception:
            self._write("<x The domain has no Mail Server ??", 'records')
            print(
                self.PURPLE,
                "<x The domain has no Mail Server ??"
            )

    def __check_spf_record(self):
        rec = self.__get_spf_record()
        if rec:
            self._write(f'<+ SPF Record: {rec}\n', 'records')
            print(
                self.GREEN,
                f'<+ SPF Record: {rec}\n'
            )
        else:
            self._write("<- SPF Record not published\n", 'records')
            print(
                self.RED,
                "<- SPF Record not published\n"
            )

    def check_records(self):
        print(
            self.YELLOW,
            '<| Mail Server Records',
            self.WHITE
        )
        self.__get_mx_data()
        self.__get_dmarc_record()
        self.__check_spf_record()
