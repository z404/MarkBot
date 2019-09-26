import pyrebase
import json, sys, os
from colorama import init as i, Fore, deinit as di
i(autoreset = True)

sys.path.append('../')

original_stdout = sys.stdout
sys.stdout = open(os.devnull,'w')
from NLPU import process
from System import command as c
sys.stdout = original_stdout

with open(r"Firebase/preferences.txt") as f:
    config = {}
    lst = f.readlines()
    for i in lst:
        prop, val = i.split(': ')
        prop = prop.rstrip(' "\n').lstrip(' "')
        val = val.rstrip(' "\n').lstrip(' "')
        config.update({prop:val})
firebase = pyrebase.initialize_app(config)

db = firebase.database()
count = 0
my_stream = ''

def start_server(code=1):
    global my_stream
    if code == 1:
        global count
        count=0
        def stream_handler(message):
            global count
            if count!=0:
                print(message)
                lst=message['path'].split('/')
                room_num = lst[1]
                try:
                    if lst[2] == 'input':
                        if message['data'] == 'blank':
                            #ignore
                            pass
                        else:
                            command = message['data']
                            try:
                                code, *params = command.split()
                            except:
                                command = ' '
                            if command != '':
                                ret_type = c.execute(code,params)
                                if ret_type[0] == 1:
                                    db.update({'output':ret_type[1]})
                                if ret_type[0] == 'nlpu':
                                    db.update({'output':process.get(ret_type[1])})
                            db.update({'input':'blank'})
                except: pass
            else: count+=1
        my_stream = db.child('rooms').stream(stream_handler)
        print(Fore.GREEN+'Server started sucsessfully!')
    else:
        my_stream.close()
