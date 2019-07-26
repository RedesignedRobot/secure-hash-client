import requests
import json
import urllib.parse as urlparse
from urllib.parse import urlencode
import pymongo
from tqdm import tqdm

db_ip = "192.168.100.118"
hash_ip = "192.168.100.118"

db_endpoint = "mongodb://dev:fsx12amir@"+db_ip+"/dev"
hash_endpoint = "http://"+hash_ip+"/hash"
# hash_endpoint = "http://hash-service.eastus2.azurecontainer.io/hash"


myclient = pymongo.MongoClient(db_endpoint)
mydb = myclient["dev"]
mycol = mydb["cb"]


def get_url_with_params(p):
    url = hash_endpoint
    url_parts = list(urlparse.urlparse(url))
    query = dict(urlparse.parse_qsl(url_parts[4]))
    query.update(p)
    url_parts[4] = urlencode(query)
    url = urlparse.urlunparse(url_parts)
    return url


def create_params(text):
    return {'rounds': '10', 'text': str(text)}


for x in tqdm(mycol.find()):
    country = str(x["Country Name"])
    response = requests.get(get_url_with_params(p = create_params(country)))
    js = json.loads(response.text)
    # print(country + " :: " + js["hash"])
