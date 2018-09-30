from pytatki.main import create_app
import pytest
from flask import jsonify


@pytest.fixture
def app():
    flask_app = create_app()

    @flask_app.route('/ping')
    def _ping():
        return jsonify(ping='pong')
    flask_app.debug = True
    return flask_app
