from dns.resolver import resolve

from utils import strings


class MX:

    def __get_mx_data(self):
        try:
            records = resolve(self.name, 'MX')
            for rdata in records:
                print(
                    strings.Helper.GREEN,
                    f'<+ {rdata}'
                )
        except Exception:
            print(
                strings.Helper.RED,
                f'<- No MX Records Found'
            )

    def __get_dmarc_record(self):
        try:
            dmarc_record = resolve(
                f'_dmarc.{self.name}', 'TXT')
            for rec in dmarc_record:
                if 'v=DMARC1' in str(rec):
                    print(
                        strings.Helper.GREEN,
                        f'<+ DMARC Record: {rec}'
                    )
                if 'p=none' in str(rec):
                    print(
                        strings.Helper.RED,
                        '<- DMARC Quarantine/Reject policy not enabled'
                    )
        except Exception:
            print(
                strings.Helper.RED,
                "<- DMARC Record not published"
            )

    def __get_spf_record(self):
        try:
            records = resolve(self.name, 'TXT')
            for rec in records:
                if 'v=spf1' in str(rec):
                    return str(rec)
        except Exception:
            print(
                strings.Helper.PURPLE,
                "<x The domain has no Mail Server ??"
            )

    def __check_spf_record(self):
        rec = self.__get_spf_record()
        if rec:
            print(
                strings.Helper.GREEN,
                f'<+ SPF Record: {rec}\n'
            )
        else:
            print(
                strings.Helper.RED,
                "<- SPF Record not published\n"
            )

    def check_records(self):
        print(
            strings.Helper.YELLOW,
            '<| Mail Server Records',
            strings.Helper.WHITE
        )
        self.__get_mx_data()
        self.__get_dmarc_record()
        self.__check_spf_record()
