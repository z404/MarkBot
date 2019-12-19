#Intent for when Mark cannot understand what you said
#Just returns "Sorry, I didn't understand that"

#Access restrictions: None
#origin: Any
#triggers: Undefined
#reservations: None
def activator(slots):
    returndict = {'reserved':False,'return':"Sorry, I didn't understand that"}
    return returndict
