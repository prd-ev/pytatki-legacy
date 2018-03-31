'''Plik konfiguracyjny'''
__author__ = 'Patryk Niedźwiedziński'

class Localhost:
    '''Do testowania na komputerze lokalnym'''
    secret_key = str()
    DEBUG = True
    HOST = "127.0.0.1"
    PORT = 5000

    def __init__(self, secret):
        self.secret_key = secret

    def is_ok(self):
        '''Sprawdza czy dane poprawne'''
        import socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex((self.HOST, self.PORT))
        if result==0:
            sock.close()
            return False
        else:
            sock.close()
            return True

class Server:
    '''Do uruchamiania na serwerze'''
    secret_key = str()
    DEBUG = True
    HOST = "127.0.0.1"
    PORT = 80

    def __init__(self, secret):
        self.secret_key = secret

    def is_ok(self):
        '''Sprawdza czy dane poprawne'''
        import socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex((self.HOST, self.PORT))
        if result==0:
            sock.close()
            return False
        else:
            sock.close()
            return True


CONFIG = Localhost("sekretny_klucz")
