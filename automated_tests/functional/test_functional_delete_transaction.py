def test_functional_delete_transaction__unauthorised(logger, client):
    """
        Covers: T-REQ83, T-REQ84
    """
    response = client.post('/delete_transaction/1', follow_redirects=True)
    logger.info(response.data)
    assert response.status_code == 200, f'Expected response status code: 200, actual: {response.status_code}'
    assert '<strong>Success!</strong> Please log in to access this page.' in response.data.decode(), \
        f'Application shall not delete transaction if action was requested by unauthorised user\n{response.data}'


def test_functional_delete_transaction__registered(logger, client_with_transactions):
    """
        Covers: T-REQ85, T-REQ86, T-REQ88, T-REQ90
    """
    response = client_with_transactions.post('/delete_transaction/1', follow_redirects=True)
    logger.info(response.data)
    assert response.status_code == 200, f'Expected response status code: 200, actual: {response.status_code}'
    assert '<strong>Success!</strong> Transaction was deleted successfully!' in response.data.decode(), \
        f'Application shall delete transaction at user request\n{response.data}'


def test_functional_delete_transaction__no_transaction(logger, client_with_period):
    """
        Covers: T-REQ85, T-REQ86, T-REQ87, T-REQ88, T-REQ89
    """
    response = client_with_period.post('/delete_transaction/1', follow_redirects=True)
    logger.info(response.data)
    assert response.status_code == 200, f'Expected response status code: 200, actual: {response.status_code}'
    assert '<strong>Warning!</strong> There is no such transaction ID!' in response.data.decode(), \
        f'Application shall not add transaction if action was requested by unauthorised user\n{response.data}'
