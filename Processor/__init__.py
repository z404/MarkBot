'''
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

Main Processing program for commandline project mark

Features to be implemented for initialization:
--> When initialized, make a database (sqlite3) of all available commands, permission role, package name and help
'''

import os
import sqlite3
os.system('clear')
## Get all packages' names
if __name__ == '__main__':
    files = os.listdir(os.getcwd())
else:
    files = os.listdir(os.getcwd()+'/Processor')
packages = []
for i in files:
    if '__' == i[:2]:
        pass
    else:
        packages.append(i)
## Import all the packages
for i in packages:
    exec('import Processor.'+i)



