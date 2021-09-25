def test_unit_start_period__start_period(logger, client_with_categories):
    response = client_with_categories.post('/settings', data=dict(period_name='new_period'), follow_redirects=True)
    logger.info(response.data)
    assert response.status_code == 200, f'Expected response status code: 200, actual: {response.status_code}'
    assert '<strong>Success!</strong> Period started!' in response.data.decode(), \
        f'Application shall start period with given name\n{response.data}'


def test_unit_start_period__too_short_period_name(logger, client_with_categories):
    response = client_with_categories.post('/settings', data=dict(period_name='aa'), follow_redirects=True)
    logger.debug(response.data)
    assert response.status_code == 200, f'Expected response status code: 200, actual: {response.status_code}'
    assert '<strong>Warning!</strong> Period name should be at least 3 characters' in response.data.decode(), \
        f'Application shall not start period if given name is shorter than 3 characters\n{response.data}'
