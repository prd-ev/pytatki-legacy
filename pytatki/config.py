from configparser import ConfigParser


def parse_config(filename, check_email=False, check_uwsgi=False, check_db_configuration=True):
    config = ConfigParser()
    with open(filename) as fp:
        config.read_file(fp, source='config.ini')
    config.sections()
    if 'DEFAULT' not in config:
        print("No DEFAULT section")
        return False
    if 'uwsgi' in config:
        print("uwsgi configuration found - you can run it with `uwsgi --ini config.ini`")
        if check_uwsgi:
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
    return config


if __name__ == '__main__':
    parse_config('../config.ini')