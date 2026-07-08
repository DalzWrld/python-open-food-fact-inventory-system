import pytest

from app import create_app
from data import store


@pytest.fixture
def client():
    store.reset_store()
    app = create_app()
    app.config["TESTING"] = True

    with app.test_client() as test_client:
        yield test_client

    store.reset_store()
