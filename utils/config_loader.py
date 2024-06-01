import yaml
import os

def load_config(env='default'):
    with open('config.yaml', 'r') as file:
        config = yaml.safe_load(file)
    return config.get(env, config['default'])
