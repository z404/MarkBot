from search_engine_parser import GoogleSearch

search_results = GoogleSearch()
search_results = search_results.search("itzcozofzak")
for i in search_results:
    print(i['titles'])
print(search_results)