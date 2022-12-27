#  TODO
#  1. Analize multiple response
#  2. Search for tokens
#  3. Parse JWT
#  4. Add: self.name = ip
from concurrent.futures import ThreadPoolExecutor
import json
import re
import socket
from threading import Lock
from urllib3.exceptions import InsecureRequestWarning

from bs4 import BeautifulSoup as bs
import requests

requests.packages.urllib3.disable_warnings(
        category=InsecureRequestWarning)

class Scan:
    LOCK = Lock()
    
    GraphQL_ENDPOINTS = (
        'graphql/',
        'graph/',
        'graphiql/',
        'graphql/console/',
        'v1/explorer/',
        'v1/graphiql/',
        'graphql.php',
        'graphiql.php',
        'graphql',
        'graph',
        'graphiql',
        'v1/explorer',
        'v1/graphiql',
        'graphql/console',
    )

    def __is_server_header_set(self):
        if 'Server' in self.res_headers:
            return f'{self.PURPLE}Server:{self.WHITE} {self.res_headers["Server"]}'

    def __is_x_powered_by_header_set(self):
        if 'X-Powered-By' in self.res_headers:
            return f'{self.PURPLE}X-Powered-By:{self.WHITE} {self.res_headers["X-Powered-By"]}'

    def __is_asp_net_header_set(self):
        if 'X-AspNet-Version' in self.res_headers:
            return f'{self.PURPLE}Asp.Net Version:{self.WHITE} {self.res_headers["X-AspNet-Version"]}'

    def __is_misconfigured_content_type(self):
        if 'X-Content-Type-Options' not in self.res_headers:
            return 'X-Content-Type-Options header is not set.'
        elif self.res_headers['X-Content-Type-Options'] != 'nosniff':
            return f'X-Content-Type-Options header is misconfigured and set to: {self.res_headers["X-Content-Type-Options"]}'

    def __is_misconfigured_hsts(self):
        if 'Strict-Transport-Security' not in self.res_headers:
            return 'Strict-Transport-Security header is not set.'
        res = 'Strict-Transport-Security: '
        if 'max-age=31536000' not in self.res_headers['Strict-Transport-Security']:
            res += f'header is misconfigured and set to: {self.res_headers["Strict-Transport-Security"]}, '
        if 'includesubdomains' not in self.res_headers['Strict-Transport-Security'].lower():
            res += f'{self.RED}includeSubDomains{self.WHITE} directive is not set, '
        if 'preload' not in self.res_headers['Strict-Transport-Security'].lower():
            res += f'{self.RED}Preload{self.WHITE} directive is not set'
        if res:
            return f'{res}'

    def __is_misconfigured_xxss(self):
        if 'X-XSS-Protection' not in self.res_headers:
            return 'X-XSS-Protection header is not set.'
        elif '1; mode=block' not in self.res_headers['X-XSS-Protection']:
            return f'X-XSS-Protection header is misconfigured and set to: {self.res_headers["X-XSS-Protection"]}'

    def __is_misconfigured_xframe(self):
        if 'X-Frame-Options' not in self.res_headers:
            return 'X-Frame-Options header is not set.'
        elif self.res_headers['X-Frame-Options'].lower() not in ('sameorigin', 'deny') :
            return f'X-Frame-Options header is misconfigured and set to: {self.res_headers["X-Frame-Options"]}'

    def __is_misconfigured_csp(self):
        if 'Content-Security-Policy' not in self.res_headers:
            return f'CSP protection is not implemented.'
        return f'{self.GREEN}CSP{self.WHITE}: {self.res_headers["Content-Security-Policy"]}'

    def __are_cookies_configured(self):
        if 'set-cookie' in self.res_headers:
            cookies = self.res_headers['set-cookie'].split(',')
            res = ''
            for c in cookies:
                cres = f'\n       {self.CYAN}# {c.strip()}{self.WHITE}\n'
                if 'HttpOnly' not in c:
                    cres += '       The "HttpOnly" flag is not set.\n'
                if 'Secure' not in c:
                    cres += '       The "Secure" flag is not set.\n'
                if 'SameSite=None' in c:
                    cres += '       The "SameSite" property is set to "None".'
                res += cres
            return res
    
    '''Find versions in script src'''
    def __extract_script_versions(self):
        scripts = [script for script in self.res_soup.find_all('script') if script.has_attr('src')]
        versions = [script['src'] for script in scripts if re.search(r'\?ver=\d+\.\d+', script['src'])]
        if versions:
            padding = '\n' + ' ' * 25
            output = padding.join(v for v in versions)
            return f'{self.PURPLE}Exposed Versions:{self.WHITE} {output}'
    
    '''Generators from Meta tags'''
    def __extract_generators(self):
        generators = self.res_soup.find_all('meta', {'name': 'generator'})
        if generators:
            return f'{self.PURPLE}Generators:{self.WHITE} {", ".join(g["content"] for g in generators)}'

    '''GraphQL'''
    def __to_pretty_json(self, dic):
        j = json.dumps(dic, sort_keys=True,)
                    # indent=4, separators=(',', ': '))
        j = j.replace(';', ';\n\t').replace('name', f'{self.DARKCYAN}name{self.WHITE}')
        return j

    def __get_graphql_schema(self, graphql_endpoint):
        introspection_query = {"query":"\n query IntrospectionQuery {\r\n __schema {\r\n queryType { name }\r\n mutationType { name }\r\n subscriptionType { name }\r\n types{name,fields{name}}\r\n }\r\n }\r\n "}
        gres = requests.post(self.url_to_analize + graphql_endpoint, data=introspection_query, allow_redirects=False, timeout=2)
        if gres.status_code == 301:
            gres = requests.post(gres.headers['Location'], data=introspection_query, timeout=2)
        return self.__to_pretty_json(gres.json())

    def __test_graphql(self):
        for gep in self.GraphQL_ENDPOINTS:
            try:
                schema = self.__get_graphql_schema(gep)
                if schema:
                    self.__print_test_result('GraphQL API', f'\n{schema}', 'warn')
                    return 
            except Exception:
                pass
    
    '''Robots.txt'''
    def __robots_txt(self, output=''):
        res = requests.get(
            self.url_to_analize + '/robots.txt', headers=self.headers, verify=False)
        if res.status_code == 200 and 'allow' in res.text.lower():
            text = '\n       '.join(res.text.splitlines())
            text = text.replace('Host:', f'{self.CYAN}Host:      {self.WHITE}')
            text = text.replace('Sitemap:', f'{self.CYAN}Sitemap:   {self.WHITE}')
            text = text.replace('User-agent:', f'{self.CYAN}User-agent:{self.WHITE}')
            text = text.replace('User-Agent:', f'{self.CYAN}User-Agent:{self.WHITE}')
            text = text.replace('Disallow:', f'{self.RED}Disallow:  {self.WHITE}')
            output = '\n       ' + text.replace('Allow:', f'{self.GREEN}Allow:     {self.WHITE}') + '\n'
        if output:
            self.__print_test_result('Robots.txt', output, 'info')
    
    '''Leaks Beta'''
    def __search_leakix(self):
        url = f'https://leakix.net/search?scope=leak&q={self.name}'
        res = requests.get(url, headers=self.headers, verify=False)
        soup = bs(res.text, "html.parser")
        links = soup.find_all('a')
        results = []
        for a in links:
            if ('/host/' in a['href'] or '/domain/' in a['href']) and a.text not in results:
                results.append(a.text)
        return results
    
    def __is_ip(self, host):
        try:
            socket.inet_aton(host)
            return 'host'
        except socket.error:
            return 'domain'

    def __get_host_leaks(self, host):
        if self.__is_ip(host) == 'domain' and self.name not in host:
            mes = 'Most likely this domain is not associated with the target domain.'
            text = f'       {self.CYAN}During the scan, the following domain was detected: {host}\n       {mes}{self.WHITE}'
            return [text]
        else:
            url = f'https://leakix.net/{self.__is_ip(host)}/{host}'
            res = requests.get(url, headers=self.headers, verify=False)
            soup = bs(res.text, "html.parser")
            col = soup.find(class_ = 'col-xl-6')
            main_card = col.find(class_ = 'card mb-3')
            cards = main_card.find_all(class_ = 'card')
            results = []
            for c in cards:
                try:
                    title = c.find(class_ = 'card-header bg-danger')
                    pre = c.find('pre')
                    pre_text = pre.text
                    if pre_text:
                        if not 'remote "origin"' in pre_text:
                            pre_text = pre_text[:500] + '...'
                        pre_line = [f'       {l}' for l in pre_text.split('\n') if l.strip()]
                        pre_text = '\n'.join(pre_line)
                        text = f'       {self.YELLOW}{title.text.strip()}{self.CYAN}\n{pre_text}'
                        results.append(text)
                except:
                    pass
            return set(results)

    def __leaks(self):
        hosts = self.__search_leakix()
        for host in hosts:
            mes = ''
            try:
                for leak in self.__get_host_leaks(host):
                    mes += f'\n{leak}{self.WHITE}\n'
                self.__print_test_result(f'Indexed Information  ::  {host}', mes, 'info')
            except:
                pass
    
    '''URL Scan'''
    def __get_historical_domain_data(self):
        url = 'https://urlscan.io/api/v1/search/?q=domain:'
        return requests.get(
            url + self.name, headers=self.headers, verify=False).json()
    
    def __parse_domain_data(self, data):
        domain_data = {
            'IP': data['page']['ip'],
            'Domain Name': data['task']['domain'],
            'Apex Domain': data['page']['apexDomain'],
            'ASN': data['page']['asn'],
            'Technologies': [],
            'Outgoing Links': []
        }
        
        # Add Detected Technologies
        res = requests.get(
            f'https://urlscan.io/result/{data["_id"]}/', headers=self.headers, verify=False)
        soup = bs(res.text, "html.parser")
        soup = soup.find(class_ = 'col col-md-5')
        bb = soup.find_all('b')
        for b in bb:
            if b.text not in ('Overall confidence', 'Detected patterns'):
                domain_data['Technologies'].append(b.text.strip())
        # Add Outgoing Links
        res = requests.get(
            f'https://urlscan.io/result/{data["_id"]}/#links', headers=self.headers, verify=False)
        soup = bs(res.text, "html.parser")
        bottoms = soup.find_all(class_ = 'bottom5')
        for bo in bottoms:
            parts = bo.text.split('\n')
            for p in parts:
                if 'http' in p and 'URL' in p:
                    domain_data['Outgoing Links'].append(p.strip())
                    break
        return domain_data

    def __get_domain_data(self):
        data = self.__get_historical_domain_data()
        if data['results']:
            results = {}
            for r in data['results']:
                if r['task']['domain'] not in results:
                    try:             
                        results[r['task']['domain']] = self.__parse_domain_data(r)
                    except:
                        pass
            return results
    
    def __print_domain_data(self):
        results = self.__get_domain_data()
        if results:
            mes = ''
            for domain_data in results.values():
                text = f'\n{"〰️" * 18}\n'
                for k, v in domain_data.items():
                    if v:
                        text += f'{self.CYAN}{k}{self.WHITE}'
                        if isinstance(v, str):
                            text += f'{" " * (20 - len(k))}{v}\n'
                        else:
                            for entry in v:
                                text += f'\n{" " * 20}{entry}'
                            text += '\n'
                mes += text
            self.__print_test_result('URL Scan', mes, 'info')
    
    '''IP Scanner'''
    def __get_host_ip(self):
        return socket.gethostbyname(self.name)

    def __tcp_scan_port(self, host_ip, port):
        self.LOCK.acquire()
        print(f'{self.CLEAR}       TCP {port}', end='\r' )
        self.LOCK.release()
        output = ''
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(5)
            result = s.connect_ex((host_ip, port))
            if result == 0:
                output = f"{self.p_succ('OPEN')} TCP {port}      "
                self.ports_open += 1
                banner = s.recv(1024).decode()
                if banner:
                    banner = banner.replace('\n', '\n' + ' ' * 7).strip()
                    output += f'\n       {self.CYAN}{banner}{self.WHITE}\n'
            s.close()
        except:
            pass
        if output:
            self.LOCK.acquire()
            print(output)
            self.LOCK.release()
            self._write(output, 'Vulnerability Scan')

    def __udp_scan_port(self, host_ip, port, m='0c'):
        self.LOCK.acquire()
        print(f'{self.CLEAR}       UDP {port}', end='\r' )
        self.LOCK.release()
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.settimeout(0.5)
            s.sendto(m.encode(), (host_ip, port))
            o = (s.recvfrom(1024))
            self.LOCK.acquire()
            print(f'{self.p_succ("OPEN")} UDP {port}  ')
            self.LOCK.release()
            self._write(f'{self.p_succ("OPEN")} UDP {port}  ', 'Vulnerability Scan')
            self.ports_open += 1
        except:
            pass

    def __ip_scanner(self, host_ip):
        total_ports = 65535
        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            self.executor = executor
            for port in range(1, total_ports):
                self.futures.append(self.executor.submit(
                    self.__tcp_scan_port, host_ip, port))
                self.futures.append(self.executor.submit(
                    self.__udp_scan_port, host_ip, port))
    
    '''Print results'''
    def __print_test_result(self, test_name, test_res, etype=None):
        if test_res:
            self.LOCK.acquire()
            test_name = test_name + '\n' if test_name else ''
            if etype == 'info':
                print(f"{self.p_info('INFO')} {test_name}{test_res}")
            elif etype == 'warn':
                print(f"{self.p_warn('WARN')} {test_name}{test_res}")
            else:
                print(f"{self.p_plain('~~~~')} {test_name}{test_res}")
            self.LOCK.release()
            self._write(test_res, 'Vulnerability Scan')

    '''Response Analysis'''
    def __analize_response(self):
        self.server_response = self._request(self.url_to_analize)
        self.res_headers = self.server_response.headers
        self.res_soup = bs(self.server_response.text, "html.parser")

        # Headers
        self.__print_test_result(
            None,
            self.__is_server_header_set(),
            'info')
        self.__print_test_result(
            None,
            self.__is_x_powered_by_header_set(),
            'info')
        self.__print_test_result(
            None,
            self.__is_asp_net_header_set(),
            'info')
        self.__print_test_result(
            None,
            self.__extract_generators(),
            'info')
        self.__print_test_result(
            None,
            self.__is_misconfigured_content_type(),
            'warn')
        self.__print_test_result(
            None,
            self.__is_misconfigured_hsts(),
            'warn')
        self.__print_test_result(
            None,
            self.__is_misconfigured_xxss(),
            'warn')
        self.__print_test_result(
            None,
            self.__is_misconfigured_xframe(),
            'warn')
        self.__print_test_result(
            None,
            self.__is_misconfigured_csp(),
            'warn')
        self.__print_test_result(
            'Cookies',
            self.__are_cookies_configured(),
            'warn')
        self.__print_test_result(
            None,
            self.__extract_script_versions(),
            'info')

    '''Full Scan'''
    def _scan(self, url):
        self.url_to_analize = url
        print(f"\n{self.p_cyan('PROC')} {self.search_type}  [{self.url_to_analize}]")
        self._write(f'{self.search_type}  [{self.url_to_analize}]\n', 'Vulnerability Scan')
        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            self.executor = executor
            self.futures.append(self.executor.submit(self.__test_graphql))
            self.futures.append(self.executor.submit(self.__analize_response))
            self.futures.append(self.executor.submit(self.__print_domain_data))
            self.futures.append(self.executor.submit(self.__leaks))
            self.futures.append(self.executor.submit(self.__robots_txt))
        self._check_futures()
        
        # IP Scan
        to_scan_ports = input(f"\n{self.p_warn('INIT')} Scan for open ports?{self.WHITE} (y/N)  ")
        if to_scan_ports == 'y':
            host_ip = self.__get_host_ip()
            ip_scan_banner = f'{self.name}  ::  {host_ip}'
            print(f'       {"-" * len(ip_scan_banner)}\n       {ip_scan_banner}\n       {"-" * len(ip_scan_banner)}')
            self.__ip_scanner(host_ip)
            self._check_futures()
