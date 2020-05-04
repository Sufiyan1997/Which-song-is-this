import json

configurations = None

with open('config.json') as config_file:
    configurations = json.load(config_file)

def get(name):
    keys = name.split(".")
    root = configurations
    for key in keys:
        root = root[key]
    return root