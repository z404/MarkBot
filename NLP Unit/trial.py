def get_prefs(name='all'):

        '''
        ----------------
        Load Preferences
        ----------------
        '''
        dict_prefs = {}  #key is name of preferance, value is preferance value
        with open('preferences.txt','r') as f:
            for line in f:
                pref_name, pref_val = line.split('=')
                pref_name, pref_val = pref_name.strip(), pref_val.strip().replace('"','')
                if name == 'all' or pref_name == name:
                    dict_prefs.update({pref_name:pref_val})
            f.close()
            if name == 'all':
                return dict_prefs
            else:
                try: return dict_prefs[name]
                except KeyError: return {name:'error'} 
