'''
================================================
Natural Language Processing Unit of Project Mark
================================================
'''



class NLPU:
    def __init__(self):

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

        #check to see if all nltk_data is present
        try:
            from nltk import word_tokenize
            word_tokenize("Checking for Packages")
            print("Directory for downloaded packages found!")
        except LookupError:
            print("The preloaded nltk packages are missing at the runtime directory.")
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
                        nltk_data_directory = os.path.dirname(os.path.abspath(__file__))+"/nltk_data"
                        os.mkdir(nltk_data_directory)
                    else:
                        if os.path.exists(nltk_data_directory):
                            os.mkdir(nltk_data_directory+"/nltk_data")
                            nltk_data_directory = nltk_data_directory+"/nltk_data"
                        else:
                            print("Error, directory doesn't exist, please enter a different one!")
                            dir_input()
                    print("Download starting")
                    print("This will take a while....")
                    time.sleep(5)
                    nltk.download("punkt",nltk_data_directory)
                    nltk.download("stopwords",nltk_data_directory)
                    
                else:
                    with open("preferences.txt","r") as preferences:
                        path_to_nltk_data = preferences.readline().rstrip()
            dir_input()
NLPU()
