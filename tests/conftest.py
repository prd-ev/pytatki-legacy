from main import create_app
import pytest
from flask import jsonify


@pytest.fixture
def app_fixture():
    app = create_app()

    @app.route('/ping')
    def _ping():
        return jsonify(ping='pong')
    app.debug = True
    return app
