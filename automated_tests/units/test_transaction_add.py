import pytest


@pytest.mark.skip('To be implemented')
def test_transaction_add__non_logged_user_transaction_add(client):
    pass


@pytest.mark.skip('To be implemented')
def test_transaction_add__empty_transaction_outcome(client):
    pass


@pytest.mark.skip('To be implemented')
def test_transaction_add__empty_transaction_description(client):
    pass


@pytest.mark.skip('To be implemented')
def test_transaction_add__empty_transaction_value(client):
    pass


@pytest.mark.skip('To be implemented')
def test_transaction_add__negative_transaction_value(client):
    pass


@pytest.mark.skip('To be implemented')
def test_transaction_add__too_short_description(client):
    pass


@pytest.mark.skip('To be implemented')
def test_transaction_add__wrong_value_variable_type(client):
    pass


@pytest.mark.skip('To be implemented')
def test_transaction_add__add_outcome(client):
    pass


def test_transaction_add__add_income(client_logged_in_user):
    response = client_logged_in_user.post('/', data=dict(transaction_value='25',
                                                         transaction_desc='shopping', transaction_outcome='20'),
                                          follow_redirects=True)
    assert response.status_code == 200, f'Expected response status code: 200, actual: {response.status_code}'
    assert '<strong>Success!</strong> Transaction added!' in response.data.decode(), \
        f'Application shall add transaction that was passed with proper data\n{response.data}'
    assert '<td>-25</td>' in response.data.decode(), 'Table field is wrong or missing'
    assert '<td>shopping</td>' in response.data.decode(), 'Table field is wrong or missing'
    assert '<td>!Not implemented!</td>' in response.data.decode(), 'Table field is wrong or missing'
