import json

def load_information(key):
    f = open('doc\print_info.json',)
    data = json.load(f)
   
    if key:
        data = [x for x in data if x['modelo'] == key or x['ip'] == key or x['nombre'] == key or x['sise'] == key ]
    f.close()
    return data