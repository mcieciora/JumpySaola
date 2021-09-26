def test_unit_edit_transaction__change_value(logger, client_with_transactions):
    response = client_with_transactions.post('/edit_transaction/1',
                                             data=dict(transaction_value='50', transaction_desc='shopping',
                                                       transaction_category='category',
                                                       transaction_outcome='transaction_outcome'),
                                             follow_redirects=True)
    logger.info(response.data)
    assert response.status_code == 200, f'Expected response status code: 200, actual: {response.status_code}'
    assert '<strong>Success!</strong> Transaction was updated!' in response.data.decode(), \
        f'Application shall allow to edit transaction that was passed with proper data\n{response.data}'
    assert '<td>-50</td>' in response.data.decode(), 'Table field is wrong or missing'
    assert '<td>shopping</td>' in response.data.decode(), 'Table field is wrong or missing'
    assert '<td>category</td>' in response.data.decode(), 'Table field is wrong or missing'


def test_unit_edit_transaction__change_category(logger, client_with_transactions):
    response = client_with_transactions.post('/edit_transaction/1',
                                             data=dict(transaction_value='25', transaction_desc='shopping',
                                                       transaction_category='category_plus',
                                                       transaction_outcome='transaction_outcome'),
                                             follow_redirects=True)
    logger.info(response.data)
    assert response.status_code == 200, f'Expected response status code: 200, actual: {response.status_code}'
    assert '<strong>Success!</strong> Transaction was updated!' in response.data.decode(), \
        f'Application shall allow to edit transaction that was passed with proper data\n{response.data}'
    assert '<td>-25</td>' in response.data.decode(), 'Table field is wrong or missing'
    assert '<td>shopping</td>' in response.data.decode(), 'Table field is wrong or missing'
    assert '<td>category_plus</td>' in response.data.decode(), 'Table field is wrong or missing'


def test_unit_edit_transaction__change_description(logger, client_with_transactions):
    response = client_with_transactions.post('/edit_transaction/1',
                                             data=dict(transaction_value='25', transaction_desc='transport',
                                                       transaction_category='category',
                                                       transaction_outcome='transaction_outcome'),
                                             follow_redirects=True)
    logger.info(response.data)
    assert response.status_code == 200, f'Expected response status code: 200, actual: {response.status_code}'
    assert '<strong>Success!</strong> Transaction was updated!' in response.data.decode(), \
        f'Application shall allow to edit transaction that was passed with proper data\n{response.data}'
    assert '<td>-25</td>' in response.data.decode(), 'Table field is wrong or missing'
    assert '<td>transport</td>' in response.data.decode(), 'Table field is wrong or missing'
    assert '<td>category</td>' in response.data.decode(), 'Table field is wrong or missing'


def test_unit_edit_transaction__change_outcome(logger, client_with_transactions):
    response = client_with_transactions.post('/edit_transaction/1',
                                             data=dict(transaction_value='25', transaction_desc='shopping',
                                                       transaction_category='category',
                                                       transaction_outcome=None),
                                             follow_redirects=True)
    logger.info(response.data)
    assert response.status_code == 200, f'Expected response status code: 200, actual: {response.status_code}'
    assert '<strong>Success!</strong> Transaction was updated!' in response.data.decode(), \
        f'Application shall allow to edit transaction that was passed with proper data\n{response.data}'
    assert '<td>25</td>' in response.data.decode(), 'Table field is wrong or missing'
    assert '<td>shopping</td>' in response.data.decode(), 'Table field is wrong or missing'
    assert '<td>category</td>' in response.data.decode(), 'Table field is wrong or missing'


def test_unit_edit_transaction__empty_transaction_description(logger, client_with_transactions):
    response = client_with_transactions.post('/edit_transaction/1',
                                             data=dict(transaction_value='25', transaction_desc='',
                                                       transaction_category='category',
                                                       transaction_outcome='transaction_outcome'),
                                             follow_redirects=True)
    logger.info(response.data)
    assert response.status_code == 200, f'Expected response status code: 200, actual: {response.status_code}'
    assert '<strong>Warning!</strong> Please insert transaction description' in response.data.decode(), \
        f'Application shall not add transaction with empty description\n{response.data}'


def test_unit_edit_transaction__empty_transaction_value(logger, client_with_transactions):
    response = client_with_transactions.post('/edit_transaction/1',
                                             data=dict(transaction_value='', transaction_desc='shopping',
                                                       transaction_category='category',
                                                       transaction_outcome='transaction_outcome'),
                                             follow_redirects=True)
    logger.info(response.data)
    assert response.status_code == 200, f'Expected response status code: 200, actual: {response.status_code}'
    assert '<strong>Warning!</strong> Transaction value should be a number!' in response.data.decode(), \
        f'Application shall not add transaction with empty value\n{response.data}'


def test_unit_edit_transaction__wrong_value_variable_type(logger, client_with_transactions):
    response = client_with_transactions.post('/edit_transaction/1',
                                             data=dict(transaction_value='abc', transaction_desc='shopping',
                                                       transaction_category='category',
                                                       transaction_outcome='transaction_outcome'),
                                             follow_redirects=True)
    logger.info(response.data)
    assert response.status_code == 200, f'Expected response status code: 200, actual: {response.status_code}'
    assert '<strong>Warning!</strong> Transaction value should be a number!' in response.data.decode(), \
        f'Application shall not add transaction with other than int description value type\n{response.data}'


def test_unit_edit_transaction__negative_outcome_value(logger, client_with_transactions):
    response = client_with_transactions.post('/edit_transaction/1',
                                             data=dict(transaction_value='-50', transaction_desc='transport',
                                                       transaction_category='category',
                                                       transaction_outcome='transaction_outcome'),
                                             follow_redirects=True)
    logger.info(response.data)
    assert response.status_code == 200, f'Expected response status code: 200, actual: {response.status_code}'
    assert '<strong>Success!</strong> Transaction was updated!' in response.data.decode(), \
        f'Application shall add transaction that was passed with proper data\n{response.data}'
    assert '<td>-50</td>' in response.data.decode(), 'Table field is wrong or missing'
    assert '<td>transport</td>' in response.data.decode(), 'Table field is wrong or missing'
    assert '<td>category</td>' in response.data.decode(), 'Table field is wrong or missing'


def test_unit_edit_transaction__negative_income_value(logger, client_with_transactions):
    response = client_with_transactions.post('/edit_transaction/1', data=dict(transaction_value='-50',
                                                                              transaction_desc='transport',
                                                                              transaction_category='category',
                                                                              transaction_outcome=None),
                                             follow_redirects=True)
    logger.info(response.data)
    assert response.status_code == 200, f'Expected response status code: 200, actual: {response.status_code}'
    assert '<strong>Success!</strong> Transaction was updated!' in response.data.decode(), \
        f'Application shall add transaction that was passed with proper data\n{response.data}'
    assert '<td>50</td>' in response.data.decode(), 'Table field is wrong or missing'
    assert '<td>transport</td>' in response.data.decode(), 'Table field is wrong or missing'
    assert '<td>category</td>' in response.data.decode(), 'Table field is wrong or missing'
