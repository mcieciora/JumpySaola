from os import remove
import pytest
from src.website import create_app, create_database


@pytest.fixture
def app():
    app = create_app()
    with app.app_context():
        create_database(app)
    yield app
    remove('../../src/website/db/database.db')


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def client_users_setup(client):
    for user, pin_code in {'user1': '1234', 'user2': '2233', 'userX': '0990'}.items():
        client.post('/signup', data={'username': user, 'pin_code_1': pin_code, 'pin_code_2': pin_code})

    yield client


@pytest.fixture
def client_logged_in_user(client):
    client.post('/signup', data={'username': 'user1', 'pin_code_1': '1234', 'pin_code_2': '1234'})
    client.post('/login', data={'username': 'user1', 'pin_code': '1234'})

    yield client


@pytest.fixture
def client_with_categories(client_logged_in_user):
    client_logged_in_user.post('/settings', data={'category_name': 'category', 'category_limit': '100'})

    yield client_logged_in_user


@pytest.fixture
def client_with_period(client_with_categories):
    client_with_categories.post('/settings', data={'period_name': 'new_period'})

    yield client_with_categories


@pytest.fixture
def client_with_transactions(client_with_period):
    client_with_period.post('/', data={'transaction_value': '25', 'transaction_desc': 'shopping',
                                       'transaction_category': 'category',
                                       'transaction_outcome': 'transaction_outcome'})

    yield client_with_period
