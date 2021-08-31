import pytest
from src.website import create_app, db, auth


@pytest.fixture(scope='function')
def app_empty():
    app = create_app()
    with app.app_context():
        db.create_all()
        with app.test_client() as client:
            yield client
        db.drop_all()


@pytest.fixture(scope='function')
def app_basic():
    app = create_app()
    with app.app_context():
        db.create_all()
        new_user = auth.User(username="user1", pin_code="1234")
        db.session.add(new_user)
        db.session.commit()
        with app.test_client() as client:
            yield client
        db.drop_all()
