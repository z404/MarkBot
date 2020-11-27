import random
def output(intentname,slots):

    if intentname[1] == 'Normal':
        outputchoice = ['Hi','Hello','Hello there, General Kenobi']
        return random.choice(outputchoice)

    if intentname[1] == 'WithQuestion':
        outputchoice = ['I\'m great! Thank\'s for asking :)','I\'m fantastic!' ]
        return random.choice(outputchoice)

    if intentname[1] == 'AskNameOfAI':
        if slots == []: return 'My name is Mark'
        else:
            name = ''
            for i in slots:
                if i['entity'] == 'username':
                    name = i['value']['value']
            return 'Hi '+name+'! I\'m Mark!'

    if intentname[1] == 'WithName':
        if slots != []:
            name = ''
            for i in slots:
                if i['entity'] == 'username':
                    name = i['value']['value']
            return 'Hi '+name+'! I\'m Mark!'
        else: return 'I could\'t understand that'