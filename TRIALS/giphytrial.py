with open('creds.txt') as file:
    apikey = file.readlines()[3].rstrip('\n')

import giphy_client as gc
from giphy_client.rest import ApiException
from random import randint

api_instance = gc.DefaultApi()
api_key = apikey
query = 'stonks'
fmt = 'gif'

try:
    response = api_instance.gifs_search_get(api_key,query,limit=1,offset=randint(1,10),fmt=fmt)
    gif_id = response.data[0]
    print(gif_id.images.downsized.url)
except ApiException:
    print("Exception when calling DefaultApi->gifs_search_get: %s\n" % e)