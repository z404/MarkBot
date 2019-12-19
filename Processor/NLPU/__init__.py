'''
================================================
Natural Language Processing Unit of Project Mark
================================================

---------------------
Initializing the NLPU
---------------------

Checks to perform:
--> Check for en download
--> Create database of callable commands and intents
'''
#importing required modules
import subprocess, os, json
import sqlite3

#Colours
def prRed(skk): print("\033[91m{}\033[00m" .format(skk)) 
def prGreen(skk): print("\033[92m{}\033[00m" .format(skk)) 
def prYellow(skk): print("\033[93m{}\033[00m" .format(skk)) 
def prLightPurple(skk): print("\033[94m{}\033[00m" .format(skk)) 
def prPurple(skk): print("\033[95m{}\033[00m" .format(skk)) 
def prCyan(skk): print("\033[96m{}\033[00m" .format(skk)) 
def prLightGray(skk): print("\033[97m{}\033[00m" .format(skk))

#checking for installed modules
try:
    prCyan("----------------")
    prCyan("Configuring NLPU")
    prCyan("----------------")
    import snips_nlu
    from snips_nlu import SnipsNLUEngine
    from snips_nlu.default_configs import CONFIG_EN
    nlu_engine = SnipsNLUEngine(config=CONFIG_EN)
    with open(os.getcwd()+'/Processor/NLPU/testdataset.json') as f:
        js = json.load(f)
        nlu_engine = nlu_engine.fit(js)
        nlu_engine.parse('Mark is learning everyday')
    prGreen('NLPU Download configured sucsessfullly')
except:
    prYellow('NLPU not configured properly. Installing packages..')
    try:os.system('python3 -m snips_nlu download en')
    except:
        try: os.system('py3 -m snips_nlu download en')
        except:
            try: os.system('python -m snips_nlu download en')
            except: os.system('py -m snips_nlu download en')
    prGreen('Download and initialization complete')

#Create file with list of commands
connection = sqlite3.connect("Processor/NLPU/intent_database")
crsr = connection.cursor()
def update_table():
    dirs = os.listdir(os.getcwd()+'/Processor/NLPU')
    dirs = [i for i in dirs if "intent" in i]
    intents = [i.replace('intent','').replace('.py','') for i in dirs if i != 'intent_database']
    crsr.execute("select name from intent_data")
    intent_in_table = list(crsr.fetchall())
    intent_in_table = [i[0] for i in intent_in_table]
    for i in intents:
        if i not in intent_in_table:
            exec('import Processor.NLPU.intent'+i+' as e\nglobal e')
            Name = e.Name
            Desc = e.Description
            Access = e.Access
            crsr.execute('select max(sl_no) from intent_data')
            num = crsr.fetchall()[0]
            if num[0] == None:
                num = 0
            else:
                num = num[0]
            crsr.execute('insert into intent_data values('+str(num+1)+',"'+Name+'","'+Desc+'","'+Access+'")')
    connection.commit()
try:
    crsr.execute("create table intent_data(sl_no integer not null primary key, name varchar(30), desc varchar(100), access_control varchar(30))")
    update_table()
except:
    update_table()
prGreen('NLPU Database updated sucsessfully!')
