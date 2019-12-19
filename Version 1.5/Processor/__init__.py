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
'''
Main Processing program for commandline project mark

Features to be implemented for initialization:
--> When initialized, make a database (sqlite3) of all available commands, permission role, package name and help
'''

def prRed(skk): print("\033[91m{}\033[00m" .format(skk)) 
def prGreen(skk): print("\033[92m{}\033[00m" .format(skk)) 
def prYellow(skk): print("\033[93m{}\033[00m" .format(skk)) 
def prLightPurple(skk): print("\033[94m{}\033[00m" .format(skk)) 
def prPurple(skk): print("\033[95m{}\033[00m" .format(skk)) 
def prCyan(skk): print("\033[96m{}\033[00m" .format(skk)) 
def prLightGray(skk): print("\033[97m{}\033[00m" .format(skk))

import os
import sqlite3
os.system('clear')
prPurple('+++++++++++++++++++++++')
prPurple('Starting Configuration!')
prPurple('+++++++++++++++++++++++')
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
prPurple('+++++++++++++++++++++++')
prPurple('Completed Configuration!')
prPurple('+++++++++++++++++++++++')
input()
os.system('clear')

