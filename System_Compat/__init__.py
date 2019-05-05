import platform

#detect platform
name = platform.system()
if "Windows" in name:
    print("Found Platorm Windows....")
    pf = "Windows"
elif "Linux" in name:
    print("Found Platform Linux....")
    pf = "Linux"
elif "Darwin" in name:
    print("Found Platform MacOSX....")
    print("Error! This script is built only for Linux and Windows Platforms!")
    raise OSError


#save Platform in preferences.txt
with open("System_Compat/preferences.txt","w+") as f:
    f.write('platform = "'+pf+'"')
    f.close()
