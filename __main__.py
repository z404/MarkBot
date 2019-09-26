l = '''\
██████╗ ██████╗  ██████╗      ██╗███████╗ ██████╗████████╗    
██╔══██╗██╔══██╗██╔═══██╗     ██║██╔════╝██╔════╝╚══██╔══╝   
██████╔╝██████╔╝██║   ██║     ██║█████╗  ██║        ██║      
██╔═══╝ ██╔══██╗██║   ██║██   ██║██╔══╝  ██║        ██║       
██║     ██║  ██║╚██████╔╝╚█████╔╝███████╗╚██████╗   ██║      
╚═╝     ╚═╝  ╚═╝ ╚═════╝  ╚════╝ ╚══════╝ ╚═════╝   ╚═╝       

            ███╗   ███╗ █████╗ ██████╗ ██╗  ██╗
            ████╗ ████║██╔══██╗██╔══██╗██║ ██╔╝
            ██╔████╔██║███████║██████╔╝█████╔╝ 
            ██║╚██╔╝██║██╔══██║██╔══██╗██╔═██╗ 
            ██║ ╚═╝ ██║██║  ██║██║  ██║██║  ██╗
            ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝
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
import Firebase

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
from Firebase import server
#Start commandline
command = ' '
status = 'Mark>> '
while command:
    command = input(Fore.GREEN+status+Fore.BLUE)
    try:
        code, *params = command.split()
    except:
        command = ' '
        continue
    if command != '':
        ret_type = c.execute(code,params)
        if ret_type[0] == 1:
            print(ret_type[1])
        if ret_type[0] == 'nlpu':
            print(process.get(ret_type[1]))
        elif ret_type[0] == 'server_start':
            server.start_server()
        elif ret_type[0] == 'quit':
            server.start_server(0)
            exit(0)
    else:
        break
'''----------------------------------------------------------------------------------------------'''
