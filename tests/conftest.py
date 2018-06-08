from main import create_app
import pytest
from flask import jsonify

@pytest.fixture
def app():
    APP = create_app()
    @APP.route('/ping')
    def ping():
        return jsonify(ping='pong')
    APP.debug = True
    return APP