def output(intent,slots):
    import os
    try:
        intentname = intent['intentName'].split('_')
        mod = __import__('OUTPUT.'+intentname[0])
        func = getattr(mod,intentname[0])
        return func.output(intentname,slots)
    except ModuleNotFoundError:
        return 'Sorry, I couldn\'t understand that.'
    except AttributeError:
        return 'Sorry, I couldn\'t understand that.'