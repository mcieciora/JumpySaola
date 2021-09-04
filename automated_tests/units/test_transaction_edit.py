def test_transaction_edit__non_logged_user_transaction_edit(client):
    response = client.post('/edit_transaction/1', data=dict(transaction_value='25', transaction_desc='shopping', transaction_category='category',
                                          transaction_outcome=None), follow_redirects=True)
    assert response.status_code == 200, f'Expected response status code: 200, actual: {response.status_code}'
    assert '<strong>Success!</strong> Please log in to access this page.' in response.data.decode(), \
        f'Application shall not add transaction if action was requested by unauthorised user\n{response.data}'


def test_transaction_edit__empty_transaction_description(client_with_transactions):
    response = client_with_transactions.post('/edit_transaction/1', data=dict(transaction_value='25', transaction_desc='',
                                                      transaction_category='category',
                                                      transaction_outcome='transaction_outcome'), follow_redirects=True)
    assert response.status_code == 200, f'Expected response status code: 200, actual: {response.status_code}'
    assert '<strong>Warning!</strong> Please insert transaction description' in response.data.decode(), \
        f'Application shall not add transaction with empty description\n{response.data}'


def test_transaction_edit__empty_transaction_value(client_with_transactions):
    response = client_with_transactions.post('/edit_transaction/1', data=dict(transaction_value='', transaction_desc='shopping',
                                                      transaction_category='category',
                                                      transaction_outcome='transaction_outcome'), follow_redirects=True)
    assert response.status_code == 200, f'Expected response status code: 200, actual: {response.status_code}'
    assert '<strong>Warning!</strong> Transaction value should be a number!' in response.data.decode(), \
        f'Application shall not add transaction with empty value\n{response.data}'


def test_transaction_edit__wrong_value_variable_type(client_with_transactions):
    response = client_with_transactions.post('/edit_transaction/1', data=dict(transaction_value='abc', transaction_desc='shopping',
                                                      transaction_category='category',
                                                      transaction_outcome='transaction_outcome'), follow_redirects=True)
    assert response.status_code == 200, f'Expected response status code: 200, actual: {response.status_code}'
    assert '<strong>Warning!</strong> Transaction value should be a number!' in response.data.decode(), \
        f'Application shall not add transaction with other than int description value type\n{response.data}'


def test_transaction_edit__negative_outcome_value(client_with_transactions):
    response = client_with_transactions.post('/edit_transaction/1', data=dict(transaction_value='-50',
                                                                              transaction_desc='transport',
                                                                              transaction_category='category',
                                                                              transaction_outcome='transaction_outcome')
                                             , follow_redirects=True)
    assert response.status_code == 200, f'Expected response status code: 200, actual: {response.status_code}'
    assert '<strong>Success!</strong> Transaction was updated!' in response.data.decode(), \
        f'Application shall add transaction that was passed with proper data\n{response.data}'
    assert '<td>-50</td>' in response.data.decode(), 'Table field is wrong or missing'
    assert '<td>transport</td>' in response.data.decode(), 'Table field is wrong or missing'
    assert '<td>category</td>' in response.data.decode(), 'Table field is wrong or missing'


def test_transaction_edit__negative_income_value(client_with_transactions):
    response = client_with_transactions.post('/edit_transaction/1', data=dict(transaction_value='-50',
                                                                              transaction_desc='transport',
                                                                              transaction_category='category',
                                                                              transaction_outcome=None),
                                             follow_redirects=True)
    assert response.status_code == 200, f'Expected response status code: 200, actual: {response.status_code}'
    assert '<strong>Success!</strong> Transaction was updated!' in response.data.decode(), \
        f'Application shall add transaction that was passed with proper data\n{response.data}'
    assert '<td>50</td>' in response.data.decode(), 'Table field is wrong or missing'
    assert '<td>transport</td>' in response.data.decode(), 'Table field is wrong or missing'
    assert '<td>category</td>' in response.data.decode(), 'Table field is wrong or missing'


def test_transaction_edit__edit_outcome(client_with_transactions):
    client_with_transactions.post('/settings', data={'category_name': 'new_category', 'category_limit': '250'})
    response = client_with_transactions.post('/edit_transaction/1', data=dict(transaction_value='75',
                                                                              transaction_desc='transport',
                                                                              transaction_category='new_category',
                                                                              transaction_outcome='transaction_outcome')
                                             , follow_redirects=True)
    assert response.status_code == 200, f'Expected response status code: 200, actual: {response.status_code}'
    assert '<strong>Success!</strong> Transaction was updated!' in response.data.decode(), \
        f'Application shall add transaction that was passed with proper data\n{response.data}'
    assert '<td>-75</td>' in response.data.decode(), 'Table field is wrong or missing'
    assert '<td>transport</td>' in response.data.decode(), 'Table field is wrong or missing'
    assert '<td>new_category</td>' in response.data.decode(), 'Table field is wrong or missing'


def test_transaction_edit__edit_income(client_with_transactions):
    client_with_transactions.post('/settings', data={'category_name': 'new_category', 'category_limit': '250'})
    response = client_with_transactions.post('/edit_transaction/1', data=dict(transaction_value='75',
                                                                              transaction_desc='transport',
                                                                              transaction_category='new_category',
                                                                              transaction_outcome=None),
                                             follow_redirects=True)
    assert response.status_code == 200, f'Expected response status code: 200, actual: {response.status_code}'
    assert '<strong>Success!</strong> Transaction was updated!' in response.data.decode(), \
        f'Application shall add transaction that was passed with proper data\n{response.data}'
    assert '<td>75</td>' in response.data.decode(), 'Table field is wrong or missing'
    assert '<td>transport</td>' in response.data.decode(), 'Table field is wrong or missing'
    assert '<td>new_category</td>' in response.data.decode(), 'Table field is wrong or missing'


def test_transaction_edit__no_category_transaction_edit(client_with_transactions):
    response = client_with_transactions.post('/edit_transaction/1', data=dict(transaction_value='25',
                                                                              transaction_desc='shopping',
                                                                              transaction_category='0',
                                                                              transaction_outcome=None),
                                             follow_redirects=True)
    assert response.status_code == 200, f'Expected response status code: 200, actual: {response.status_code}'
    assert '<strong>Warning!</strong> Category was not set!' in response.data.decode(), \
        f'Application shall not accept transaction with default category set\n{response.data}'
