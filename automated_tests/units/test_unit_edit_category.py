def test_unit_edit_category__change_name(logger, client_with_categories):
    response = client_with_categories.post('/edit_category/1', data=dict(category_name='category_name',
                                                                         category_limit='100'), follow_redirects=True)
    logger.info(response.data)
    assert response.status_code == 200, f'Expected response status code: 200, actual: {response.status_code}'
    assert '<strong>Success!</strong> Category was updated!' in response.data.decode(), \
        f'Application shall update values of given category\n{response.data}'


def test_unit_edit_category__change_limit(logger, client_with_categories):
    response = client_with_categories.post('/edit_category/1', data=dict(category_name='category',
                                                                         category_limit='250'), follow_redirects=True)
    logger.info(response.data)
    assert response.status_code == 200, f'Expected response status code: 200, actual: {response.status_code}'
    assert '<strong>Success!</strong> Category was updated!' in response.data.decode(), \
        f'Application shall update values of given category\n{response.data}'


def test_unit_edit_category__too_short_category_name(logger, client_with_categories):
    response = client_with_categories.post('/edit_category/1', data=dict(category_name='aa',
                                                                         category_limit=250), follow_redirects=True)
    logger.info(response.data)
    assert response.status_code == 200, f'Expected response status code: 200, actual: {response.status_code}'
    assert '<strong>Warning!</strong> Category name should be at least 3 characters long' in response.data.decode(), \
        f'Application shall not accept too short category name\n{response.data}'


def test_unit_edit_category__empty_value(logger, client_with_categories):
    response = client_with_categories.post('/edit_category/1', data=dict(category_name='new_category',
                                                                         category_limit=''), follow_redirects=True)
    logger.info(response.data)
    assert response.status_code == 200, f'Expected response status code: 200, actual: {response.status_code}'
    assert '<strong>Warning!</strong> Category limit shall not be empty!' in response.data.decode(), \
        f'Application shall not accept empty category value\n{response.data}'


def test_unit_edit_category__wrong_value_variable_type(logger, client_with_categories):
    response = client_with_categories.post('/edit_category/1', data=dict(category_name='new_category',
                                                                         category_limit='aa'), follow_redirects=True)
    logger.info(response.data)
    assert response.status_code == 200, f'Expected response status code: 200, actual: {response.status_code}'
    assert '<strong>Warning!</strong> Category limit value should be a number!' in response.data.decode(), \
        f'Application shall not accept wrong value of category limit\n{response.data}'
