def test_functional_sing_up__unregistered(logger, client):
    """
        Covers: T-REQ9, T-REQ10
    """
    response = client.post("/signup", data=dict(username="user1", pin_code_1="1234", pin_code_2="1234"),
                           follow_redirects=True)
    logger.info(response.data)
    assert response.status_code == 200, f'Expected response status code: 200, actual: {response.status_code}'
    assert '<strong>Success!</strong> Account created!' in response.data.decode(), \
        f'Application shall sign up user who provided proper credentials\n{response.data}'


def test_functional_sing_up__unauthorised(logger, client_users_setup):
    """
        Covers: T-REQ10, T-REQ11
    """
    response = client_users_setup.post("/signup", data=dict(username="user1", pin_code_1="1234", pin_code_2="1234"),
                                       follow_redirects=True)
    logger.info(response.data)
    assert response.status_code == 200, f'Expected response status code: 200, actual: {response.status_code}'
    assert '<strong>Warning!</strong> User already exists.' in response.data.decode(), \
        f'Application shall not accept creating two exactly the same accounts\n{response.data}'


def test_functional_sing_up__logged_in(logger, client_logged_in_user):
    """
        Covers: T-REQ12
    """
    response = client_logged_in_user.post("/signup", data=dict(username="user1", pin_code_1="1234", pin_code_2="1234"),
                                          follow_redirects=True)
    logger.info(response.data)
    assert response.status_code == 200, f'Expected response status code: 200, actual: {response.status_code}'
    assert '<strong>Warning!</strong> You are already logged in!' in response.data.decode(), \
        f'Application shall not sign up user who is already logged\n{response.data}'
