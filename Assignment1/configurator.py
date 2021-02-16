import json, time

def change(key,value):
    with open('config.json','r') as fin:
        config = json.load(fin)
    oldVal = config[key]
    if isinstance(value, str):
        if 'toggle' in value:
            print('configurator toggling value')
            config[key] = not config[key]
        else:
            config[key] = value
    else:
        config[key] = value
    with open('config.json','w') as fout:
        fout.write(json.dumps(config, indent=4, sort_keys=True))
    print('Configurator changed',key,'from',oldVal,'to',config[key])
    return config

def load():
    config = None
    l = 0
    while config == None:
        try:
            with open('config.json','r') as fin:
                config = json.load(fin)
        except:
            time.sleep(.01)
            print('trying to load config file' , l)
            l += 1
    return config

def main():
    config = change('use_broker','toggle')
    print(config['use_broker'])

#----------------------------------------------
if __name__ == '__main__':
    main ()