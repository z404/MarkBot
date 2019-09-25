'''
================================================
Natural Language Processing Unit of Project Mark
================================================
'''

'''
---------------------
Initializing the NLPU
---------------------
'''
#importing required modules
import sys, time, os, json

#pip install snips-nlu
#python -m snips_nlu download en

#checking for installed modules
try:
    import snips_nlu
    from snips_nlu import SnipsNLUEngine
    from snips_nlu.default_configs import CONFIG_EN
    nlu_engine = SnipsNLUEngine(config=CONFIG_EN)
    with open(r'NLPU/testdataset.json') as f:
        js = json.load(f)
        print('hi')
        nlu_engine = nlu_engine.fit(js)
        nlu_engine.parse('Mark is learning everyday')
    print('NLPU configured sucsessfullly')
except:
    print('NLPU not configured properly. Installing packages..')
    try:os.system('python3 -m snips_nlu download en')
    except:
        try: os.system('py3 -m snips_nlu download en')
        except:
            try: os.system('python -m snips_nlu download en')
            except: os.system('py -m snips_nlu download en')
    print('Download and initialization complete')
