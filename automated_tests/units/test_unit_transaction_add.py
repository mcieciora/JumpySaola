def test_transaction_add__empty_transaction_description(client_with_period):
    response = client_with_period.post('/', data=dict(transaction_value='25', transaction_desc='',
                                                      transaction_category='category',
                                                      transaction_outcome='transaction_outcome'), follow_redirects=True)
    assert response.status_code == 200, f'Expected response status code: 200, actual: {response.status_code}'
    assert '<strong>Warning!</strong> Please insert transaction description' in response.data.decode(), \
        f'Application shall not add transaction with empty description\n{response.data}'


def test_transaction_add__empty_transaction_value(client_with_period):
    response = client_with_period.post('/', data=dict(transaction_value='', transaction_desc='shopping',
                                                      transaction_category='category',
                                                      transaction_outcome='transaction_outcome'), follow_redirects=True)
    assert response.status_code == 200, f'Expected response status code: 200, actual: {response.status_code}'
    assert '<strong>Warning!</strong> Transaction value should be a number!' in response.data.decode(), \
        f'Application shall not add transaction with empty value\n{response.data}'


def test_transaction_add__wrong_value_variable_type(client_with_period):
    response = client_with_period.post('/', data=dict(transaction_value='abc', transaction_desc='shopping',
                                                      transaction_category='category',
                                                      transaction_outcome='transaction_outcome'), follow_redirects=True)
    assert response.status_code == 200, f'Expected response status code: 200, actual: {response.status_code}'
    assert '<strong>Warning!</strong> Transaction value should be a number!' in response.data.decode(), \
        f'Application shall not add transaction with other than int description value type\n{response.data}'


def test_transaction_add__negative_outcome_value(client_with_period):
    response = client_with_period.post('/', data=dict(transaction_value='-25', transaction_desc='shopping',
                                                      transaction_category='category',
                                                      transaction_outcome='transaction_outcome'), follow_redirects=True)
    assert response.status_code == 200, f'Expected response status code: 200, actual: {response.status_code}'
    assert '<strong>Success!</strong> Transaction added!' in response.data.decode(), \
        f'Application shall add transaction that was passed with proper data\n{response.data}'
    assert '<td>-25</td>' in response.data.decode(), 'Table field is wrong or missing'
    assert '<td>shopping</td>' in response.data.decode(), 'Table field is wrong or missing'
    assert '<td>category</td>' in response.data.decode(), 'Table field is wrong or missing'


def test_transaction_add__negative_income_value(client_with_period):
    response = client_with_period.post('/', data=dict(transaction_value='-25', transaction_desc='shopping',
                                                      transaction_category='category', transaction_outcome=None),
                                       follow_redirects=True)
    assert response.status_code == 200, f'Expected response status code: 200, actual: {response.status_code}'
    assert '<strong>Success!</strong> Transaction added!' in response.data.decode(), \
        f'Application shall add transaction that was passed with proper data\n{response.data}'
    assert '<td>25</td>' in response.data.decode(), 'Table field is wrong or missing'
    assert '<td>shopping</td>' in response.data.decode(), 'Table field is wrong or missing'
    assert '<td>category</td>' in response.data.decode(), 'Table field is wrong or missing'
