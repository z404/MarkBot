l = '''

  _____           _           _     __  __          _____  _  __
 |  __ \         (_)         | |   |  \/  |   /\   |  __ \| |/ /
 | |__) | __ ___  _  ___  ___| |_  | \  / |  /  \  | |__) | ' / 
 |  ___/ '__/ _ \| |/ _ \/ __| __| | |\/| | / /\ \ |  _  /|  <  
 | |   | | | (_) | |  __/ (__| |_  | |  | |/ ____ \| | \ \| . \ 
 |_|   |_|  \___/| |\___|\___|\__| |_|  |_/_/    \_\_|  \_\_|\_\\
                _/ |                                            
               |__/                                             
'''

#first find os, and specify commands for each

#Display Logo and initialize the ENTIRE PROGRAM
from System_Compat import command as c
try:
    import colorama
    import nltk
except:
    c.exec
import NLPU


