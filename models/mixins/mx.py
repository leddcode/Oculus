import socket

from dns.resolver import resolve
import requests


class Mx:

    def __get_ip(self, domain):
        try:
            domain_ip = socket.gethostbyname(domain)
            return domain_ip
        except:
            return ''

    def __get_mx_data(self):
        try:
            records = resolve(self.name, 'MX')
            ips = []
            for rdata in records:
                rx, domain = str(rdata).split(' ')
                domain = domain[:-1] if domain.endswith('.') else domain
                domain_ip = self.__get_ip(domain)
                ips.append(domain_ip)
                output = f'<+ {rx} {domain}'
                output += f'{" " * (55 - len(output))} | {domain_ip}'
                self._write(output, 'records')
                print(self.GREEN, output)
            return ips
        except Exception:
            self._write('<- No MX Records Found', 'records')
            print(self.RED, '<- No MX Records Found')

    def __get_dkim_record(self):
        try:
            data = requests.get(f'https://www.courier.com/api/tools/dkim-record-checker/?domain={self.name}&selector=site').json()
            if not data['error']:
                rec = data['result']['record']
                self._write(f'<+ DKIM  Record: {rec}', 'records')
                print(self.GREEN, f'<+ DKIM  Record: {rec}')
                print(data['result']['record'])
            else:
                self._write("<- DKIM  Record not published", 'records')
                print(self.RED, "<- DKIM  Record not published")
        except Exception:
            self._write("<- DKIM lookup failed", 'records')
            print(self.RED, "<- DKIM lookup failed")

    def __get_dmarc_record(self):
        try:
            dmarc_record = resolve(
                f'_dmarc.{self.name}', 'TXT')
            for rec in dmarc_record:
                if 'v=DMARC1' in str(rec):
                    self._write(f'<+ DMARC Record: {rec}', 'records')
                    print(self.GREEN, f'<+ DMARC Record: {rec}')
                if 'p=none' in str(rec):
                    self._write('<- DMARC Quarantine/Reject policy not enabled', 'records')
                    print(self.RED, '<- DMARC Quarantine/Reject policy not enabled')
        except Exception:
            self._write("<- DMARC Record not published", 'records')
            print(self.RED, "<- DMARC Record not published")

    def __get_spf_record(self):
        try:
            records = resolve(self.name, 'TXT')
            for rec in records:
                if 'v=spf1' in str(rec):
                    return str(rec)
        except Exception:
            self._write("<- The domain has no Mail Server ??", 'records')
            print(self.PURPLE, "<- The domain has no Mail Server ??")

    def __check_spf_record(self):
        rec = self.__get_spf_record()
        if rec:
            self._write(f'<+ SPF Record: {rec}\n', 'records')
            print(self.GREEN, f'<+ SPF Record: {rec}\n')
        else:
            self._write("<- SPF Record not published\n", 'records')
            print( self.RED, "<- SPF Record not published\n")

    def check_records(self):
        print(self.YELLOW, '<| Mail Server Records', self.WHITE)
        ips = self.__get_mx_data()
        self.__get_dkim_record()
        self.__get_dmarc_record()
        self.__check_spf_record()
        if ips:
            self.shodan_lookup(ips)
