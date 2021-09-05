def test_functional_edit_category__unauthorised(client_with_categories):
    """
            Covers: T-REQ23, T-REQ24
    """
    response = client_with_categories.get('/logout', follow_redirects=True)
    assert response.status_code == 200, f'Expected response status code: 200, actual: {response.status_code}'
    assert 'Success!</strong> Logged out!' in response.data.decode(), \
        f'Application shall logout user at request\n{response.data}'
    response = client_with_categories.post('/edit_category/1', data=dict(category_name='new_category',
                                                                         category_limit=250), follow_redirects=True)
    assert response.status_code == 200, f'Expected response status code: 200, actual: {response.status_code}'
    assert '<strong>Success!</strong> Please log in to access this page.' in response.data.decode(), \
        f'Application shall not allow unauthorised user to edit category\n{response.data}'


def test_functional_edit_category__no_period(client_with_categories):
    """
        Covers: T-REQ25, T-REQ26, T-REQ27, T-REQ29, T-REQ31
    """
    response = client_with_categories.post('/edit_category/1', data=dict(category_name='new_category',
                                                                         category_limit=250), follow_redirects=True)
    assert response.status_code == 200, f'Expected response status code: 200, actual: {response.status_code}'
    assert '<strong>Success!</strong> Category was updated!' in response.data.decode(), \
        f'Application shall update values of given category\n{response.data}'
    assert '<td>new_category</td>' in response.data.decode(), 'Table field is wrong or missing'
    assert '<td>250</td>' in response.data.decode(), 'Table field is wrong or missing'


def test_functional_edit_category__is_period(client_with_period):
    """
        Covers: T-REQ25, T-REQ26, T-REQ28, T-REQ30, T-REQ31
    """
    response = client_with_period.post('/edit_category/1', data=dict(category_name='new_category', category_limit=250),
                                       follow_redirects=True)
    assert response.status_code == 200, f'Expected response status code: 200, actual: {response.status_code}'
    assert '<strong>Success!</strong> Category was updated!' in response.data.decode(), \
        f'Application shall accept category edition while period is active\n{response.data}'


def test_functional_edit_category__is_category(client_with_categories):
    """
        Covers: T-REQ15, T-REQ16, T-REQ18, T-REQ20, T-REQ21, T-REQ25, T-REQ26, T-REQ28, T-REQ29, T-REQ31
    """
    response = client_with_categories.post('/settings', data=dict(category_name='new_category', category_limit=100),
                                           follow_redirects=True)
    assert response.status_code == 200, f'Expected response status code: 200, actual: {response.status_code}'
    assert '<strong>Success!</strong> Category added!' in response.data.decode(), \
        f'Application shall update values of given category\n{response.data}'
    response = client_with_categories.post('/edit_category/1', data=dict(category_name='new_category',
                                                                         category_limit=100), follow_redirects=True)
    assert response.status_code == 200, f'Expected response status code: 200, actual: {response.status_code}'
    assert '<strong>Warning!</strong> Such category name already exists!' in response.data.decode(), \
        f'Application shall not update name of category that already exists\n{response.data}'


def test_functional_edit_category__is_transaction(client_with_transactions):
    """
        Covers: T-REQ25, T-REQ26, T-REQ28, T-REQ30, T-REQ32
    """
    response = client_with_transactions.post('/edit_category/1', data=dict(category_name='new_category',
                                                                           category_limit=100), follow_redirects=True)
    assert response.status_code == 200, f'Expected response status code: 200, actual: {response.status_code}'
    assert '<strong>Success!</strong> Category was updated!' in response.data.decode(), \
        f'Application shall accept category addition while period is active\n{response.data}'
