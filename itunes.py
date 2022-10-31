import requests
import sys
import json

if len(sys.argv) !=2:
    sys.exit()

response=requests.get("https://itunes.apple.com/search?entity=song&limit=50&term=" + sys.argv[1])
#print(json.dumps(response.json(), indent=2))

o=response.json()
for result in o["results"]:
    # o["results"] es una lista de dicc. y result es un dicc.
    print(result["trackName"])