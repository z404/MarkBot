import random
def output(intentname):
    if intentname[1] == 'Normal':
        outputchoice = ['Hi','Hello','Hello there, General Kenobi']
        return random.choice(outputchoice)
    if intentname[1] == 'WithQuestion':
        outputchoice = ['I\'m great! Thank\'s for asking :)','I\'m fantastic!' ]
        return random.choice(outputchoice)