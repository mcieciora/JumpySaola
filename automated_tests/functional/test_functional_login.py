def test_functional_login__unregistered(client):
    """
        Covers: T-REQ1
    """
    response = client.post('/login', data=dict(username='user1', pin_code='1234'), follow_redirects=True)
    assert response.status_code == 200, f'Expected response status code: 200, actual: {response.status_code}'
    assert '<strong>Warning!</strong> Username does not exist.' in response.data.decode(), \
        f'Application shall not login user who does not exist\n{response.data}'


def test_functional_login__unauthorised(client_users_setup):
    """
        Covers: T-REQ2, T-REQ3
    """
    response = client_users_setup.post('/login', data=dict(username='user1', pin_code='1234'), follow_redirects=True)
    assert response.status_code == 200, f'Expected response status code: 200, actual: {response.status_code}'
    assert '<strong>Success!</strong> Logged in successfully!' in response.data.decode(), \
        f'Application shall log in user who exists and provided correct pin code\n{response.data}'
    response = client_users_setup.get('/')
    assert response.status_code == 200, f'Expected response status code: 200, actual: {response.status_code}'
    assert '<h1 align="center">No active period! Go to settings and start one!</h1>' in response.data.decode(), \
        f'Application without started period shall return proper message\n{response.data}'


def test_functional_login__logged_in(client_logged_in_user):
    """
        Covers: T-REQ4
    """
    response = client_logged_in_user.post('/login', data=dict(username='user1', pin_code='1234'), follow_redirects=True)
    assert response.status_code == 200, f'Expected response status code: 200, actual: {response.status_code}'
    assert '<strong>Warning!</strong> You are already logged in!' in response.data.decode(), \
        f'Application shall not log in user who is already logged\n{response.data}'
