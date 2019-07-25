import requests
import json
import urllib.parse as urlparse
from urllib.parse import urlencode

params = {'rounds': '9', 'text': 'amir'}
url = "http://hash-service.eastus2.azurecontainer.io/hash"
url_parts = list(urlparse.urlparse(url))
query = dict(urlparse.parse_qsl(url_parts[4]))
query.update(params)
url_parts[4] = urlencode(query)
url = urlparse.urlunparse(url_parts)

for i in range(10):
    response = requests.get(url)
    js = json.loads(response.text)
    print(js["host_name"])

