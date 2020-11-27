def output(intent):
    import os
    try:
        intentname = intent['intentName'].split('_')
        mod = __import__('OUTPUT.'+intentname[0])
        func = getattr(mod,intentname[0])
        return func.output(intentname)
    except ModuleNotFoundError:
        return 'Sorry, I couldn\'t understand that.'
   