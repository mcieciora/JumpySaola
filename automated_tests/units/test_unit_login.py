def test_auth_login__wrong_pin_code(client_users_setup):
    response = client_users_setup.post('/login', data=dict(username='user1', pin_code='1224'), follow_redirects=True)
    assert response.status_code == 200, f'Expected response status code: 200, actual: {response.status_code}'
    assert '<strong>Warning!</strong> Incorrect pin code, try again.' in response.data.decode(), \
        f'Application shall not login user who provided wrong credentials\n{response.data}'


def test_auth_login__empty_login(client_users_setup):
    response = client_users_setup.post('/login', data=dict(username='', pin_code='1234'), follow_redirects=True)
    assert response.status_code == 200, f'Expected response status code: 200, actual: {response.status_code}'
    assert '<strong>Warning!</strong> Username does not exist.' in response.data.decode(), \
        f'Application shall not login user that does not exist\n{response.data}'


def test_auth_login__empty_pin_code(client_users_setup):
    response = client_users_setup.post('/login', data=dict(username='user1', pin_code=''), follow_redirects=True)
    assert response.status_code == 200, f'Expected response status code: 200, actual: {response.status_code}'
    assert '<strong>Warning!</strong> Incorrect pin code, try again.' in response.data.decode(), \
        f'Application shall not login user who provided wrong credentials\n{response.data}'


def test_auth_login__empty_credentials(client_users_setup):
    response = client_users_setup.post('/login', data=dict(username='', pin_code=''), follow_redirects=True)
    assert response.status_code == 200, f'Expected response status code: 200, actual: {response.status_code}'
    assert '<strong>Warning!</strong> Username does not exist.' in response.data.decode(), \
        f'Application shall not login user that does not exist\n{response.data}'