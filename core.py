import requests
import json
import platform
import urllib.parse as urlparse
from urllib.parse import urlencode
from tabulate import tabulate
import pymongo
from tqdm import tqdm
import click

db_ip = ""
hash_ip = ""

if platform.system() == 'Windows':
    db_ip = "192.168.100.118"
    hash_ip = "192.168.100.118"
else:
    db_ip = "localhost"
    hash_ip = "localhost"

db_endpoint = "mongodb://dev:fsx12amir@" + db_ip + "/dev"
hash_endpoint = "http://" + hash_ip + "/hash"
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


def create_params(rounds, text):
    return {'rounds': int(rounds), 'text': str(text)}


result_set = []


@click.command()
@click.option("--rounds", default = 4)
@click.option("--attribute", default = "Language")
@click.option("--key", default = "ar")
def origin(rounds, attribute, key):
    for x in tqdm(mycol.find({attribute: key})):
        country = str(x["Country Name"])
        response = requests.get(get_url_with_params(p = create_params(rounds, country)))
        js = json.loads(response.text)
        sub_list = [str(country), str(js["hash"])]
        result_set.append(sub_list)
    print()
    print(tabulate(result_set, headers = ['Country', 'Hash'], tablefmt = "html"))


if __name__ == '__main__':
    origin()
