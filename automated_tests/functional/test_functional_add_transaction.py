def test_functional_add_transaction__unauthorised(logger, client):
    """
        Covers: T-REQ63, T-REQ64, T-REQ73, T-REQ74
    """
    response = client.post('/', data=dict(transaction_value='25', transaction_desc='shopping',
                                          transaction_category='category',
                                          transaction_outcome=None), follow_redirects=True)
    logger.info(response.data)
    assert response.status_code == 200, f'Expected response status code: 200, actual: {response.status_code}'
    assert '<strong>Success!</strong> Please log in to access this page.' in response.data.decode(), \
        f'Application shall not add transaction if action was requested by unauthorised user\n{response.data}'
    response = client.post('/', data=dict(transaction_value='25', transaction_desc='shopping',
                                          transaction_category='category',
                                          transaction_outcome='transaction_outcome'), follow_redirects=True)
    logger.info(response.data)
    assert response.status_code == 200, f'Expected response status code: 200, actual: {response.status_code}'
    assert '<strong>Success!</strong> Please log in to access this page.' in response.data.decode(), \
        f'Application shall not add transaction if action was requested by unauthorised user\n{response.data}'


def test_functional_add_transaction__registered(logger, client_with_period):
    """
        Covers: T-REQ65, T-REQ66, T-REQ68, T-REQ70, T-REQ71, T-REQ75, T-REQ76, T-REQ78, T-REQ80, T-REQ81
    """
    response = client_with_period.post('/', data=dict(transaction_value='-25', transaction_desc='shopping',
                                                      transaction_category='category',
                                                      transaction_outcome=None), follow_redirects=True)
    logger.info(response.data)
    assert response.status_code == 200, f'Expected response status code: 200, actual: {response.status_code}'
    assert '<strong>Success!</strong> Transaction added!' in response.data.decode(), \
        f'Application shall add transaction that was passed with proper data\n{response.data}'
    assert '<td>25</td>' in response.data.decode(), 'Table field is wrong or missing'
    assert '<td>shopping</td>' in response.data.decode(), 'Table field is wrong or missing'
    assert '<td>category</td>' in response.data.decode(), 'Table field is wrong or missing'
    response = client_with_period.post('/delete_transaction/1')
    logger.info(response.data)
    assert response.status_code == 200, f'Expected response status code: 200, actual: {response.status_code}'
    assert '<strong>Success!</strong> Transaction was deleted successfully!' in response.data.decode(), \
        f'Application shall remove transaction chosen by user\n{response.data}'
    response = client_with_period.post('/', data=dict(transaction_value='-25', transaction_desc='shopping',
                                                      transaction_category='category',
                                                      transaction_outcome='transaction_outcome'), follow_redirects=True)
    logger.info(response.data)
    assert response.status_code == 200, f'Expected response status code: 200, actual: {response.status_code}'
    assert '<strong>Success!</strong> Transaction added!' in response.data.decode(), \
        f'Application shall add transaction that was passed with proper data\n{response.data}'
    assert '<td>-25</td>' in response.data.decode(), 'Table field is wrong or missing'
    assert '<td>shopping</td>' in response.data.decode(), 'Table field is wrong or missing'
    assert '<td>category</td>' in response.data.decode(), 'Table field is wrong or missing'


def test_functional_add_transaction__no_category(logger, client_with_transactions):
    """
        Covers: T-REQ65, T-REQ66, T-REQ67, T-REQ70, T-REQ71, T-REQ75, T-REQ76, T-REQ77, T-REQ80, T-REQ81
    """
    response = client_with_transactions.post('/', data=dict(transaction_value='25', transaction_desc='shopping',
                                                            transaction_category='0', transaction_outcome=None),
                                             follow_redirects=True)
    logger.info(response.data)
    assert response.status_code == 200, f'Expected response status code: 200, actual: {response.status_code}'
    assert '<strong>Warning!</strong> Category was not set!' in response.data.decode(), \
        f'Application shall not accept transaction with default category set\n{response.data}'
    response = client_with_transactions.post('/', data=dict(transaction_value='25', transaction_desc='shopping',
                                                            transaction_category='0',
                                                            transaction_outcome='transaction_outcome'),
                                             follow_redirects=True)
    logger.info(response.data)
    assert response.status_code == 200, f'Expected response status code: 200, actual: {response.status_code}'
    assert '<strong>Warning!</strong> Category was not set!' in response.data.decode(), \
        f'Application shall not accept transaction with default category set\n{response.data}'


def test_functional_add_transaction__no_period(logger, client_with_categories):
    """
        Covers: T-REQ65, T-REQ66, T-REQ68, T-REQ69, T-REQ71, T-REQ75, T-REQ76, T-REQ78, T-REQ79, T-REQ81
    """
    response = client_with_categories.post('/', data=dict(transaction_value='25', transaction_desc='shopping',
                                                          transaction_category='category', transaction_outcome=None),
                                           follow_redirects=True)
    logger.info(response.data)
    assert response.status_code == 200, f'Expected response status code: 200, actual: {response.status_code}'
    assert '<strong>Warning!</strong> No period started!' in response.data.decode(), \
        f'Application without started period shall return proper message\n{response.data}'
    response = client_with_categories.post('/', data=dict(transaction_value='25', transaction_desc='shopping',
                                                          transaction_category='category',
                                                          transaction_outcome='transaction_outcome'),
                                           follow_redirects=True)
    logger.info(response.data)
    assert response.status_code == 200, f'Expected response status code: 200, actual: {response.status_code}'
    assert '<strong>Warning!</strong> No period started!' in response.data.decode(), \
        f'Application without started period shall return proper message\n{response.data}'


def test_functional_add_transaction__is_transaction(logger, client_with_transactions):
    """
        Covers: T-REQ65, T-REQ66, T-REQ68, T-REQ70, T-REQ72, T-REQ75, T-REQ76, T-REQ78, T-REQ80, T-REQ82
    """
    response = client_with_transactions.post('/', data=dict(transaction_value='-50', transaction_desc='food',
                                                            transaction_category='income_category',
                                                            transaction_outcome=None), follow_redirects=True)
    logger.info(response.data)
    assert response.status_code == 200, f'Expected response status code: 200, actual: {response.status_code}'
    assert '<strong>Success!</strong> Transaction added!' in response.data.decode(), \
        f'Application shall add transaction that was passed with proper data\n{response.data}'
    assert '<td>50</td>' in response.data.decode(), 'Table field is wrong or missing'
    assert '<td>food</td>' in response.data.decode(), 'Table field is wrong or missing'
    assert '<td>income_category</td>' in response.data.decode(), 'Table field is wrong or missing'
    response = client_with_transactions.post('/', data=dict(transaction_value='-75', transaction_desc='transport',
                                                            transaction_category='outcome_category',
                                                            transaction_outcome='transaction_outcome'),
                                             follow_redirects=True)
    logger.info(response.data)
    assert response.status_code == 200, f'Expected response status code: 200, actual: {response.status_code}'
    assert '<strong>Success!</strong> Transaction added!' in response.data.decode(), \
        f'Application shall add transaction that was passed with proper data\n{response.data}'
    assert '<td>-75</td>' in response.data.decode(), 'Table field is wrong or missing'
    assert '<td>transport</td>' in response.data.decode(), 'Table field is wrong or missing'
    assert '<td>outcome_category</td>' in response.data.decode(), 'Table field is wrong or missing'
