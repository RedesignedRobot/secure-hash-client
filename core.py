import requests
import json
import platform
import urllib.parse as urlparse
from urllib.parse import urlencode
from tabulate import tabulate
import pymongo
from tqdm import tqdm
from flask import Flask, request, jsonify

app = Flask(__name__)
app.config['ENV'] = 'development'
app.config['DEBUG'] = True

db_ip = ""
hash_ip = ""

if platform.system() == 'Windows':
    db_ip = "192.168.100.118"
    hash_ip = "192.168.100.118"
else:
    db_ip = "localhost"
    hash_ip = "localhost"

db_endpoint = "mongodb://dev:password@" + db_ip + "/dev"
hash_endpoint = "http://" + hash_ip + "/hash"


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


@app.route('/hash-client/run')
def origin():
    result_set = []
    rounds = request.args.get('rounds', default = 10, type = int)
    attribute = request.args.get('attribute', default = "Language", type = str)
    key = request.args.get('key', default = "ar", type = str)
    for x in tqdm(mycol.find({attribute: key})):
        country = str(x["Country Name"])
        response = requests.get(get_url_with_params(p = create_params(rounds, country)))
        js = json.loads(response.text)
        sub_list = [str(country), str(js["hash"])]
        result_set.append(sub_list)
    return tabulate(result_set, headers = ['Country', 'Hash'], tablefmt = "html")


if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = 80)
