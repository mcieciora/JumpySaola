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
def test_auth_functional__sing_up_logout(client):
    pass


@pytest.skip('To be implemented')
def test_auth_functional__sing_up_logout_login(client):
    pass


@pytest.skip('To be implemented')
def test_auth_functional__sing_up_logout(client):
    pass


@pytest.skip('To be implemented')
def test_auth_functional__sing_up_three_users_login_all(client):
    pass
