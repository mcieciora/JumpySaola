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
def test_transaction_add__empty_transaction_outcome(client):
    pass


@pytest.skip('To be implemented')
def test_transaction_add__empty_transaction_description(client):
    pass


@pytest.skip('To be implemented')
def test_transaction_add__empty_transaction_value(client):
    pass


@pytest.skip('To be implemented')
def test_transaction_add__positive_transaction_value(client):
    pass


@pytest.skip('To be implemented')
def test_transaction_add__too_short_description(client):
    pass


@pytest.skip('To be implemented')
def test_transaction_add__wrong_value_variable_type(client):
    pass


@pytest.skip('To be implemented')
def test_transaction_add__add_outcome(client):
    pass


@pytest.skip('To be implemented')
def test_transaction_add__add_income(client):
    pass
