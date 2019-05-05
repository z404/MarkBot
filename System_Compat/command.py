##run commands on the system's shell

def get_platform():
    with open("System_Compat/preferences.txt","r") as f:
        line = f.readline()
        print("hii")
        garbage, platform = line.split('=')
        platform = platform.strip().replace('"','')
        return platform

import os
pf = get_platform()

def exec(code,
