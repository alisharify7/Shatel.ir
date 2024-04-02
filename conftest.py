import pytest
from shatelCore import create_app
from shatelCore.extensions import db

@pytest.fixture()
def app():
    """ Flask Main Application """
    app = create_app()
    app.testing = True
    app.config["SERVER_NAME"] = "localhost:5000"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"

    with app.app_context():
        db.create_all()

    yield app


@pytest.fixture()
def client(app):
    """ Simple client for testing Flask application """
    yield app.test_client()



