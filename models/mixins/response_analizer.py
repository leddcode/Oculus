#  TODO
#  1. Analize multiple response
#  2. Search for tokens
#  3. Parse JWT
#  4. GraphQL Explorer
#  5. WP analysis (users, admin page and so on)
import json

import requests


class Response_Analizer:
    
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
            return f' {self.YELLOW}<|  Server: {self.res_headers["Server"]}{self.WHITE}'

    def __is_x_powered_by_header_set(self):
        if 'X-Powered-By' in self.res_headers:
            return f' {self.YELLOW}<|  X-Powered-By: {self.res_headers["X-Powered-By"]}{self.WHITE}'

    def __is_asp_net_header_set(self):
        if 'X-AspNet-Version' in self.res_headers:
            return f' {self.YELLOW}<|  Asp.Net Version: {self.res_headers["X-AspNet-Version"]}{self.WHITE}'

    def __is_misconfigured_content_type(self):
        if 'X-Content-Type-Options' not in self.res_headers:
            return f' {self.RED}<-{self.WHITE}  X-Content-Type-Options header is not set.'
        elif self.res_headers['X-Content-Type-Options'] != 'nosniff':
            return f' {self.RED}<-{self.WHITE}  X-Content-Type-Options header is misconfigured and set to: {self.res_headers["X-Content-Type-Options"]}'

    def __is_misconfigured_hsts(self):
        if 'Strict-Transport-Security' not in self.res_headers:
            return f' {self.RED}<-{self.WHITE}  Strict-Transport-Security header is not set.'
        res = ''
        if 'max-age=31536000' not in self.res_headers['Strict-Transport-Security']:
            res +=  f' {self.RED}<-{self.WHITE}  Strict-Transport-Security header is misconfigured and set to: {self.res_headers["Strict-Transport-Security"]}\n'
        if 'includesubdomains' not in self.res_headers['Strict-Transport-Security'].lower():
            res += f' {self.RED}<-{self.WHITE}  includeSubDomains directive is not set.\n'
        if 'preload' not in self.res_headers['Strict-Transport-Security'].lower():
            res += f' {self.RED}<-{self.WHITE}  Preload directive is not set.\n'
        if res:
            return f'{res}'

    def __is_misconfigured_xxss(self):
        if 'X-XSS-Protection' not in self.res_headers:
            return f' {self.RED}<-{self.WHITE}  X-XSS-Protection header is not set.'
        elif '1; mode=block' not in self.res_headers['X-XSS-Protection']:
            return f' {self.RED}<-{self.WHITE}  X-XSS-Protection header is misconfigured and set to: {self.res_headers["X-XSS-Protection"]}'

    def __is_misconfigured_xframe(self):
        if 'X-Frame-Options' not in self.res_headers:
            return f' {self.RED}<-{self.WHITE}  X-Frame-Options header is not set.'
        elif self.res_headers['X-Frame-Options'].lower() not in ('sameorigin', 'deny') :
            return f' {self.RED}<-{self.WHITE}  X-Frame-Options header is misconfigured and set to: {self.res_headers["X-Frame-Options"]}'

    def __is_misconfigured_csp(self):
        if 'Content-Security-Policy' not in self.res_headers:
            return f' {self.RED}<-{self.WHITE}  CSP protection is not implemented.'
        return f' {self.GREEN}<+  {self.res_headers["Content-Security-Policy"]}'

    def __are_cookies_configured(self):
        if 'set-cookie' in self.res_headers:
            cookies = self.res_headers['set-cookie'].split(',')
            res = ''
            for c in cookies:
                cres = f' {self.ORANGE}#{self.WHITE}   {c.strip()}\n'
                if 'HttpOnly' not in c:
                    cres += f' {self.RED}<-{self.WHITE}  The "HttpOnly" flag is not set.\n'
                if 'Secure' not in c:
                    cres += f' {self.RED}<-{self.WHITE}  The "Secure" flag is not set.\n'
                if 'SameSite=None' in c:
                    cres += f' {self.RED}<-{self.WHITE}  The "SameSite" property is set to "None".\n'
                res += cres + '\n'
            return res
    

    '''GraphQL'''
    def __to_pretty_json(self, dic):
        j = json.dumps(dic, sort_keys=True,)
                    # indent=4, separators=(',', ': '))
        j = j.replace(';', ';\n\t').replace('name', f'{self.ORANGE}name{self.WHITE}')
        return j

    def __get_graphql_schema(self, graphql_endpoint):
        introspection_query = {"query":"\n query IntrospectionQuery {\r\n __schema {\r\n queryType { name }\r\n mutationType { name }\r\n subscriptionType { name }\r\n types {\r\n ...FullType\r\n }\r\n directives {\r\n name\r\n description\r\n locations\r\n args {\r\n ...InputValue\r\n }\r\n }\r\n }\r\n }\r\n\r\n fragment FullType on __Type {\r\n kind\r\n name\r\n description\r\n fields(includeDeprecated: true) {\r\n name\r\n description\r\n args {\r\n ...InputValue\r\n }\r\n type {\r\n ...TypeRef\r\n }\r\n isDeprecated\r\n deprecationReason\r\n }\r\n inputFields {\r\n ...InputValue\r\n }\r\n interfaces {\r\n ...TypeRef\r\n }\r\n enumValues(includeDeprecated: true) {\r\n name\r\n description\r\n isDeprecated\r\n deprecationReason\r\n }\r\n possibleTypes {\r\n ...TypeRef\r\n }\r\n }\r\n\r\n fragment InputValue on __InputValue {\r\n name\r\n description\r\n type { ...TypeRef }\r\n defaultValue\r\n }\r\n\r\n fragment TypeRef on __Type {\r\n kind\r\n name\r\n ofType {\r\n kind\r\n name\r\n ofType {\r\n kind\r\n name\r\n ofType {\r\n kind\r\n name\r\n ofType {\r\n kind\r\n name\r\n ofType {\r\n kind\r\n name\r\n ofType {\r\n kind\r\n name\r\n ofType {\r\n kind\r\n name\r\n }\r\n }\r\n }\r\n }\r\n }\r\n }\r\n }\r\n }\r\n "}
        gres = requests.post(self.url_to_analize + graphql_endpoint, data=introspection_query, allow_redirects=False)
        if gres.status_code == 301:
            gres = requests.post(gres.headers['Location'], data=introspection_query)
        return self.__to_pretty_json(gres.json())

    def __test_graphql(self):
        for gep in self.GraphQL_ENDPOINTS:
            try:
                schema = self.__get_graphql_schema(gep)
                if schema:
                    return schema
            except Exception:
                pass

    def __print_test_result(self, test_name, test_res):
        if test_res:
            if test_name:
                print(f'\n {self.YELLOW}<|  {test_name}{self.WHITE}')
            print(test_res)

    def _analize_response(self, url):
        self.url_to_analize = url
        self.server_response = self._request(url)
        self.res_headers = self.server_response.headers

        print(f' <| Analizing {self.url_to_analize}\n')

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

        graphql_test_result = self.__test_graphql()
        
        self.__print_test_result(
            'GraphQL API',
            graphql_test_result if graphql_test_result else f' {self.CYAN}<X{self.WHITE}  GraphQL API wasn\'t detected..\n' )
