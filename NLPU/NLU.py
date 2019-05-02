'''
================================================
Natural Language Processing Unit of Project Mark
================================================
'''

'''
---------------------
Initializing the NLPU
---------------------
'''

print("Initializing NLPU for Project Mark")
import sys, os, time

#Check to see if nltk is installed
try: import nltk
except ImportError: print("ImportError: Module NLTK hasn't been installed. Please install the module to continue")

#import sub-requirement files
import prefs

#check to see if all nltk_data is present
try:
    from nltk import word_tokenize
    from nltk.corpus import stopwords
    set(stopwords.words('english'))
    word_tokenize("Checking for Packages")
    print("Directory for downloaded packages found!")
    print("Initialization complete, ready for use")
except LookupError:
    print("The preloaded nltk packages are missing at the runtime directory.")
    print("Checking Preferences file")
    #check preferences for path to nltk_data
    path_to_nltk_data = prefs.get('path_to_nltk_data')
    if path_to_nltk_data == '':
        print("Path not recorded on preferences file")
        print("Please Enter the path of the folder nltk_data below")
        print("If the packages haven't been downloaded, input a space and hit enter")
        def dir_input():
            choice = input("Path to nltk_data >>")
            if choice.isspace():
                print("Warning: This takes about 42 MB of data") #citation needed!
                print("Please enter the path at which to download the data")
                print("If you want to download the data to the current directory, enter space")
                nltk_data_directory = input("Path to download nltk_data >>")
                if nltk_data_directory.isspace():
                    nltk_data_directory = os.path.dirname(os.path.abspath(__file__))+"\\nltk_data"
                    try: os.mkdir(nltk_data_directory)
                    except FileExistsError:
                        print("Error, nltk_data under this directory already exists, please delete and try again")
                        dir_input()
                else:
                    if os.path.exists(nltk_data_directory):
                        os.mkdir(nltk_data_directory+"\\nltk_data")
                        nltk_data_directory = nltk_data_directory+"\\nltk_data"
                    else:
                        print("Error, directory doesn't exist, please enter a different one!")
                        dir_input()
                print("Download starting, please do not interupt")
                print("This will take a while....")
                time.sleep(5)
                nltk.download("punkt",nltk_data_directory)
                nltk.download("stopwords",nltk_data_directory)
                print("download complete!")
                print("Setting path in preference file")
                prefs.set('path_to_nltk_data',nltk_data_directory)
                print("Verifying download.....")
                time.sleep(3)
                nltk.data.path.append(nltk_data_directory)
                word_tokenize("Checking for Packages")
                set(stopwords.words('english'))
                print("Directory for downloaded packages found!")
                print("Initialization complete, ready for use")
            else:
                if choice.replace(choice.replace('nltk_data',''),'') == '':
                    print("Error, please paste the directory of the nltk_data")
                    dir_input()
                elif not os.path.exists(choice):
                    print("Error, Directory doesn't exist")
                    dir_input()
                else:
                    try:
                        nltk.data.path.append(choice)
                        word_tokenize("Checking for Packages")
                        set(stopwords.words('english'))
                        print("Directory for downloaded packages found!")
                        print("Adding path to preferences")
                        prefs.set('path_to_nltk_data',choice)
                        print("Initialization complete, ready for use")
                    except LookupError:
                        print("Error, Broken Download, please download again!")
                        os.remove(os.path.dirname(os.path.abspath(__file__))+'/preferences.txt')
                        nltk.data.path.pop()
        dir_input()
    else:
        if not os.path.exists(path_to_nltk_data):
            print("Error, preference path doesnt exist, resetting preference: path")
            os.remove(os.path.dirname(os.path.abspath(__file__))+'/preferences.txt')
            raise LookupError
        else:
            nltk.data.path.append(path_to_nltk_data)
            try:
                word_tokenize("Checking for Packages")
                set(stopwords.words('english'))
                print("Directory for downloaded packages found!")
                print("Initialization complete, ready for use")
            except LookupError:
                print("Error, Broken Download, please download again!")
                nltk.data.path.pop()
                raise LookupError
        #as this is set by the script, it should be correct, verify and move on, if wrong delete pref and reruns
