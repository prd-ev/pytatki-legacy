from flask import url_for

class TestApp:

    def test_ping(self, client):
        res = client.get(url_for('_ping'))
        if not res.status_code == 200:
            raise AssertionError()
        if not res.json == {'ping': 'pong'}:
            raise AssertionError()
