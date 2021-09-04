def test_category_edit__edit_category_with_active_period(client_with_period):
    response = client_with_period.post('/edit_category/1', data=dict(category_name='new_category', category_limit=250),
                                       follow_redirects=True)
    assert response.status_code == 200, f'Expected response status code: 200, actual: {response.status_code}'
    assert '<strong>Success!</strong> Category was updated!' in response.data.decode(), \
        f'Application shall accept category edition while period is active\n{response.data}'


def test_category_edit__edit_category_with_inactive_period(client_with_categories):
    response = client_with_categories.post('/edit_category/1', data=dict(category_name='new_category',
                                                                         category_limit=250), follow_redirects=True)
    assert response.status_code == 200, f'Expected response status code: 200, actual: {response.status_code}'
    assert '<strong>Success!</strong> Category was updated!' in response.data.decode(), \
        f'Application shall update values of given category\n{response.data}'
    assert '<td>new_category</td>' in response.data.decode(), 'Table field is wrong or missing'
    assert '<td>250</td>' in response.data.decode(), 'Table field is wrong or missing'


def test_category_edit__non_logged_user_edit_category(client_with_categories):
    response = client_with_categories.get('/logout', follow_redirects=True)
    assert response.status_code == 200, f'Expected response status code: 200, actual: {response.status_code}'
    assert 'Success!</strong> Logged out!' in response.data.decode(), \
        f'Application shall logout user at request\n{response.data}'
    response = client_with_categories.post('/edit_category/1', data=dict(category_name='new_category',
                                                                         category_limit=250), follow_redirects=True)
    assert response.status_code == 200, f'Expected response status code: 200, actual: {response.status_code}'
    assert '<strong>Success!</strong> Please log in to access this page.' in response.data.decode(), \
        f'Application shall not allow unauthorised user to add category\n{response.data}'


def test_category_edit__too_short_category_name(client_with_categories):
    response = client_with_categories.post('/edit_category/1', data=dict(category_name='aa',
                                                                         category_limit=250), follow_redirects=True)
    assert response.status_code == 200, f'Expected response status code: 200, actual: {response.status_code}'
    assert '<strong>Warning!</strong> Category name should be at least 3 characters long' in response.data.decode(), \
        f'Application shall not accept too short category name\n{response.data}'


def test_category_edit__empty_value(client_with_categories):
    response = client_with_categories.post('/edit_category/1', data=dict(category_name='new_category',
                                                                         category_limit=''), follow_redirects=True)
    assert response.status_code == 200, f'Expected response status code: 200, actual: {response.status_code}'
    assert '<strong>Warning!</strong> Category limit shall not be empty!' in response.data.decode(), \
        f'Application shall not accept empty category value\n{response.data}'


def test_category_edit__wrong_value_variable_type(client_with_categories):
    response = client_with_categories.post('/edit_category/1', data=dict(category_name='new_category',
                                                                         category_limit='aa'), follow_redirects=True)
    assert response.status_code == 200, f'Expected response status code: 200, actual: {response.status_code}'
    assert '<strong>Warning!</strong> Category limit value should be a number!' in response.data.decode(), \
        f'Application shall not accept wrong value of category limit\n{response.data}'
