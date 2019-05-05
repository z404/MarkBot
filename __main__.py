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
from System_Compat import command as c
c.execute('clear')
import time
try:
    import colorama
    import nltk
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
input()
'''----------------------------------------------------------------------------------------------'''
