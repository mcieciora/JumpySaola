def test_category_add__add_category_with_inactive_period(client_logged_in_user):
    response = client_logged_in_user.post('/settings', data=dict(category_name='category', category_limit=100),
                                          follow_redirects=True)
    assert response.status_code == 200, f'Expected response status code: 200, actual: {response.status_code}'
    assert '<strong>Success!</strong> Category added!' in response.data.decode(), \
        f'Application without started period shall return proper message\n{response.data}'


def test_category_delete__delete_category_with_inactive_period(client_with_categories):
    response = client_with_categories.post('/delete_category/1')
    assert response.status_code == 200, f'Expected response status code: 200, actual: {response.status_code}'
    assert '<strong>Success!</strong> Category was deleted successfully!' in response.data.decode(), \
        f'Application shall remove transaction chosen by user\n{response.data}'


def test_category_add__non_logged_user_add_category(client):
    response = client.post('/settings', data=dict(category_name='category', category_limit=100),
                           follow_redirects=True)
    assert response.status_code == 200, f'Expected response status code: 200, actual: {response.status_code}'
    assert '<strong>Success!</strong> Please log in to access this page.' in response.data.decode(), \
        f'Application shall not allow unauthorised user to add category\n{response.data}'


def test_category_add__too_short_category_name(client_logged_in_user):
    response = client_logged_in_user.post('/settings', data=dict(category_name='aa', category_limit=100),
                                          follow_redirects=True)
    assert response.status_code == 200, f'Expected response status code: 200, actual: {response.status_code}'
    assert '<strong>Warning!</strong> Category name should be at least 3 characters long' in response.data.decode(), \
        f'Application shall not accept too short category name\n{response.data}'


def test_category_add__empty_category_name(client_logged_in_user):
    response = client_logged_in_user.post('/settings', data=dict(category_name='', category_limit=100),
                                          follow_redirects=True)
    assert response.status_code == 200, f'Expected response status code: 200, actual: {response.status_code}'
    assert '<strong>Success!</strong> Category added!' in response.data.decode(), \
        f'Application without started period shall return proper message\n{response.data}'


def test_category_add__empty_value(client_logged_in_user):
    response = client_logged_in_user.post('/settings', data=dict(category_name='category', category_limit=''),
                                          follow_redirects=True)
    assert response.status_code == 200, f'Expected response status code: 200, actual: {response.status_code}'
    assert '<strong>a!</strong>' in response.data.decode(), \
        f'Application without started period shall return proper message\n{response.data}'


def test_category_add__wrong_value_variable_type(client_logged_in_user):
    response = client_logged_in_user.post('/settings', data=dict(category_name='category', category_limit='aa'),
                                          follow_redirects=True)
    assert response.status_code == 200, f'Expected response status code: 200, actual: {response.status_code}'
    assert '<strong>Warning!</strong> Category limit value should be a number!' in response.data.decode(), \
        f'Application shall not accept wrong value of category limit\n{response.data}'


def test_category_add__add_same_category_name_two_times(client_logged_in_user):
    response = client_logged_in_user.post('/settings', data=dict(category_name='category', category_limit=100),
                                          follow_redirects=True)
    assert response.status_code == 200, f'Expected response status code: 200, actual: {response.status_code}'
    assert '<strong>Success!</strong> Category added!' in response.data.decode(), \
        f'Application without started period shall return proper message\n{response.data}'
    response = client_logged_in_user.post('/settings', data=dict(category_name='category', category_limit=100),
                                          follow_redirects=True)
    assert response.status_code == 200, f'Expected response status code: 200, actual: {response.status_code}'
    assert '<strong>Success!</strong> Category added!' in response.data.decode(), \
        f'Application without started period shall return proper message\n{response.data}'


def test_category_add__add_category_with_active_period(client_with_period):
    response = client_with_period.post('/settings', data=dict(category_name='category', category_limit=100),
                                       follow_redirects=True)
    assert response.status_code == 200, f'Expected response status code: 200, actual: {response.status_code}'
    assert '<strong>Success!</strong> Category added!' in response.data.decode(), \
        f'Application without started period shall return proper message\n{response.data}'


def test_category_delete__delete_category_with_active_period(client_with_period):
    response = client_with_period.post('/delete_category/1')
    assert response.status_code == 200, f'Expected response status code: 200, actual: {response.status_code}'
    assert '<strong>Success!</strong> Transaction was deleted successfully!' in response.data.decode(), \
        f'Application shall remove transaction chosen by user\n{response.data}'
    assert '<td>25</td>' not in response.data.decode(), 'Table field is wrong or missing'
    assert '<td>shopping</td>' not in response.data.decode(), 'Table field is wrong or missing'
    assert '<td>None</td>' not in response.data.decode(), 'Table field is wrong or missing'


def test_category_delete__delete_category(client_logged_in_user):
    response = client_logged_in_user.post('/delete_category/1')
    assert response.status_code == 200, f'Expected response status code: 200, actual: {response.status_code}'
    assert '<strong>Success!</strong> Transaction was deleted successfully!' in response.data.decode(), \
        f'Application shall remove transaction chosen by user\n{response.data}'
    assert '<td>25</td>' not in response.data.decode(), 'Table field is wrong or missing'
    assert '<td>shopping</td>' not in response.data.decode(), 'Table field is wrong or missing'
    assert '<td>None</td>' not in response.data.decode(), 'Table field is wrong or missing'


def test_category_delete__non_logged_user_delete_category(client_logged_in_user):
    response = client_logged_in_user.post('/delete_category/1')
    assert response.status_code == 200, f'Expected response status code: 200, actual: {response.status_code}'
    assert '<strong>Success!</strong> Transaction was deleted successfully!' in response.data.decode(), \
        f'Application shall remove transaction chosen by user\n{response.data}'
    assert '<td>25</td>' not in response.data.decode(), 'Table field is wrong or missing'
    assert '<td>shopping</td>' not in response.data.decode(), 'Table field is wrong or missing'
    assert '<td>None</td>' not in response.data.decode(), 'Table field is wrong or missing'



