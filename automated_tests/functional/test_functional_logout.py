def test_functional_logout__unregistered(logger, client):
    """
        Covers: T-REQ5, T-REQ6
    """
    response = client.get('/logout', follow_redirects=True)
    logger.info(response.data)
    assert response.status_code == 200, f'Expected response status code: 200, actual: {response.status_code}'
    assert '<strong>Success!</strong> Please log in to access this page.' in response.data.decode(), \
        f'Application shall not log out user who is unregistered and unauthorised\n{response.data}'


def test_functional_logout__logged_in(logger, client_logged_in_user):
    """
        Covers: T-REQ7, T-REQ8
    """
    response = client_logged_in_user.get('/logout', follow_redirects=True)
    logger.info(response.data)
    assert response.status_code == 200, f'Expected response status code: 200, actual: {response.status_code}'
    assert 'Success!</strong> Logged out!' in response.data.decode(), \
        f'Application shall logout user at request\n{response.data}'
    response = client_logged_in_user.get('/logout', follow_redirects=True)
    logger.info(response.data)
    assert response.status_code == 200, f'Expected response status code: 200, actual: {response.status_code}'
    assert '<strong>Success!</strong> Please log in to access this page.' in response.data.decode(), \
        f'Application shall not log out user who is registered but unauthorised\n{response.data}'
