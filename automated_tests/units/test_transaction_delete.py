import pytest
from src.website import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True

    with app.app_context():
        with app.test_client() as client:
            yield client


@pytest.skip('To be implemented')
def test_transaction_delete__delete_transaction(client):
    pass


@pytest.skip('To be implemented')
def test_transaction_delete__non_existing_transaction(client):
    pass


@pytest.skip('To be implemented')
def test_transaction_delete__other_user_transaction(client):
    pass
