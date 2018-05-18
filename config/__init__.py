"""Plik konfiguracyjny"""
__author__ = 'Patryk Niedzwiedzinski'

class Config():
    """Config class"""
    secret_key = str()
    DEBUG = True
    HOST = "127.0.0.1"
    PORT = 5000
    EMAIL = ""
    EMAIL_PASSWORD = ""

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
