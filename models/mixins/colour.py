import sys

import colorama


class Colour:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    NONBOLD = '\033[0m'
    UNDERLINE = '\033[4m'
    WHITE = '\033[0m'
    ORANGE = '\033[33m'
    CLEAR = '\033[K'

    if sys.platform.startswith('win'):
        try:
            colorama.init()
        except Exception:
            PURPLE = ''
            CYAN = ''
            DARKCYAN = ''
            BLUE = ''
            GREEN = ''
            YELLOW = ''
            RED = ''
            BOLD = ''
            NONBOLD = ''
            UNDERLINE = ''
            WHITE = ''
            ORANGE = ''
            CLEAR = ''

    EXCEPT_CODES = (401, 403, 409)

    def colour_code(self, code, status):
        if status == 'possible false positive':
            return Colour.RED
        elif code in Colour.EXCEPT_CODES:
            return Colour.DARKCYAN
        return Colour.GREEN

    def colour_status(self, code):
        if code not in Colour.EXCEPT_CODES:
            return 'possible false positive'
        return ''
    
    def p_plain(self, s):
        return f"{self.BOLD}{self.WHITE}[{s}]{self.WHITE}{self.NONBOLD}"
    
    def p_info(self, s):
        return f"{self.BOLD}{self.BLUE}[{s}]{self.WHITE}{self.NONBOLD}"
    
    def p_warn(self, s):
        return f"{self.BOLD}{self.YELLOW}[{s}]{self.WHITE}{self.NONBOLD}"
    
    def p_fail(self, s):
        return f"{self.BOLD}{self.RED}[{s}]{self.WHITE}{self.NONBOLD}"
    
    def p_succ(self, s):
        return f"{self.BOLD}{self.GREEN}[{s}]{self.WHITE}{self.NONBOLD}"
