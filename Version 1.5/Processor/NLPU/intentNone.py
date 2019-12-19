#Intent for when Mark cannot understand what you said
#Just returns "Sorry, I didn't understand that"

Name = "None"
Description = "Intent for when Mark cannot associate an intent with what you said"
Access = "Any"

def activator(slots):
    returndict = {'reserved':False,'return':"Sorry, I didn't understand that"}
    return returndict
