"""Test of application"""
from flask import url_for


def test_ping(client):
    """Tests if application works"""
    res = client.get(url_for('_ping'))
    if not res.status_code == 200:
        raise AssertionError()
    if not res.json == {'ping': 'pong'}:
        raise AssertionError()
