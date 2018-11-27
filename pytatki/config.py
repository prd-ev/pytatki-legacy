"""This module is used to load configuration file."""

import json

from pytatki import __version__ as version

__author__ = u"Patryk Niedźwiedziński"
__copyright__ = "Copyright 2018, Pytatki"
__credits__ = []
__license__ = "MIT"
__version__ = version
__maintainer__ = u"Patryk Niedźwiedziński"
__email__ = "pniedzwiedzinski19@gmail.com"
__status__ = "Production"


def generate_host(hostname: "(str) Name of host",
                  port: "(int) Number of port",
                  https=False):
    """Generates host url."""
    try:
        host = "http{}://" + hostname
    except TypeError:
        raise TypeError("`hostname` should be str")
    if https:
        host = host.format('s')
    else:
        host = host.format('')
        if host != 80:
            host += ':' + str(port)
    return host


def parse_config(filename, check_uwsgi=False, check_db_configuration=True):
    with open(filename) as fp:
        config = json.load(fp)
    if 'default' not in config:
        raise Warning("No default section in config")
    if 'database' not in config:
        raise Warning("Database configuration not found")
    if 'email' not in config:
        raise Warning("Email configuration not found")
    if 'identifiers' not in config:
        if check_db_configuration:
            raise Warning("Run init_db.py to setup database")
    host = generate_host(config["default"]["host"], config["default"]
                         ["port"], https=config["default"]["https"])
    config.update({"host": host})
    return config
