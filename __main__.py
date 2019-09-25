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

'''-----------------------------------------------------------------------------------------------'''
#Display Logo and initialize the ENTIRE PROGRAM
from System import command as c
c.execute('clear')
import time
try:
    import colorama
    import nltk
    import snips_nlu
except:
    print("Requirements not installed!")
    print("Installing requirements....")
    time.sleep(3)
    c.execute("install")

from colorama import init as i, Fore, deinit as di
i(autoreset = True)
print(Fore.CYAN + "--------------------------\
                \n       Initializing\
                \n--------------------------")
time.sleep(2)

#make all print statements yellow
import NLPU

print(Fore.CYAN + "--------------------------\
                \n    Done Initializing!\
                \n--------------------------")
input()
c.execute('clear')
c.execute('l')
platform = c.get_platform()
if platform!='Linux':
    print(Fore.RED+'Operating system not supported, limited functionality')
from NLPU import process
#Start commandline
command = ' '
status = 'Mark>> '
while command:
    command = input(Fore.GREEN+status+Fore.BLUE)
    code, *params = command.split()
    if command != '':
        ret_type = c.execute(code,params)
        if ret_type[0] == 'nlpu':
            print(process.get(ret_type[1]))
    else:
        break
'''----------------------------------------------------------------------------------------------'''
