def test_functional_add_category__unauthorised(logger, client):
    """
            Covers: T-REQ13, T-REQ14
    """
    response = client.post('/settings', data=dict(category_name='category', category_limit=100),
                           follow_redirects=True)
    logger.info(response.data)
    assert response.status_code == 200, f'Expected response status code: 200, actual: {response.status_code}'
    assert '<strong>Success!</strong> Please log in to access this page.' in response.data.decode(), \
        f'Application shall not allow unauthorised user to add category\n{response.data}'


def test_functional_add_category__no_period(logger, client_logged_in_user):
    """
        Covers: T-REQ15, T-REQ16, T-REQ17, T-REQ19, T-REQ21
    """
    response = client_logged_in_user.post('/settings', data=dict(category_name='category', category_limit=100),
                                          follow_redirects=True)
    logger.info(response.data)
    assert response.status_code == 200, f'Expected response status code: 200, actual: {response.status_code}'
    assert '<strong>Success!</strong> Category added!' in response.data.decode(), \
        f'Application shall accept category addition while no period is active\n{response.data}'
    assert '<td>category</td>' in response.data.decode(), 'Table field is wrong or missing'
    assert '<td>100</td>' in response.data.decode(), 'Table field is wrong or missing'


def test_functional_add_category__is_period(logger, client_with_period):
    """
        Covers: T-REQ15, T-REQ16, T-REQ18, T-REQ20, T-REQ21
    """
    response = client_with_period.post('/settings', data=dict(category_name='new_category', category_limit=100),
                                       follow_redirects=True)
    logger.info(response.data)
    assert response.status_code == 200, f'Expected response status code: 200, actual: {response.status_code}'
    assert '<strong>Success!</strong> Category added!' in response.data.decode(), \
        f'Application shall accept category addition while period is active\n{response.data}'


def test_functional_add_category__is_category(logger, client_logged_in_user):
    """
        Covers: T-REQ15, T-REQ16, T-REQ18, T-REQ19, T-REQ21
    """
    response = client_logged_in_user.post('/settings', data=dict(category_name='category', category_limit=100),
                                          follow_redirects=True)
    logger.info(response.data)
    assert response.status_code == 200, f'Expected response status code: 200, actual: {response.status_code}'
    assert '<strong>Success!</strong> Category added!' in response.data.decode(), \
        f'Application shall accept category addition while no period is active\n{response.data}'
    response = client_logged_in_user.post('/settings', data=dict(category_name='category', category_limit=100),
                                          follow_redirects=True)
    logger.info(response.data)
    assert response.status_code == 200, f'Expected response status code: 200, actual: {response.status_code}'
    assert '<strong>Warning!</strong> Such category name already exists!' in response.data.decode(), \
        f'Application shall not add category which already exists\n{response.data}'


def test_functional_add_category__is_transaction(logger, client_with_transactions):
    """
        Covers: T-REQ15, T-REQ16, T-REQ18, T-REQ20, T-REQ22
    """
    response = client_with_transactions.post('/settings', data=dict(category_name='new_category', category_limit=100),
                                             follow_redirects=True)
    logger.info(response.data)
    assert response.status_code == 200, f'Expected response status code: 200, actual: {response.status_code}'
    assert '<strong>Success!</strong> Category added!' in response.data.decode(), \
        f'Application shall accept category addition while period is active\n{response.data}'
