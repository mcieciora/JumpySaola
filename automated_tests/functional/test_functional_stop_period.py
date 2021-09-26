def test_functional_stop_period__unauthorised(logger, client):
    """
        Covers: T-REQ53, T-REQ54
    """
    response = client.post('/settings', data=dict(category_name=None, category_limit=None, period_name=None),
                           follow_redirects=True)
    logger.info(response.data)
    assert response.status_code == 200, f'Expected response status code: 200, actual: {response.status_code}'
    assert '<strong>Success!</strong> Please log in to access this page.' in response.data.decode(), \
        f'Application shall not allow unauthorised user to stop period\n{response.data}'


def test_functional_stop_period__registered(logger, client_with_period):
    """
        Covers: T-REQ55, T-REQ56, T-REQ58, T-REQ60, T-REQ61
    """
    response = client_with_period.get('/history')
    logger.info(response.data)
    assert 'There are no periods in history to show!' in response.data.decode(), \
        f'Application shall inform in history view that there are no periods data\n{response.data}'
    response = client_with_period.post('/settings', data=dict(category_name=None, category_limit=None,
                                                              period_name=None), follow_redirects=True)
    logger.info(response.data)
    assert response.status_code == 200, f'Expected response status code: 200, actual: {response.status_code}'
    assert '<strong>Success!</strong> Period finished!' in response.data.decode(), \
        f'Application shall finish period at user request\n{response.data}'
    response = client_with_period.get('/')
    logger.info(response.data)
    assert response.status_code == 200, f'Expected response status code: 200, actual: {response.status_code}'
    assert '<h1 align="center">No active period! Go to settings and start one!</h1>' in response.data.decode(), \
        f'Application shall inform on main page that there is no active period\n{response.data}'


def test_functional_stop_period__no_category(logger, client_with_period):
    """
        Covers: T-REQ55, T-REQ56, T-REQ57, T-REQ60, T-REQ61, T-REQ114
    """
    response = client_with_period.post('/delete_category/1')
    logger.info(response.data)
    assert response.status_code == 200, f'Expected response status code: 200, actual: {response.status_code}'
    assert '<strong>Success!</strong> Category was deleted successfully!' in response.data.decode(), \
        f'Application shall remove category chosen by user\n{response.data}'
    assert '<td>25</td>' not in response.data.decode(), 'Table field is wrong or missing'
    assert '<td>shopping</td>' not in response.data.decode(), 'Table field is wrong or missing'
    response = client_with_period.post('/settings', data=dict(category_name=None, category_limit=None,
                                                              period_name=None), follow_redirects=True)
    logger.info(response.data)
    assert response.status_code == 200, f'Expected response status code: 200, actual: {response.status_code}'
    assert '<strong>Success!</strong> Period finished!' in response.data.decode(), \
        f'Application shall finish period at user request\n{response.data}'


def test_functional_stop_period__no_period(logger, client_with_categories):
    """
        Covers: T-REQ55,T-REQ56, T-REQ58, T-REQ59, T-REQ61, T-REQ114
    """
    response = client_with_categories.get('/')
    logger.info(response.data)
    assert response.status_code == 200, f'Expected response status code: 200, actual: {response.status_code}'
    assert '<h1 align="center">No active period! Go to settings and start one!</h1>' in response.data.decode(), \
        f'Application shall inform on main page that there is no active period\n{response.data}'
    response = client_with_categories.post('/settings', data=dict(category_name=None, category_limit=None,
                                                                  period_name=None), follow_redirects=True)
    logger.info(response.data)
    assert response.status_code == 200, f'Expected response status code: 200, actual: {response.status_code}'
    assert '<strong>Warning!</strong> There is no active period!' in response.data.decode(), \
        f'Application shall not start period if given name was already used in the past\n{response.data}'


def test_functional_stop_period__is_transaction(logger, client_without_history):
    """
        Covers: T-REQ55, T-REQ56, T-REQ58, T-REQ60, T-REQ62, T-REQ114, T-REQ116, T-REQ117
    """
    response = client_without_history.post('/settings', data=dict(category_name=None, category_limit=None,
                                                                  period_name=None), follow_redirects=True)
    logger.info(response.data)
    assert response.status_code == 200, f'Expected response status code: 200, actual: {response.status_code}'
    assert '<strong>Success!</strong> Period finished!' in response.data.decode(), \
        f'Application shall stop period at user request\n{response.data}'
    response = client_without_history.get('/history')
    logger.info(response.data)
    assert '<td>new_period</td>' in response.data.decode(), 'Table field is wrong or missing'
    assert '<td>-25</td>' in response.data.decode(), 'Table field is wrong or missing'
    assert '<td>25</td>' in response.data.decode(), 'Table field is wrong or missing'
    response = client_without_history.post('/settings', data=dict(period_name='next_period'), follow_redirects=True)
    logger.info(response.data)
    assert response.status_code == 200, f'Expected response status code: 200, actual: {response.status_code}'
    assert '<strong>Success!</strong> Period started!' in response.data.decode(), \
        f'Application shall start new period\n{response.data}'
    response = client_without_history.post('/settings', data=dict(category_name=None, category_limit=None,
                                                                  period_name=None), follow_redirects=True)
    logger.info(response.data)
    assert response.status_code == 200, f'Expected response status code: 200, actual: {response.status_code}'
    assert '<strong>Success!</strong> Period finished!' in response.data.decode(), \
        f'Application shall stop period at user request\n{response.data}'
