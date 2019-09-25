import pyrebase
import json
from colorama import init as i, Fore, deinit as di
i(autoreset = True)

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

def start_server():
    def stream_handler(message):
        pass
    my_stream = db.child('anish').stream(stream_handler)
    print(Fore.GREEN+'Server started sucsessfully!')

