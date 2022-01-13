# %%

import requests
import random
import time
import argparse 
import pathlib
import fnmatch

 

def send_request(url, body, key=None):
    start = time.time_ns()
    headers = {"content-type":"application/json"}
    if key is not None:
        headers["Authorization"]= "Bearer "+key
    
    resp = requests.post(url, data=body, headers=headers)
    elapsed = (time.time_ns() - start) / 1000000
    print("POST {} {} - {}ms".format(url, resp.status_code, elapsed))
    if resp.status_code != 200:
        print(resp.text)
    return resp

def infer(base_url, model_name, file, key): 
    with open(file, "r") as f:
        req_body = f.read()   
        url = "{}/v2/models/{}/infer".format(base_url, model_name)
        send_request(url, req_body, key)

def unload(base_url, model_name, key): 
    url = "{}/v2/repository/models/{}/unload".format(base_url, model_name)
    send_request(url, None, key)


def load(base_url, model_name, key ): 
    url = "{}/v2/repository/models/{}/load".format(base_url, model_name)
    send_request(url, None, key)



parser = argparse.ArgumentParser(description='Send infer request.')
parser.add_argument('--base',  type=str,  default="http://localhost:9000",
                    help='number of request')
 
parser.add_argument('model', type=str, default=None)
parser.add_argument('--request-file', type=pathlib.Path, default=None)

parser.add_argument('--action', type=str, default='infer')
parser.add_argument('--key', type=str, default=None)


args = parser.parse_args()

def model_index(base_url, key):
    r = requests.get(base_url+"/v2/repository/index", headers = {"Authorization": "Bearer "+key})
    return r.json()["models"]

models = model_index(args.base, args.key)



if args.action == 'infer':
    model_names = fnmatch.filter([m["name"] for m in models], args.model)
    while True: 
        i = random.randrange(0, len(model_names))
        model_name = model_names[i]    
        infer(args.base, model_name, args.request_file, args.key)
elif args.action == 'unload':
    model_names = fnmatch.filter([m["name"]  for m in models if m["state"] == "Ready"], args.model)
    for model_name in model_names:
        unload(args.base, model_name, args.key)
elif args.action == 'load':
    model_names = fnmatch.filter([m["name"]  for m in models if m["state"] != "Ready"], args.model)
    for model_name in model_names:
        load(args.base, model_name, args.key)