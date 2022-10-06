#  TODO
#  1. Analize multiple response
#  2. Search for tokens
#  3. Parse JWT
#  4. WP analysis (users, admin page and so on)
from concurrent.futures import ThreadPoolExecutor
import json
import socket
from threading import Lock

import requests


class Response_Analizer:
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
            return f' {self.YELLOW}<|  Server:{self.WHITE} {self.res_headers["Server"]}'

    def __is_x_powered_by_header_set(self):
        if 'X-Powered-By' in self.res_headers:
            return f' {self.YELLOW}<|  X-Powered-By:{self.WHITE} {self.res_headers["X-Powered-By"]}'

    def __is_asp_net_header_set(self):
        if 'X-AspNet-Version' in self.res_headers:
            return f' {self.YELLOW}<|  Asp.Net Version:{self.WHITE} {self.res_headers["X-AspNet-Version"]}'

    def __is_misconfigured_content_type(self):
        if 'X-Content-Type-Options' not in self.res_headers:
            return f' {self.RED}<x{self.WHITE}  X-Content-Type-Options header is not set.'
        elif self.res_headers['X-Content-Type-Options'] != 'nosniff':
            return f' {self.RED}<x{self.WHITE}  X-Content-Type-Options header is misconfigured and set to: {self.res_headers["X-Content-Type-Options"]}'

    def __is_misconfigured_hsts(self):
        if 'Strict-Transport-Security' not in self.res_headers:
            return f' {self.RED}<x{self.WHITE}  Strict-Transport-Security header is not set.'
        res = ''
        if 'max-age=31536000' not in self.res_headers['Strict-Transport-Security']:
            res +=  f' {self.RED}<x{self.WHITE}  Strict-Transport-Security header is misconfigured and set to: {self.res_headers["Strict-Transport-Security"]}\n'
        if 'includesubdomains' not in self.res_headers['Strict-Transport-Security'].lower():
            res += f' {self.RED}<x{self.WHITE}  includeSubDomains directive is not set.\n'
        if 'preload' not in self.res_headers['Strict-Transport-Security'].lower():
            res += f' {self.RED}<x{self.WHITE}  Preload directive is not set.\n'
        if res:
            return f'{res}'

    def __is_misconfigured_xxss(self):
        if 'X-XSS-Protection' not in self.res_headers:
            return f' {self.RED}<x{self.WHITE}  X-XSS-Protection header is not set.'
        elif '1; mode=block' not in self.res_headers['X-XSS-Protection']:
            return f' {self.RED}<x{self.WHITE}  X-XSS-Protection header is misconfigured and set to: {self.res_headers["X-XSS-Protection"]}'

    def __is_misconfigured_xframe(self):
        if 'X-Frame-Options' not in self.res_headers:
            return f' {self.RED}<x{self.WHITE}  X-Frame-Options header is not set.'
        elif self.res_headers['X-Frame-Options'].lower() not in ('sameorigin', 'deny') :
            return f' {self.RED}<x{self.WHITE}  X-Frame-Options header is misconfigured and set to: {self.res_headers["X-Frame-Options"]}'

    def __is_misconfigured_csp(self):
        if 'Content-Security-Policy' not in self.res_headers:
            return f' {self.RED}<x{self.WHITE}  CSP protection is not implemented.'
        return f' {self.GREEN}<+  {self.res_headers["Content-Security-Policy"]}'

    def __are_cookies_configured(self):
        if 'set-cookie' in self.res_headers:
            cookies = self.res_headers['set-cookie'].split(',')
            res = ''
            for c in cookies:
                cres = f'\n {self.BLUE}<#{self.WHITE}  {c.strip()}\n'
                if 'HttpOnly' not in c:
                    cres += f' {self.RED}<x{self.WHITE}  The "HttpOnly" flag is not set.\n'
                if 'Secure' not in c:
                    cres += f' {self.RED}<x{self.WHITE}  The "Secure" flag is not set.\n'
                if 'SameSite=None' in c:
                    cres += f' {self.RED}<x{self.WHITE}  The "SameSite" property is set to "None".\n'
                res += cres
            return res
    

    '''GraphQL'''
    def __to_pretty_json(self, dic):
        j = json.dumps(dic, sort_keys=True,)
                    # indent=4, separators=(',', ': '))
        j = j.replace(';', ';\n\t').replace('name', f'{self.ORANGE}name{self.WHITE}')
        return j

    def __get_graphql_schema(self, graphql_endpoint):
        introspection_query = {"query":"\n query IntrospectionQuery {\r\n __schema {\r\n queryType { name }\r\n mutationType { name }\r\n subscriptionType { name }\r\n types{name,fields{name}}\r\n }\r\n }\r\n "}
        gres = requests.post(self.url_to_analize + graphql_endpoint, data=introspection_query, allow_redirects=False, timeout=3)
        if gres.status_code == 301:
            gres = requests.post(gres.headers['Location'], data=introspection_query, timeout=3)
        return self.__to_pretty_json(gres.json())

    def __test_graphql(self):
        for gep in self.GraphQL_ENDPOINTS:
            try:
                schema = self.__get_graphql_schema(gep)
                if schema:
                    return schema
            except Exception:
                pass
    
    '''Robots.txt'''
    def __robots_txt(self):
        res = requests.get(self.url_to_analize + '/robots.txt')
        if res.status_code == 200:
            text = '\n     '.join(res.text.splitlines())
            text = text.replace('Sitemap:', f'{self.CYAN}Sitemap:{self.WHITE}')
            text = text.replace('User-agent:', f'{self.CYAN}User-agent:{self.WHITE}')
            text = text.replace('User-Agent:', f'{self.CYAN}User-Agent:{self.WHITE}')
            text = text.replace('Disallow:', f'{self.RED}Disallow:{self.WHITE}')
            return '\n     ' + text.replace('Allow:', f'{self.GREEN}Allow:   {self.WHITE}')
        return '\n     Not found.'
    
    '''IP Scanner'''
    def __get_host_ip(self):
        return socket.gethostbyname(self.name)

    def __tcp_scan_port(self, host_ip, port):
        self.LOCK.acquire()
        print(f'\r     TCP {port}', ' ' * 10, end='\r' )
        self.LOCK.release()
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(2)
            s.connect((host_ip, port))
            try:
                banner = s.recv(1024).decode()
                if not banner:
                    banner = '??'
                self.LOCK.acquire()
                print(f"     TCP [OPEN] {port}  //  {banner.replace('/n', '|').strip()}")
                self.LOCK.release()
            except:
                self.LOCK.acquire()
                print(f"     TCP [OPEN] {port}")
                self.LOCK.release()
            finally:
                self.ports_open += 1
                s.close()
        except:
            pass

    def __udp_scan_port(self, host_ip, port, m='0c'):
        self.LOCK.acquire()
        print(f'\r     UDP {port}', ' ' * 10, end='\r' )
        self.LOCK.release()
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.settimeout(0.2)
            s.sendto(m.encode(), (host_ip, port))
            o = (s.recvfrom(1024))
            self.LOCK.acquire()
            print(f'     UDP [OPEN] {port} ')
            self.LOCK.release()
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
    def __print_test_result(self, test_name, test_res):
        if test_res:
            if test_name:
                print(f'\n {self.YELLOW}<|  {test_name}{self.WHITE}')
            print(test_res)

    '''RUN'''
    def _analize_response(self, url):
        self.url_to_analize = url
        self.server_response = self._request(url)
        self.res_headers = self.server_response.headers

        print(f'{self.YELLOW} <|  URL:{self.WHITE} {self.url_to_analize}\n')

        '''Headers'''
        self.__print_test_result(
            None,
            self.__is_server_header_set())
        self.__print_test_result(
            None,
            self.__is_x_powered_by_header_set())
        self.__print_test_result(
            None,
            self.__is_asp_net_header_set())
        self.__print_test_result(
            'X-Content-Type-Options',
            self.__is_misconfigured_content_type())
        self.__print_test_result(
            'Strict-Transport-Security',
            self.__is_misconfigured_hsts())
        self.__print_test_result(
            'X-XSS-Protection',
            self.__is_misconfigured_xxss())
        self.__print_test_result(
            'X-Frame-Options',
            self.__is_misconfigured_xframe())
        self.__print_test_result(
            'CSP',
            self.__is_misconfigured_csp())
        self.__print_test_result(
            'Cookies',
            self.__are_cookies_configured())
        
        '''Robots.txt'''
        self.__print_test_result(
            'Robots.txt',
            self.__robots_txt())

        '''GraphQL'''
        graphql_test_result = self.__test_graphql()
        
        self.__print_test_result(
            'GraphQL API',
            graphql_test_result if graphql_test_result else ' <|  GraphQL API wasn\'t detected.' )

        '''IP Scan'''
        host_ip = self.__get_host_ip()  
        self.__print_test_result(
            'IP Scan',
            f'     {"-" * 50}\n     {self.name}  ::  {host_ip}')
        print(f'     {"-" * 50}')
        self.__ip_scanner(host_ip)
