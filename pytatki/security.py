"""This module contains all security stuff"""

from itsdangerous import URLSafeTimedSerializer

from pytatki import __version__ as version
from pytatki.main import CONFIG

__author__ = u"Patryk Niedźwiedziński"
__copyright__ = "Copyright 2018, Pytatki"
__credits__ = []
__license__ = "MIT"
__version__ = version
__maintainer__ = u"Patryk Niedźwiedziński"
__email__ = "pniedzwiedzinski19@gmail.com"
__status__ = "Production"


ts = URLSafeTimedSerializer(CONFIG['default']['secret_key'])
