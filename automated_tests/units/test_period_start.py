import pytest


def test_period__no_categories_period_start(client_logged_in_user):
    response = client_logged_in_user.post('/settings', data=dict(period_name='new_period'), follow_redirects=True)
    assert response.status_code == 200, f'Expected response status code: 200, actual: {response.status_code}'
    assert '<strong>Warning!</strong> You need to have at least one transaction category created before ' \
           'starting new period!' in response.data.decode(), f'Application without added categories shall not ' \
                                                             f'start period\n{response.data}'


def test_period__start_period(client_with_categories):
    response = client_with_categories.post('/settings', data=dict(period_name='new_period'), follow_redirects=True)
    assert response.status_code == 200, f'Expected response status code: 200, actual: {response.status_code}'
    assert '<strong>Success!</strong> Period started!' in response.data.decode(), \
        f'Application shall start period with given name\n{response.data}'


def test_period__too_short_period_name(client_with_categories):
    response = client_with_categories.post('/settings', data=dict(period_name='aa'), follow_redirects=True)
    assert response.status_code == 200, f'Expected response status code: 200, actual: {response.status_code}'
    assert '<strong>Warning!</strong> Period name should be at least 3 characters' in response.data.decode(), \
        f'Application shall not start period if given name is shorter than 3 characters\n{response.data}'


@pytest.mark.xfail(reason='BUG-2: If given period name is the same as the one used in the past application exit '
                          'with error')
def test_period__use_the_same_period_name(client_with_categories):
    response = client_with_categories.post('/settings', data=dict(period_name='new_period'), follow_redirects=True)
    assert response.status_code == 200, f'Expected response status code: 200, actual: {response.status_code}'
    assert '<strong>Success!</strong> Period started!' in response.data.decode(), \
        f'Application shall start period with given name\n{response.data}'
    response = client_with_categories.post('/settings', data=dict(period_name='new_period'), follow_redirects=True)
    assert response.status_code == 200, f'Expected response status code: 200, actual: {response.status_code}'
    assert '<strong>Success!</strong> Period started!' in response.data.decode(), \
        f'Application shall not start period if given name was already used in the past\n{response.data}'
