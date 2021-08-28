import pytest
from src.website import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True

    with app.app_context():
        with app.test_client() as client:
            yield client


@pytest.mark.skip('To be implemented')
def test_auth_login__no_such_username(client):
    pass


@pytest.mark.skip('To be implemented')
def test_auth_login__wrong_password(client):
    pass


@pytest.mark.skip('To be implemented')
def test_auth_login__empty_login(client):
    pass


@pytest.mark.skip('To be implemented')
def test_auth_login__empty_password(client):
    pass


@pytest.mark.skip('To be implemented')
def test_auth_login__empty_credentials(client):
    pass


@pytest.mark.skip('To be implemented')
def test_auth_login__correct_credentials(client):
    pass


@pytest.mark.skip('To be implemented')
def test_auth_logout__logout(client):
    pass
