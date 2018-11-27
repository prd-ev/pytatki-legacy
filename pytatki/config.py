"""Module for loading configuration file"""
import json


def parse_config(filename, check_email=False, check_uwsgi=False, check_db_configuration=True):
    with open(filename) as fp:
        config = json.load(fp)
    if 'default' not in config:
        print("No default section")
        return False
    if 'database' not in config:
        print("Database configuration not found")
        return False
    if 'email' not in config:
        print("Email configuration not found")
        if check_email:
            return False
    if 'database' not in config:
        print("Run init_db.py to setup database")
        if check_db_configuration:
            return False
    if config["default"]["port"] == "80":
        config.update({"host": config["default"]["host"]})
    else:
        config.update({"host": "{}:{}".format(
            config["default"]["host"], config["default"]["port"])})
    return config


if __name__ == '__main__':
    parse_config('config.json')
