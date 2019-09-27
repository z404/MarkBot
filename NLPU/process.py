'''
================================================
Natural Language Processing Unit of Project Mark
================================================
'''
import json, os
from snips_nlu import SnipsNLUEngine
from snips_nlu.default_configs import CONFIG_EN
nlu_engine = SnipsNLUEngine(config=CONFIG_EN)
from colorama import init as i, Fore, deinit as di
i(autoreset = True)
#dataset = train.yaml

yaml_path = os.path.join(os.path.dirname(__file__),'train.yaml')
json_path = os.path.join(os.path.dirname(__file__),'train.json')

try: os.system('python3 -m snips_nlu generate-dataset en '+yaml_path+' > '+json_path)
except:
    try: os.system('py3 -m snips_nlu generate-dataset en '+yaml_path+' > '+json_path)
    except:
        try: os.system('python -m snips_nlu generate-dataset en '+yaml_path+' > '+json_path)
        except: os.system('py -m snips_nlu generate-dataset en '+yaml_path+' > '+json_path)
with open(json_path) as f:
    json_f = json.load(f)
    trained_nlu_engine = nlu_engine.fit(json_f)

def process_intent(ret_lst,origin):
    
    if ret_lst[0] == None:
        if origin == 'main':
            return Fore.MAGENTA+'I\'m sorry, I didn\'t understand that'
        else:
            return 'I\'m sorry, I didn\'t understand that'

    elif ret_lst[0] == 'askNameOfAI':
        if origin == 'main':
            return Fore.MAGENTA+'My name is Mark!'
        else:
            return 'My name is Mark!'

def rectify(return_json):
    name_of_intent = return_json['intent']['intentName']
    probability = return_json['intent']['probability']
    slots = return_json['slots']
    return [name_of_intent,probability,slots]

def get(text, origin='main'):
    ret = trained_nlu_engine.parse(text)
    rect_ret = rectify(ret)
    output = process_intent(rect_ret,origin)
    return output

    
