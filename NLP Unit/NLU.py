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
except ImportError: print("ImportError: Module NLTK hasn't been installed.\
               please install the module to continue")

#check to see if all nltk_data is present
try:
    from nltk import word_tokenize
    with open("preferences.txt","r") as preferences:
        path_to_nltk_data = preferences.readline().rstrip()
##        
##        if path_to_nltk_data[21:-1] == "":
##            print("No preference set for nltk_data. Checking default python directory....")
##            path_to_nltk_data = 
    word_tokenize("Checking for Packages")
except LookupError:
    print("The preloaded nltk packages are missing at the runtime directory.")
    print("Please Enter the path of the folder nltk_data below")
    print("If the packages haven't been downloaded, input a space and hit enter")
    choice = input("Path to nltk_data >>")
    if input.isWhitespace():
        print("Please enter the path at which to download the data")
        print("If you want to download the data to the current directory, enter space")
        nltk_data_directory = input("Path to download nltk_data >>")
        if nltk_data_directory.isWhitespace():
            nltk_data_directory = os.path.dirname(os.path.abspath(__file__))
        print("Download starting")
        print("This will take a while....")
        time.sleep(5)
        
