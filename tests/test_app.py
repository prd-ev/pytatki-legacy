from flask import url_for

class TestApp:

    def test_ping(self, client):
        res = client.get(url_for('_ping'))
        assert res.status_code == 200
        assert res.json == {'ping': 'pong'}
