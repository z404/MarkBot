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
            #get path, number, role, banned
            command = message['data']
            path = message['path']
            path_lst = path.split('/')
            if len(path_lst)>2 and 'input' in path and command != 'blank':
                userid = path_lst[1]
                user_details = db.child('user_database').child(userid).get()
                banned = user_details.val()['banned']
                role = user_details.val()['role']
                path_to_log_file = 'Firebase/logs/LOGUSER'+userid+'.txt'
                with open(path_to_log_file,'a') as f:
                    f.write('\n>>> '+command)
                if banned == 'true':
                    output = 'You have been banned from this service. Please contact an administrator to resolve this issue.'
                else:
                    #if role == 'administrator':
                    try:
                        code, *params = command.split()
                    except:
                        code = command
                        params = []
                    if code == 'input' or code == 'inp' or code == 'nlp' or code == 'nlpu':
                        string = ''
                        for i in params:
                            string+=i+' '
                        string.rstrip(' \n')
                        output = process.get(string,origin='fire')
                    else:
                        output = c.execute(code,params,origin='fire',role=role)
                with open(path_to_log_file,'a') as f:
                    f.write('\n<<< '+output)
                db.child('user_database').child(userid).child('room').update({'output':output})
                db.child('user_database').child(userid).child('room').update({'input':'blank'})
        my_stream = db.child('user_database').stream(stream_handler)
        print(Fore.GREEN+'Server started sucsessfully!')
    else:
        try:
            my_stream.close()
        except AttributeError:
            pass
