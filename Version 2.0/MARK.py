l = '''
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

#Imports
import os
import json
import snips_nlu
from snips_nlu import SnipsNLUEngine
from snips_nlu.default_configs import CONFIG_EN

def MAIN():
    prRed("Welcome to Project Mark! Please wait until the program has been initialized")
    initialize_mark()
    authorize_mark()

#Colours
def prRed(skk): print("\033[91m{}\033[00m" .format(skk)) 
def prGreen(skk): print("\033[92m{}\033[00m" .format(skk)) 
def prYellow(skk): print("\033[93m{}\033[00m" .format(skk)) 
def prLightPurple(skk): print("\033[94m{}\033[00m" .format(skk)) 
def prPurple(skk, end = '\n'): print("\033[95m{}\033[00m" .format(skk),end=end) 
def prCyan(skk): print("\033[96m{}\033[00m" .format(skk)) 
def prLightGray(skk): print("\033[97m{}\033[00m" .format(skk)) 

def initialize_mark():
    
    #Initializing NLPU
    try:
        prCyan("Configuring NLPU")
        nlu_engine = SnipsNLUEngine(config=CONFIG_EN)
        with open(os.getcwd()+'/testdataset.json') as f:
            js = json.load(f)
            nlu_engine = nlu_engine.fit(js)
            nlu_engine.parse('Mark is learning everyday')
        prGreen('NLPU configured sucsessfullly')
    except Exception as e:
        print(e)
        prYellow('NLPU not configured properly. Installing packages..')
        try:os.system('python3 -m snips_nlu download en')
        except:
            try: os.system('py3 -m snips_nlu download en')
            except:
                try: os.system('python -m snips_nlu download en')
                except: os.system('py -m snips_nlu download en')
        prGreen('Download and initialization completed sucsessfully')

    #Initialization complete
    prGreen('Initialization Complete! Press any key to continue


MAIN()
