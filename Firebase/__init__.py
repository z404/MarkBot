#initializing the firebase server
import platform, time, os
from colorama import init as i, Fore, deinit as di
i(autoreset = True)

#detect platform
def done():
    #checking to load config file
    import pyrebase
    config = {}
    try:
        with open(r"Firebase/preferences.txt") as f:
            lst = f.readlines()
            for i in lst:
                prop, val = i.split(': ')
                prop = prop.rstrip(' "').lstrip(' "')
                val = val.rstrip(' "').lstrip(' "')
                config.update({prop:val})
        firebase = pyrebase.initialize_app(config)
        print('Firebase configured sucsessfully')
    except Exception as e:
        print(Fore.RED+'Error: ',e)

        
name = platform.system()
if "Windows" in name:
    print("Found Platorm Windows....")
    try:
        import pyrebase
        done()
    except:
        print(Fore.RED+'ERROR: Pyrebase not installed, install it using pip. Windows users face problems while\
                installing pyrebase. Therefore, if pyrebase cannot be installed, this functionality cannot be used on Windows. \
                Other functions can still work properly')
elif "Linux" in name:
    #print("Found Platform Linux....")
    try:
        import pyrebase
        done()
    except:
        print("Pyrebase not installed, installing now...")
        try:
            os.system('pip3 install pyrebase')
        except:
            os.system('pip install pyrebase')
        done()
