import pyrebase
import json, sys, os

sys.path.append('../')

#original_stdout = sys.stdout
#sys.stdout = open(os.devnull,'w')
#from NLPU import process
#from System import command as c
#sys.stdout = original_stdout

with open("preferences.txt") as f:
    config = {}
    lst = f.readlines()
    for i in lst:
        prop, val = i.split(': ')
        prop = prop.rstrip(' "\n').lstrip(' "')
        val = val.rstrip(' "\n').lstrip(' "')
        config.update({prop:val})
firebase = pyrebase.initialize_app(config)

db = firebase.database()

db.child("user_database").update({3:{'name':'Dhrhduv','role':'administrator','email':'','banned':'false','room':{'input':'blank','output':'blank'}}})