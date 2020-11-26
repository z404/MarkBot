def output(intent):
    import os
    try:
        intentname = intent['intentName'].split('_')
        mod = __import__('OUTPUT.'+intentname[0])
        func = getattr(mod,intentname[0])
        func.output(intentname)
    except ModuleNotFoundError:
        print('Sorry, I couldn\'t understand that.')
   