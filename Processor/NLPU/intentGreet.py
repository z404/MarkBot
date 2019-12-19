#Intent for when Mark computes a greeting
#Returns a random greeting back to the user

Name = "Greet"
Description = "Intent for when Mark computes a greeting"
Access = "Any"

def activator(slots):
    returndict = {'reserved':False,'return':"Hello! How do you do?"}
    return returndict
