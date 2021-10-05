def test_unit_add_category__add_category(logger, client_logged_in_user):
    response = client_logged_in_user.post('/settings', data=dict(category_name='category', category_limit=100),
                                          follow_redirects=True)
    logger.info(response.data)
    assert response.status_code == 200, f'Expected response status code: 200, actual: {response.status_code}'
    assert '<strong>Success!</strong> Category added!' in response.data.decode(), \
        f'Application shall accept category addition while no period is active\n{response.data}'


def test_unit_add_category__too_short_category_name(logger, client_logged_in_user):
    response = client_logged_in_user.post('/settings', data=dict(category_name='aa', category_limit=100),
                                          follow_redirects=True)
    logger.info(response.data)
    assert response.status_code == 200, f'Expected response status code: 200, actual: {response.status_code}'
    assert '<strong>Warning!</strong> Category name should be at least 3 characters long' in response.data.decode(), \
        f'Application shall not accept too short category name\n{response.data}'


def test_unit_add_category__empty_value(logger, client_logged_in_user):
    response = client_logged_in_user.post('/settings', data=dict(category_name='category', category_limit=''),
                                          follow_redirects=True)
    logger.info(response.data)
    assert response.status_code == 200, f'Expected response status code: 200, actual: {response.status_code}'
    assert '<strong>Warning!</strong> Category limit shall not be empty!' in response.data.decode(), \
        f'Application shall not accept empty category value\n{response.data}'


def test_unit_add_category__wrong_value_variable_type(logger, client_logged_in_user):
    response = client_logged_in_user.post('/settings', data=dict(category_name='category', category_limit='aa'),
                                          follow_redirects=True)
    logger.info(response.data)
    assert response.status_code == 200, f'Expected response status code: 200, actual: {response.status_code}'
    assert '<strong>Warning!</strong> Category limit value should be a number!' in response.data.decode(), \
        f'Application shall not accept wrong value of category limit\n{response.data}'
