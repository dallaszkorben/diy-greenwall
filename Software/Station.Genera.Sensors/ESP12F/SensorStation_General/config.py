import ujson

CONFIG_FILE='level.config.json'
f=open(CONFIG_FILE, 'r')
config=ujson.loads(f.read())

def getValue(section, key):
    return config[section][key]