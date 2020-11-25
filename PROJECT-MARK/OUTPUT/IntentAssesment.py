def output(intent):
    import os
    mod = __import__('OUTPUT.'+intent['intentName'])
    func = getattr(mod,intent['intentName'])
    func.output()
    
