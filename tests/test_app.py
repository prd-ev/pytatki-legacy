from main import create_app


def test_app():
    app = create_app()
    app.run()
