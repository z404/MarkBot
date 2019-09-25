'''
================================================
Natural Language Processing Unit of Project Mark
================================================
'''
import json, os
from snips_nlu import SnipsNLUEngine
from snips_nlu.default_configs import CONFIG_EN
nlu_engine = SnipsNLUEngine(config=CONFIG_EN)
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

def get(text):
    ret = trained_nlu_engine.parse(text)
    return ret
