import pytest


def test_transaction_add__non_logged_user_transaction_add(client):
    response = client.post('/', data=dict(transaction_value='25', transaction_desc='shopping',
                                          transaction_outcome=None), follow_redirects=True)
    assert response.status_code == 200, f'Expected response status code: 200, actual: {response.status_code}'
    assert '<strong>Success!</strong> Please log in to access this page.' in response.data.decode(), \
        f'Application shall not add transaction if action was requested by unauthorised user\n{response.data}'


def test_transaction_delete__non_logged_user_delete_transaction(client_with_transactions):
    response = client_with_transactions.get('/logout', follow_redirects=True)
    assert response.status_code == 200, f'Expected response status code: 200, actual: {response.status_code}'
    assert 'Success!</strong> Logged out!' in response.data.decode(), \
        f'Application shall logout user at request\n{response.data}'
    response = client_with_transactions.delete('/delete_transaction/1', follow_redirects=True)
    assert response.status_code == 200, f'Expected response status code: 200, actual: {response.status_code}'
    assert '<strong>Success!</strong> Please log in to access this page.' in response.data.decode(), \
        f'Application shall not delete transaction if action was requested by unauthorised user \n{response.data}'


def test_transaction_add__empty_transaction_description(client_logged_in_user):
    response = client_logged_in_user.post('/', data=dict(transaction_value='25', transaction_desc='',
                                          transaction_outcome='transaction_outcome'), follow_redirects=True)
    assert response.status_code == 200, f'Expected response status code: 200, actual: {response.status_code}'
    assert '<strong>Warning!</strong> Please insert transaction description' in response.data.decode(), \
        f'Application shall not add transaction with empty description\n{response.data}'


def test_transaction_add__empty_transaction_value(client_logged_in_user):
    response = client_logged_in_user.post('/', data=dict(transaction_value='', transaction_desc='shopping',
                                                         transaction_outcome='transaction_outcome'),
                                          follow_redirects=True)
    assert response.status_code == 200, f'Expected response status code: 200, actual: {response.status_code}'
    assert '<strong>Warning!</strong> Transaction value should be a number!' in response.data.decode(), \
        f'Application shall not add transaction with empty value\n{response.data}'


def test_transaction_add__negative_outcome_value(client_logged_in_user):
    response = client_logged_in_user.post('/', data=dict(transaction_value='-25', transaction_desc='shopping',
                                                         transaction_outcome='transaction_outcome'),
                                          follow_redirects=True)
    assert response.status_code == 200, f'Expected response status code: 200, actual: {response.status_code}'
    assert '<strong>Success!</strong> Transaction added!' in response.data.decode(), \
        f'Application shall add transaction that was passed with proper data\n{response.data}'
    assert '<td>-25</td>' in response.data.decode(), 'Table field is wrong or missing'
    assert '<td>shopping</td>' in response.data.decode(), 'Table field is wrong or missing'
    assert '<td>!Not implemented!</td>' in response.data.decode(), 'Table field is wrong or missing'


@pytest.mark.xfail(reason='BUG-1: If transaction value is negative and outcome field is unchecked, then transaction '
                          'is added with negative value but should be positive')
def test_transaction_add__negative_income_value(client_logged_in_user):
    response = client_logged_in_user.post('/', data=dict(transaction_value='-25', transaction_desc='shopping',
                                                         transaction_outcome=None),
                                          follow_redirects=True)
    assert response.status_code == 200, f'Expected response status code: 200, actual: {response.status_code}'
    assert '<strong>Success!</strong> Transaction added!' in response.data.decode(), \
        f'Application shall add transaction that was passed with proper data\n{response.data}'
    assert '<td>25</td>' in response.data.decode(), 'Table field is wrong or missing'
    assert '<td>shopping</td>' in response.data.decode(), 'Table field is wrong or missing'
    assert '<td>!Not implemented!</td>' in response.data.decode(), 'Table field is wrong or missing'


def test_transaction_add__wrong_value_variable_type(client_logged_in_user):
    response = client_logged_in_user.post('/', data=dict(transaction_value='abc', transaction_desc='shopping',
                                                         transaction_outcome='transaction_outcome'),
                                          follow_redirects=True)
    assert response.status_code == 200, f'Expected response status code: 200, actual: {response.status_code}'
    assert '<strong>Warning!</strong> Transaction value should be a number!' in response.data.decode(), \
        f'Application shall not add transaction with other than int description value type\n{response.data}'


def test_transaction_add__add_outcome(client_logged_in_user):
    response = client_logged_in_user.post('/', data=dict(transaction_value='25', transaction_desc='shopping',
                                                         transaction_outcome='transaction_outcome'),
                                          follow_redirects=True)
    assert response.status_code == 200, f'Expected response status code: 200, actual: {response.status_code}'
    assert '<strong>Success!</strong> Transaction added!' in response.data.decode(), \
        f'Application shall add transaction that was passed with proper data\n{response.data}'
    assert '<td>-25</td>' in response.data.decode(), 'Table field is wrong or missing'
    assert '<td>shopping</td>' in response.data.decode(), 'Table field is wrong or missing'
    assert '<td>!Not implemented!</td>' in response.data.decode(), 'Table field is wrong or missing'


def test_transaction_add__add_income(client_logged_in_user):
    response = client_logged_in_user.post('/', data=dict(transaction_value='25', transaction_desc='shopping',
                                                         transaction_outcome=None), follow_redirects=True)
    assert response.status_code == 200, f'Expected response status code: 200, actual: {response.status_code}'
    assert '<strong>Success!</strong> Transaction added!' in response.data.decode(), \
        f'Application shall add transaction that was passed with proper data\n{response.data}'
    assert '<td>25</td>' in response.data.decode(), 'Table field is wrong or missing'
    assert '<td>shopping</td>' in response.data.decode(), 'Table field is wrong or missing'
    assert '<td>!Not implemented!</td>' in response.data.decode(), 'Table field is wrong or missing'


def test_transaction_delete__delete_transaction(client_with_transactions):
    response = client_with_transactions.delete('/delete_transaction/1')
    assert response.status_code == 200, f'Expected response status code: 200, actual: {response.status_code}'
    assert '<strong>Success!</strong> Transaction was deleted successfully!' in response.data.decode(), \
        f'Application shall remove transaction chosen by user\n{response.data}'
    assert '<td>25</td>' not in response.data.decode(), 'Table field is wrong or missing'
    assert '<td>shopping</td>' not in response.data.decode(), 'Table field is wrong or missing'
    assert '<td>!Not implemented!</td>' not in response.data.decode(), 'Table field is wrong or missing'
