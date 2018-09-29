from configparser import ConfigParser, MissingSectionHeaderError, ParsingError


def parse_config(check_email=False, check_uwsgi=False):
    config = ConfigParser()
    try:
        with open('config.ini') as fp:
            config.read_file(fp, source='config.ini')
    except MissingSectionHeaderError:
        print("You have missing section header in your config.ini file")
        return None
    except ParsingError:
        print("You have syntax error in your config.ini file")
        return None
    except FileNotFoundError:
        print("Couldn't find config.ini file")
        return None
    print(config)
    config.sections()
    if 'uwsgi' in config:
        print("uwsgi configuration found - you can run it with `uwsgi --ini config.ini")
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
    parse_config()