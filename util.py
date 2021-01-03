import configparser
import json

def get_config():
    config = configparser.ConfigParser()
    config.read("config.ini")
    return config