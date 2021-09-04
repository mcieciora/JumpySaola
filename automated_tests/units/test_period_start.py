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


def test_period__use_the_same_period_name(client_with_categories):
    response = client_with_categories.post('/settings', data=dict(period_name='new_period'), follow_redirects=True)
    assert response.status_code == 200, f'Expected response status code: 200, actual: {response.status_code}'
    assert '<strong>Success!</strong> Period started!' in response.data.decode(), \
        f'Application shall start period with given name\n{response.data}'

    client_with_categories.post('/settings', data=dict(category_name=None, category_limit=None,
                                                       period_name=None), follow_redirects=True)
    response = client_with_categories.get('/')
    assert '<h1 align="center">No active period! Go to settings and start one!</h1>' in response.data.decode()
    response = client_with_categories.post('/settings', data=dict(period_name='new_period'), follow_redirects=True)
    assert response.status_code == 200, f'Expected response status code: 200, actual: {response.status_code}'
    assert '<strong>Warning!</strong> Such period name was already used in the past!' in response.data.decode(), \
        f'Application shall not start period if given name was already used in the past\n{response.data}'


def test_period__stop_period(client_with_period):
    client_with_period.post('/settings', data=dict(category_name=None, category_limit=None,
                                                                  period_name=None), follow_redirects=True)
    response = client_with_period.get('/')
    assert response.status_code == 200, f'Expected response status code: 200, actual: {response.status_code}'
    assert '<h1 align="center">No active period! Go to settings and start one!</h1>' in response.data.decode()
