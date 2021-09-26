from os import remove
import pytest
from src.website import create_app, create_database
import logging


@pytest.fixture
def logger():
    logging.basicConfig(level=logging.INFO)
    return logging.getLogger()


@pytest.fixture
def app():
    app = create_app()
    with app.app_context():
        create_database(app)
    yield app
    remove('src/website/db/database.db')


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
    client_logged_in_user.post('/settings', data={'category_name': 'category_plus', 'category_limit': '150'})

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


@pytest.fixture
def client_without_history(client_with_transactions):
    client_with_transactions.post('/', data={'transaction_value': '25', 'transaction_desc': 'shopping',
                                             'transaction_category': 'category',
                                             'transaction_outcome': None})
    yield client_with_transactions


@pytest.fixture
def client_with_history(client_without_history):
    client_without_history.post('/settings', data=dict(category_name=None, category_limit=None, period_name=None),
                                follow_redirects=True)
    yield client_without_history


def sign_up(logger, this_client, data):
    response = this_client.post("/signup", data=data, follow_redirects=True)
    logger.info(response.data)
    assert response.status_code == 200, f'Expected response status code: 200, actual: {response.status_code}'
    assert '<strong>Success!</strong> Account created!' in response.data.decode(), \
        f'Application shall sign up user who provided proper credentials\n{response.data}'
    return response


def log_in(logger, this_client, data):
    response = this_client.post('/login', data=data, follow_redirects=True)
    logger.info(response.data)
    assert response.status_code == 200, f'Expected response status code: 200, actual: {response.status_code}'
    assert '<strong>Success!</strong> Logged in successfully!' in response.data.decode(), \
        f'Application shall log in user who exists and provided correct pin code\n{response.data}'
    return response


def log_out(logger, this_client):
    response = this_client.get('/logout', follow_redirects=True)
    logger.info(response.data)
    assert response.status_code == 200, f'Expected response status code: 200, actual: {response.status_code}'
    assert 'Success!</strong> Logged out!' in response.data.decode(), \
        f'Application shall logout user at request\n{response.data}'
    return response


def add_category(logger, this_client, data):
    response = this_client.post('/settings', data=data, follow_redirects=True)
    logger.info(response.data)
    assert response.status_code == 200, f'Expected response status code: 200, actual: {response.status_code}'
    assert '<strong>Success!</strong> Category added!' in response.data.decode(), \
        f'Application shall accept category addition while no period is active\n{response.data}'
    return response


def edit_category(logger, this_client, data, category_id):
    response = this_client.post(f'/edit_category/{category_id}', data=data, follow_redirects=True)
    logger.info(response.data)
    assert response.status_code == 200, f'Expected response status code: 200, actual: {response.status_code}'
    assert '<strong>Success!</strong> Category was updated!' in response.data.decode(), \
        f'Application shall update values of given category\n{response.data}'
    return response


def delete_category(logger, this_client, category_id):
    response = this_client.post(f'/delete_category/{category_id}', follow_redirects=True)
    logger.info(response.data)
    assert response.status_code == 200, f'Expected response status code: 200, actual: {response.status_code}'
    assert '<strong>Success!</strong> Category was deleted successfully!' in response.data.decode(), \
        f'Application shall delete category at user request\n{response.data}'
    return response


def start_period(logger, this_client, data):
    response = this_client.post('/settings', data=data, follow_redirects=True)
    logger.info(response.data)
    assert response.status_code == 200, f'Expected response status code: 200, actual: {response.status_code}'
    assert '<strong>Success!</strong> Period started!' in response.data.decode(), \
        f'Application shall start period with given name\n{response.data}'
    return response


def stop_period(logger, this_client):
    response = this_client.post('/settings', data=dict(category_name=None, category_limit=None, period_name=None),
                                follow_redirects=True)
    logger.info(response.data)
    assert response.status_code == 200, f'Expected response status code: 200, actual: {response.status_code}'
    assert '<strong>Success!</strong> Period finished!' in response.data.decode(), \
        f'Application shall finish period at user request\n{response.data}'
    return response


def add_transaction(logger, this_client, data):
    response = this_client.post('/', data=data, follow_redirects=True)
    logger.info(response.data)
    assert response.status_code == 200, f'Expected response status code: 200, actual: {response.status_code}'
    assert '<strong>Success!</strong> Transaction added!' in response.data.decode(), \
        f'Application shall add transaction that was passed with proper data\n{response.data}'
    return response


def edit_transaction(logger, this_client, data, transaction_id):
    response = this_client.post(f'/edit_transaction/{transaction_id}', data=data, follow_redirects=True)
    logger.info(response.data)
    assert response.status_code == 200, f'Expected response status code: 200, actual: {response.status_code}'
    assert '<strong>Success!</strong> Transaction was updated!' in response.data.decode(), \
        f'Application shall allow to edit transaction that was passed with proper data\n{response.data}'
    return response


def delete_transaction(logger, this_client, transaction_id):
    response = this_client.post(f'/delete_transaction/{transaction_id}', follow_redirects=True)
    logger.info(response.data)
    assert response.status_code == 200, f'Expected response status code: 200, actual: {response.status_code}'
    assert '<strong>Success!</strong> Transaction was deleted successfully!' in response.data.decode(), \
        f'Application shall delete transaction at user request\n{response.data}'
    return response
