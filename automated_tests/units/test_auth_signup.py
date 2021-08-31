from src.website.models import User


def test_auth_signup__new_user(db):
    response = db.post("/signup", data=dict(username="user1", pin_code_1="1234", pin_code_2="1234"),
                        follow_redirects=True)
    assert response.status_code == 200, f'Expected response status code: 200, actual: {response.status_code}'
    assert '<strong>Success!</strong> Account created!' in response.data.decode(), \
        f'New user sign up failed!\n{response.data}'


def test_auth_signup__too_short_username(app):
    response = app.post("/signup", data=dict(username="aa", pin_code_1="1234", pin_code_2="1234"),
                                follow_redirects=True)
    assert response.status_code == 200, f'Expected response status code: 200, actual: {response.status_code}'
    assert '<strong>Warning!</strong> User name length must be greater than 3 characters.' in response.data.decode(), \
        f'Application shall not accept username value length shorter than 3 characters\n{response.data}'


def test_auth_signup__too_short_pin_code(app):
    response = app.post("/signup", data=dict(username="user1", pin_code_1="123", pin_code_2="123"),
                                follow_redirects=True)
    assert response.status_code == 200, f'Expected response status code: 200, actual: {response.status_code}'
    assert '<strong>Warning!</strong> Password must be exactly 4 characters long.' in response.data.decode(), \
        f'Application shall not accept pin code value other than 4 characters long\n{response.data}'


def test_auth_signup__too_long_pin_code(app):
    response = app.post("/signup", data=dict(username="user1", pin_code_1="12345", pin_code_2="12345"),
                                follow_redirects=True)
    assert response.status_code == 200, f'Expected response status code: 200, actual: {response.status_code}'
    assert '<strong>Warning!</strong> Password must be exactly 4 characters long.' in response.data.decode(), \
        f'Application shall not accept pin code value other than 4 characters long\n{response.data}'


def test_auth_signup__not_matching_pin_codes(app):
    response = app.post("/signup", data=dict(username="user1", pin_code_1="1122", pin_code_2="2233"),
                                follow_redirects=True)
    assert response.status_code == 200, f'Expected response status code: 200, actual: {response.status_code}'
    assert '<strong>Warning!</strong> Passwords do not match.' in response.data.decode(), \
        f'Application shall not accept pin codes that do not match\n{response.data}'


def test_auth_signup__existing_user(app_basic):
    response = app_basic.post("/signup", data=dict(username="user1", pin_code_1="1234", pin_code_2="1234"),
                              follow_redirects=True)
    assert response.status_code == 200, f'Expected response status code: 200, actual: {response.status_code}'
    assert '<strong>Warning!</strong> User already exists.' in response.data.decode(), \
        f'Application shall not accept creating two exactly the same accounts\n{response.data}'
