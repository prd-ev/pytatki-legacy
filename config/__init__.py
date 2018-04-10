"""Plik konfiguracyjny"""
__author__ = 'Patryk Niedźwiedziński'

import ssl

class Config():
    """Config class"""
    secret_key = str()
    DEBUG = True
    HOST = "127.0.0.1"
    PORT = 5000
    EMAIL = ""
    EMAIL_PASSWORD = ""
    SSL_CONTEXT = ssl.SSLContext(ssl.PROTOCOL_SSLv23).load_cert_chain(
        '',
        '')


    def __init__(self, secret):
        self.secret_key = secret

    def is_ok(self):
        """Check if host and port are valid"""
        import socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex((self.HOST, self.PORT))
        if result==0:
            sock.close()
            return False
        else:
            sock.close()
            return True


CONFIG = Config("sekretny_klucz")
