import json, os

server_data = {}
keylist = {}
global DefData
DefData = {"channel": -1, "subscribed": "False", "license": -1, "key": -1}

def save():
    with open(f"configs.json", 'w') as fl:
        json.dump(server_data, fl, indent=2)

def load(guild):
    DefData = {"channel": -1, "subscribed": "False"}
    if os.path.exists(f"configs.json"):
        with open(f'configs.json', 'r') as fl:
            loaded = json.load(fl)
            print(loaded)
            if f"{guild.id}" in loaded:
                DefData = loaded[f"{guild.id}"]
    else:
        with open(f'configs.json', 'w') as fl:
            json.dump(DefData, fl)

    return DefData

def keys():
    if os.path.exists("keys.json"):
        with open("keys.json", 'r') as fl:
            return json.load(fl)

def update():
    with open("keys.json", 'w') as fl:
        json.dump(keylist, fl, indent=2)