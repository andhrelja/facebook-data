import json

def read_json(path):
    with open(path, encoding='utf8') as json_file:
        return json.load(json_file)

def write_json(path, obj):
    with open(path, 'w', encoding='utf8') as f:
        json.dump(obj, f, ensure_ascii=False, indent=4)

def read_initial_json(path):
    with open(path, 'r', encoding='utf8') as json_file:
        content = json.load(json_file)
        dumps = json.dumps(content, ensure_ascii=False)
        _bytes = bytes(dumps, 'latin-1')
        return json.loads(_bytes.decode('utf8'))
