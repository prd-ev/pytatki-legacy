from configparser import ConfigParser


def parse_config(filename, check_email=False, check_uwsgi=False):
    config = ConfigParser()
    with open(filename) as fp:
        config.read_file(fp, source='config.ini')
    print(config)
    config.sections()
    if 'DEFAULT' not in config:
        print("No DEFAULT section")
        return None
    if 'uwsgi' in config:
        print("uwsgi configuration found - you can run it with `uwsgi --ini config.ini`")
        if check_uwsgi:
            return None
    if 'DATABASE' not in config:
        print("Database configuration not found")
        return None
    if 'EMAIL' not in config:
        print("Email configuration not found")
        if check_email:
            return None
    if 'IDENTIFIERS' not in config:
        print("Run init_db.py to setup database")
        return None
    return config


if __name__ == '__main__':
    parse_config('../config.ini')