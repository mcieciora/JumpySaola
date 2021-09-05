def test_period__too_short_period_name(client_with_categories):
    response = client_with_categories.post('/settings', data=dict(period_name='aa'), follow_redirects=True)
    assert response.status_code == 200, f'Expected response status code: 200, actual: {response.status_code}'
    assert '<strong>Warning!</strong> Period name should be at least 3 characters' in response.data.decode(), \
        f'Application shall not start period if given name is shorter than 3 characters\n{response.data}'
