import json

def change(key,value):
    with open('config.json','r') as fin:
        config = json.load(fin)
    if isinstance(value, str):
        if 'toggle' in value:
            config[key] = not config[key]
        else:
            config[key] = value
    else:
        config[key] = not config[key]
    with open('config.json','w') as fout:
        fout.write(json.dumps(config))
    return config

def main():
    config = change('use_broker','toggle')
    print(config['use_broker'])

#----------------------------------------------
if __name__ == '__main__':
    main ()