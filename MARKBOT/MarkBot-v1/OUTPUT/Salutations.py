import random
def output(intentname,slots):

    if intentname[1] == 'Normal':
        outputchoice = ['Wogay den, bye *yeets*','Alright, see ya around','Aw, leaving already? Bye :(','See ya!']
        return random.choice(outputchoice)
