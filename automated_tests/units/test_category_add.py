def test_category__add_category(client_logged_in_user):
    response = client_logged_in_user.post('/settings', data=dict(category_name='category', category_limit=100),
                                          follow_redirects=True)
    assert response.status_code == 200, f'Expected response status code: 200, actual: {response.status_code}'
    assert '<strong>Success!</strong> Category added!' in response.data.decode(), \
        f'Application without started period shall return proper message\n{response.data}'
