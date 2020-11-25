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
#Importing nessesary packages
import json
import os
from snips_nlu import SnipsNLUEngine
from snips_nlu.dataset import dataset
from snips_nlu.default_configs import CONFIG_EN
from OUTPUT import IntentAssesment

print(l)

print('Initializing...')
engine = SnipsNLUEngine(config=CONFIG_EN)
data = dataset.Dataset.from_yaml_files('en',['./PROJECT-MARK/TRAIN/'+i for i in os.listdir('./PROJECT-MARK/TRAIN') if '.yaml' in i])
engine.fit(data)

def INPUT(text):
    parsing = engine.parse(text)
    IntentAssesment.output(parsing['intent'])
print('Done')

while True:
    a = input('Mark-> ')
    if a == 'quit': break
    INPUT(a)
