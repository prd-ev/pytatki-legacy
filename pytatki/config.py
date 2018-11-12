"""Module for loading configuration file"""
import json


def parse_config(filename, check_email=False, check_uwsgi=False, check_db_configuration=True):
    with open(filename) as fp:
        config = json.load(fp)
    if 'DEFAULT' not in config:
        print("No DEFAULT section")
        return False
    if 'DATABASE' not in config:
        print("Database configuration not found")
        return False
    if 'EMAIL' not in config:
        print("Email configuration not found")
        if check_email:
            return False
    if 'IDENTIFIERS' not in config:
        print("Run init_db.py to setup database")
        if check_db_configuration:
            return False
    config.update({"HOST": "{}:{}".format(
        config["DEFAULT"]["HOST"], config["DEFAULT"]["PORT"])})
    return config


if __name__ == '__main__':
    parse_config('config.json')
