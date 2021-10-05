import pytest


def test_functional_edit_transaction__unauthorised(logger, client):
    """
        Covers: T-REQ91, T-REQ92, T-REQ100, T-REQ101
    """
    response = client.post('/edit_transaction/1', data=dict(transaction_value='25', transaction_desc='shopping',
                                                            transaction_category='category',
                                                            transaction_outcome=None), follow_redirects=True)
    logger.info(response.data)
    assert response.status_code == 200, f'Expected response status code: 200, actual: {response.status_code}'
    assert '<strong>Success!</strong> Please log in to access this page.' in response.data.decode(), \
        f'Application shall not allow to edit transaction if action was requested by unauthorised user\n{response.data}'
    response = client.post('/edit_transaction/1', data=dict(transaction_value='25', transaction_desc='shopping',
                                                            transaction_category='category',
                                                            transaction_outcome='transaction_outcome'),
                           follow_redirects=True)
    logger.info(response.data)
    assert response.status_code == 200, f'Expected response status code: 200, actual: {response.status_code}'
    assert '<strong>Success!</strong> Please log in to access this page.' in response.data.decode(), \
        f'Application shall not allow to edit transaction if action was requested by unauthorised user\n{response.data}'


def test_functional_edit_transaction__registered(logger, client_with_transactions):
    """
        Covers: T-REQ93, T-REQ94, T-REQ96, T-REQ97, T-REQ99, T-REQ102, T-REQ103, T-REQ105, T-REQ106, T-REQ108
    """
    response = client_with_transactions.post('/edit_transaction/1', data=dict(transaction_value='25',
                                                                              transaction_desc='shopping',
                                                                              transaction_category='category',
                                                                              transaction_outcome=None),
                                             follow_redirects=True)
    logger.info(response.data)
    assert response.status_code == 200, f'Expected response status code: 200, actual: {response.status_code}'
    assert '<strong>Success!</strong> Transaction was updated!' in response.data.decode(), \
        f'Application shall allow to edit transaction that was passed with proper data\n{response.data}'
    response = client_with_transactions.post('/edit_transaction/1',
                                             data=dict(transaction_value='25', transaction_desc='shopping',
                                                       transaction_category='category',
                                                       transaction_outcome='transaction_outcome'),
                                             follow_redirects=True)
    logger.info(response.data)
    assert response.status_code == 200, f'Expected response status code: 200, actual: {response.status_code}'
    assert '<strong>Success!</strong> Transaction was updated!' in response.data.decode(), \
        f'Application shall allow to edit transaction that was passed with proper data\n{response.data}'


@pytest.mark.skip('Those REQs are covered by selenium tests')
def test_functional_edit_transaction__no_category(logger, client_with_transactions):
    """
        Covers: T-REQ93, T-REQ94, T-REQ95, T-REQ97, T-REQ99, T-REQ102, T-REQ103, T-REQ104, T-REQ106, T-REQ108
    """
    response = client_with_transactions.post('/delete_category/1')
    logger.info(response.data)
    assert response.status_code == 302, f'Expected response status code: 200, actual: {response.status_code}'
    assert '<strong>Success!</strong> Category was deleted successfully!' in response.data.decode(), \
        f'Application shall remove category chosen by user\n{response.data}'
    response = client_with_transactions.post('/edit_transaction/1', data=dict(transaction_value='25',
                                                                              transaction_desc='shopping',
                                                                              transaction_category='0',
                                                                              transaction_outcome=None),
                                             follow_redirects=True)
    logger.info(response.data)
    assert response.status_code == 200, f'Expected response status code: 200, actual: {response.status_code}'
    assert '<strong>Warning!</strong> Category was not set!' in response.data.decode(), \
        f'Application shall not allow to edit transaction without category provided\n{response.data}'
    response = client_with_transactions.post('/edit_transaction/1',
                                             data=dict(transaction_value='25', transaction_desc='shopping',
                                                       transaction_category='0',
                                                       transaction_outcome='transaction_outcome'),
                                             follow_redirects=True)
    logger.info(response.data)
    assert response.status_code == 200, f'Expected response status code: 200, actual: {response.status_code}'
    assert '<strong>Warning!</strong> Category was not set!' in response.data.decode(), \
        f'Application shall not allow to edit transaction without category provided\n{response.data}'


def test_functional_edit_transaction__no_transaction(logger, client_with_period):
    """
        Covers: T-REQ93, T-REQ94, T-REQ96, T-REQ97, T-REQ98, T-REQ102, T-REQ103, T-REQ105, T-REQ106, T-REQ107
    """
    response = client_with_period.post('/edit_transaction/1', data=dict(transaction_value='25',
                                                                        transaction_desc='shopping',
                                                                        transaction_category=None,
                                                                        transaction_outcome=None),
                                       follow_redirects=True)
    logger.info(response.data)
    assert response.status_code == 200, f'Expected response status code: 200, actual: {response.status_code}'
    assert '<strong>Warning!</strong> There is no such transaction' in response.data.decode(), \
        f'Application shall not allow to edit transaction that does not exist\n{response.data}'
    response = client_with_period.post('/edit_transaction/1', data=dict(transaction_value='25',
                                                                        transaction_desc='shopping',
                                                                        transaction_category=None,
                                                                        transaction_outcome='transaction_outcome'),
                                       follow_redirects=True)
    logger.info(response.data)
    assert response.status_code == 200, f'Expected response status code: 200, actual: {response.status_code}'
    assert '<strong>Warning!</strong> There is no such transaction' in response.data.decode(), \
        f'Application shall not allow to edit transaction that does not exist\n{response.data}'
