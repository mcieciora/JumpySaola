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
def test_auth_signup__new_user(client):
    pass


@pytest.skip('To be implemented')
def test_auth_signup__existing_user(client):
    pass


@pytest.skip('To be implemented')
def test_auth_signup__too_short_username(client):
    pass


@pytest.skip('To be implemented')
def test_auth_signup__too_short_pin_code(client):
    pass


@pytest.skip('To be implemented')
def test_auth_signup__not_matching_pin_codes(client):
    pass
