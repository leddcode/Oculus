class Colour:
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

    def colour_code(self, code, status):
        if code == 200 and not status:
            return Colour.GREEN
        elif code in Colour.EXCEPT_CODES:
            return Colour.DARKCYAN
        return Colour.RED

    def colour_status(self, code):
        if code not in Colour.EXCEPT_CODES:
            return 'Possible false positive!'
        return '' * 20
