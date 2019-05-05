import os,sys,time
dict_prefs = {}  #key is name of preference, value is preference value
if not os.path.exists(os.path.dirname(os.path.abspath(__file__))+'\\preferences.txt'):
    print("Creating preferences.txt")
    with open ('NLPU/preferences.txt','w+') as f:
        f.write('''path_to_nltk_data = ""''')
with open('NLPU/preferences.txt','r') as f:
    for line in f:
        pref_name, pref_val = line.split('=')
        pref_name, pref_val = pref_name.strip(), pref_val.strip().replace('"','')
        dict_prefs.update({pref_name:pref_val})
    f.close()
    
def get(name_of_pref = 'all'):
    if name_of_pref == 'all':
        return dict_prefs
    else:
        try: return dict_prefs[name_of_pref]
        except KeyError: return 'error'
        
def set(name_of_pref,val):
    print("{",name_of_pref,':',val,'}')
    write_string = ''
    dict_prefs.update({name_of_pref:val})
    for key,value in dict_prefs.items():
        write_string += key+' = "'+value+'"'
    write_string.strip()
    with open('NLPU/preferences.txt','w') as f:
        f.write(write_string)
