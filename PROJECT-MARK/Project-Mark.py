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
#Importing packages required to run NLPU tasks 
from snips_nlu import SnipsNLUEngine
from snips_nlu.dataset import dataset
from snips_nlu.default_configs import CONFIG_EN
from OUTPUT import IntentAssesment
#Importing packages required for discord bot
import discord
import threading

with open('creds.txt') as file:
    TOKEN = file.read()

print(l)


print('Initializing...')
initlst = [False]#,False]

#Initializing NLP Engine
engine = SnipsNLUEngine(config=CONFIG_EN)
data = dataset.Dataset.from_yaml_files('en',['./PROJECT-MARK/TRAIN/'+i for i in os.listdir('./PROJECT-MARK/TRAIN') if '.yaml' in i])
engine.fit(data)
print('NLP Engine Initialized')
initlst[0] = True

#Initializing Discord connection
# client = discord.Client()
# @client.event
# async def on_ready(): #Defining methods for discord bot
#     print('Discord Module Initialized')
#     initlst[1] = True
# @client.event
# async def on_message(message):
#     if message.author.id != client.user.id:
#         if message.content.startswith('.'):
#             command = message.content.split()
#             if command[0].lower() == '.say' and len(command)>1:
#                 inputstr = ' '.join([i for i in command[1:]])
#                 a = INPUT(inputstr)
#                 await message.channel.send(a)
#mythread = threading.Thread(target=client.run,args=[TOKEN])
#mythread.daemon = True
#mythread.start()

#This is temporary code to test NLPU. Change after system is in place
def INPUT(text):
    parsing = engine.parse(text)
    try: slot = parsing['slots']
    except: slot = []
    return IntentAssesment.output(parsing['intent'],slot)

while True:
    if initlst.count(True) == len(initlst):
        a = input('Mark-> ')
        if a == 'quit':
            break
        print(INPUT(a))
