def test_functional_start_period__unauthorised(client):
    """
        Covers: T-REQ43, T-REQ44
    """
    response = client.post('/settings', data=dict(period_name='new_period'), follow_redirects=True)
    assert response.status_code == 200, f'Expected response status code: 200, actual: {response.status_code}'
    assert '<strong>Success!</strong> Please log in to access this page.' in response.data.decode(), \
        f'Application shall not allow unauthorised user to start period\n{response.data}'


def test_functional_start_period__registered(client_with_categories):
    """
        Covers: T-REQ45, T-REQ46, T-REQ48, T-REQ49, T-REQ51
    """
    response = client_with_categories.get('/')
    assert '<h1 align="center">No active period! Go to settings and start one!</h1>' in response.data.decode()
    response = client_with_categories.post('/settings', data=dict(period_name='new_period'), follow_redirects=True)
    assert response.status_code == 200, f'Expected response status code: 200, actual: {response.status_code}'
    assert '<strong>Success!</strong> Period started!' in response.data.decode(), \
        f'Application shall start period with given name\n{response.data}'


def test_functional_start_period__no_category(client_logged_in_user):
    """
        Covers: T-REQ45, T-REQ46, T-REQ47, T-REQ49, T-REQ51, T-REQ113
    """
    response = client_logged_in_user.post('/settings', data=dict(period_name='new_period'), follow_redirects=True)
    assert response.status_code == 200, f'Expected response status code: 200, actual: {response.status_code}'
    assert '<strong>Warning!</strong> You need to have at least one transaction category created before ' \
           'starting new period!' in response.data.decode(), f'Application without added categories shall not ' \
                                                             f'start period\n{response.data}'


def test_functional_start_period__is_period(client_with_period):
    """
        Covers: T-REQ45, T-REQ46, T-REQ48, T-REQ50, T-REQ51, T-REQ113
    """
    client_with_period.post('/settings', data=dict(category_name=None, category_limit=None,
                                                   period_name=None), follow_redirects=True)
    response = client_with_period.get('/')
    assert '<h1 align="center">No active period! Go to settings and start one!</h1>' in response.data.decode()
    response = client_with_period.post('/settings', data=dict(period_name='new_period'), follow_redirects=True)
    assert response.status_code == 200, f'Expected response status code: 200, actual: {response.status_code}'
    assert '<strong>Warning!</strong> Such period name was already used in the past!' in response.data.decode(), \
        f'Application shall not start period if given name was already used in the past\n{response.data}'


def test_functional_start_period__is_transaction(client_with_transactions):
    """
        Covers: T-REQ45, T-REQ46, T-REQ48, T-REQ50, T-REQ52, T-REQ113
    """
    response = client_with_transactions.post('/settings', data=dict(period_name='new_period'), follow_redirects=True)
    assert response.status_code == 200, f'Expected response status code: 200, actual: {response.status_code}'
    assert '<strong>Warning!</strong> There is already an active period!' in response.data.decode(), \
        f'Application shall not start period if one is already active\n{response.data}'
