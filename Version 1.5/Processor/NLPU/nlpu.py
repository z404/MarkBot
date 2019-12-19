'''
================================================
Natural Language Processing Unit of Project Mark
================================================
'''
import json, subprocess, os
from snips_nlu import SnipsNLUEngine
from snips_nlu.default_configs import CONFIG_EN

## Generate the dataset
nlu_engine = SnipsNLUEngine(config=CONFIG_EN)

yaml_path = os.path.join(os.path.dirname(__file__),'train.yaml')
json_path = os.path.join(os.path.dirname(__file__),'train.json')

try:
    a = os.system('python3 -m snips_nlu generate-dataset en '+yaml_path+' > '+json_path)
except:
    try: os.system(['py3','-m','snips_nlu','generate-dataset','en',yaml_path,'>',json_path])
    except:
        try: os.system(['python','-m','snips_nlu','generate-dataset','en',yaml_path,' > ',json_path])
        except: os.system(['py','-m','snips_nlu','generate-dataset','en',yaml_path,'>',json_path])

reserved = False
reserving_intent = None

# Train the dataset  
with open(json_path) as f:
    json_f = json.load(f)
    trained_nlu_engine = nlu_engine.fit(json_f)

#Intent Processor
def process_intent(ret_lst,origin):
    global reserved,reserving_intent
    ##find intent file and pass it to activator function
    intentname = str(ret_lst[0])
    slots = ret_lst [2]
    dirs = os.listdir()
    dirs = [i for i in dirs if 'intent' in i]
    intents = [i.replace('intent','').replace('.py','') for i in dirs]
    if reserved == True:
        reserved == False
        command = 'import intent'+reserving_intent+'.activator as activate'
        exec(command)
        returncommand = activate(slots)
        if returncommand['reserved']==True:
            reserved = True
        return returncommand['return']
    else:
        command = 'import intent'+intentname+' as activate\nglobal activate'
        exec(command)
        returncommand = activate.activator(slots)
        if returncommand['reserved']==True:
            reserved = True
            reserving_intent = intentname
        return returncommand['return']
#Send request here
def get(text, origin='main'):
    return_json = trained_nlu_engine.parse(text)
    name_of_intent = return_json['intent']['intentName']
    probability = return_json['intent']['probability']
    slots = return_json['slots']
    rect_ret =  [name_of_intent,probability,slots]
    output = process_intent(rect_ret,origin)
    return output

    
