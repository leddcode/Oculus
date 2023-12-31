from models.mixins.colour import Colour

search_types = f'''{Colour.p_warn(Colour, 'INIT')} Enumeration Options                
       -------------------
       1 Environments Discovery                      
       2 Directories Discovery                       
       3 Subdomains Discovery                        
       4 Mail Server DNS records and Emails Discovery
       5 S3 Buckets                                  
       6 Azure Blob Containers                       
       7 Firebase Databases                        
       8 GCP Buckets                          
       9 General Information and Misconfigurations   
'''

version = 'v1.2.39'
credit = ''

banner_digital = '''
+-+-+-+-+-+-+
|O|c|u|l|u|s|
+-+-+-+-+-+-+
'''

banner_speed = f''' {Colour.ORANGE}
* * * * * * * * * * * * * * * * * * * * * * * * * * *
*                                                   *
*      _______             ______      {version}      *
*      __  __ \_________  ____  /___  _________     *
*      _  / / /  ___/  / / / / /_  / / /_  ___/     *
*      / /_/ // /__ / /_/ / / / / /_/ /_(__  )      *
*      \____/ \___/ \__,_/ /_/  \__,_/ /____/       *
*                                                   *
*      Domain OSINT                                 *
*      By @leddcode                                 *
*                                                   *
* * * * * * * * * * * * * * * * * * * * * * * * * * *
{Colour.WHITE}'''

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

banners = [banner_speed]