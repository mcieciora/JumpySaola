def test_functional_delete_history__unauthorised(logger, client):
    """
        Covers: T-REQ109, T-REQ110
    """
    response = client.post('/delete_period/1', follow_redirects=True)
    logger.info(response.data)
    assert response.status_code == 200, f'Expected response status code: 200, actual: {response.status_code}'
    assert '<strong>Success!</strong> Please log in to access this page.' in response.data.decode(), \
        f'Application shall not allow unauthorised user to delete category\n{response.data}'


def test_functional_delete_category__registered(logger, client_with_history):
    """
        Covers: T-REQ111, T-REQ112, T-REQ118
    """
    response = client_with_history.post('/delete_period/1', follow_redirects=True)
    logger.info(response.data)
    assert response.status_code == 200, f'Expected response status code: 200, actual: {response.status_code}'
    assert '<strong>Success!</strong> Period was deleted successfully!' in response.data.decode(), \
        f'Application shall delete category at user request\n{response.data}'


def test_functional_delete_history__no_history(logger, client_without_history):
    """
        Covers: T-REQ111, T-REQ112, T-REQ115
    """
    response = client_without_history.post('/delete_period/1')
    logger.info(response.data)
    assert response.status_code == 302, f'Expected response status code: 200, actual: {response.status_code}'
    assert '<strong>Warning!</strong> There is no such period ID!' in response.data.decode(), \
        f'Application shall inform user there is no such period to delete\n{response.data}'
