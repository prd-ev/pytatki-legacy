"""Managing security"""
from itsdangerous import URLSafeTimedSerializer
from pytatki.main import CONFIG

__author__ = "Patryk Niedźwiedziński"


ts = URLSafeTimedSerializer(CONFIG['DEFAULT']['secret_key'])
