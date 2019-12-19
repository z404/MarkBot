#Intent for when Mark computes a greeting
#Returns a random greeting back to the user

Name = "GreetWithName"
Description = "Intent for when Mark computes a greeting with a name in it"
Access = "Any"

def activator(slots):
    if len(slots)>=1:
        if slots[0]['entity'] == 'name':
            greetname = slots[0]['rawValue']
        else:
            greetname = 'user'
        returndict = {'reserved':False,'return':"Hello, "+greetname+"! I'm Mark! Nice to meet you!"}
        return returndict
    else:
        returndict = {'reserved':False,'return':"Hi! Nice to meet you!"}
        return returndict
