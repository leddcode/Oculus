from models.mixins.colour import Colour

search_types = '''
 <: Enumeration Options
    -----------------------------------------------
    1. Environments Discovery
    2. Directories Discovery
    3. Subdomains Discovery
    4. Mail Server DNS records and Emails Discovery
    5. S3 Buckets
    6. Azure Blob Containers
    7. Firebase Databases
    8. Server Response Misconfigurations
    _______________________________________________
'''

version = 'v1.1.17'
credit = 'By @leddcode'

banner_digital = '''
+-+-+-+-+-+-+
|O|c|u|l|u|s|
+-+-+-+-+-+-+
'''

banner_speed = f'''
                _______             ______
                __  __ \_________  ____  /___  _________
                _  / / /  ___/  / / /_  /_  / / /_  ___/
                / /_/ // /__ / /_/ /_  / / /_/ /_(__  )
                \____/ \___/ \__,_/ /_/  \__,_/ /____/

                {version}
                {credit}'''


banner_bloody = f'''{Colour.RED}

           ▒█████   ▄████▄   █    ██  ██▓     █    ██   ██████ 
          ▒██▒  ██▒▒██▀ ▀█   ██  ▓██▒▓██▒     ██  ▓██▒▒██    ▒ 
          ▒██░  ██▒▒▓█    ▄ ▓██  ▒██░▒██░    ▓██  ▒██░░ ▓██▄   
          ▒██   ██░▒▓▓▄ ▄██▒▓▓█  ░██░▒██░    ▓▓█  ░██░  ▒   ██▒
          ░ ████▓▒░▒ ▓███▀ ░▒▒█████▓ ░██████▒▒▒█████▓ ▒██████▒▒
          ░ ▒░▒░▒░ ░ ░▒ ▒  ░░▒▓▒ ▒ ▒ ░ ▒░▓  ░░▒▓▒ ▒ ▒ ▒ ▒▓▒ ▒ ░
            ░ ▒ ▒░   ░  ▒   ░░▒░ ░ ░ ░ ░ ▒  ░░░▒░ ░ ░ ░ ░▒  ░ ░
          ░ ░ ░ ▒  ░         ░░░ ░ ░   ░ ░    ░░░ ░ ░ ░  ░  ░  
              ░ ░  ░ ░         ░         ░  ░   ░           ░  
                   ░ {Colour.WHITE}                              
          {version}
          {credit}'''

banner_ansi = f'''{Colour.GREEN}

          ██████╗   ██████╗██╗   ██╗██╗     ██╗   ██╗███████╗
          ██╔═══██╗██╔════╝██║   ██║██║     ██║   ██║██╔════╝
          ██║   ██║██║     ██║   ██║██║     ██║   ██║███████╗
          ██║   ██║██║     ██║   ██║██║     ██║   ██║╚════██║
          ╚██████╔╝╚██████╗╚██████╔╝███████╗╚██████╔╝███████║
           ╚═════╝  ╚═════╝ ╚═════╝ ╚══════╝ ╚═════╝ ╚══════╝
{Colour.WHITE}
          {version}
          {credit}'''


solid_line = '''
_________________________________________________________________________
'''

banners = [banner_speed, banner_bloody, banner_ansi]