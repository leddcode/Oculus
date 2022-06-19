search_types = '''
 <: Options
    -----------------------------------------------
    1. Environments Discovery
    2. Directories Discovery
    3. Subdomains Discovery
    4. Mail Server DNS records and Emails Discovery
    _______________________________________________
'''

banner_digital = '''
+-+-+-+-+-+-+
|O|c|u|l|u|s|
+-+-+-+-+-+-+
'''

banner_speed = '''
                _______             ______
                __  __ \_________  ____  /___  _________
                _  / / /  ___/  / / /_  /_  / / /_  ___/
                / /_/ // /__ / /_/ /_  / / /_/ /_(__  )
                \____/ \___/ \__,_/ /_/  \__,_/ /____/

                v1.0.7
                By @enotr0n'''

solid_line = '''
_________________________________________________________________________
'''


class Helper:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    WHITE = '\033[0m'

    EXCEPT_CODES = (401, 403)

    @staticmethod
    def colour(code, status):
        if code == 200 and not status:
            return Helper.GREEN
        elif code in Helper.EXCEPT_CODES:
            return Helper.DARKCYAN
        return Helper.RED

    @staticmethod
    def status(code):
        if code not in Helper.EXCEPT_CODES:
            return 'Possible false positive!'
        return '' * 20
