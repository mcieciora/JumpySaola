def test_functional_delete_category__unauthorised(logger, client):
    """
        Covers: T-REQ33, T-REQ34
    """
    response = client.post('/delete_category/1', follow_redirects=True)
    logger.info(response.data)
    assert response.status_code == 200, f'Expected response status code: 200, actual: {response.status_code}'
    assert '<strong>Success!</strong> Please log in to access this page.' in response.data.decode(), \
        f'Application shall not allow unauthorised user to delete category\n{response.data}'


def test_functional_delete_category__registered(logger, client_with_categories):
    """
        Covers: T-REQ35, T-REQ36, T-REQ38, T-REQ40
    """
    response = client_with_categories.post('/delete_category/1', follow_redirects=True)
    logger.info(response.data)
    assert response.status_code == 200, f'Expected response status code: 200, actual: {response.status_code}'
    assert '<strong>Success!</strong> Category was deleted successfully!' in response.data.decode(), \
        f'Application shall delete category at user request\n{response.data}'


def test_functional_delete_category__no_period(logger, client_with_categories):
    """
        Covers: T-REQ35, T-REQ36, T-REQ38, T-REQ39, T-REQ41
    """
    response = client_with_categories.post('/delete_category/1')
    logger.info(response.data)
    assert response.status_code == 302, f'Expected response status code: 200, actual: {response.status_code}'
    assert '<strong>Success!</strong> Category was deleted successfully!' in response.data.decode(), \
        f'Application shall remove category chosen by user\n{response.data}'


def test_functional_delete_category__is_period(logger, client_with_period):
    """
        Covers: T-REQ35, T-REQ36, T-REQ38, T-REQ40, T-REQ41
    """
    response = client_with_period.post('/delete_category/1')
    logger.info(response.data)
    assert response.status_code == 302, f'Expected response status code: 200, actual: {response.status_code}'
    assert '<strong>Success!</strong> Category was deleted successfully!' in response.data.decode(), \
        f'Application shall remove category chosen by user\n{response.data}'
    assert '<td>25</td>' not in response.data.decode(), 'Table field is wrong or missing'
    assert '<td>shopping</td>' not in response.data.decode(), 'Table field is wrong or missing'


def test_functional_delete_category__no_category(logger, client_logged_in_user):
    """
        Covers: T-REQ35, T-REQ36, T-REQ37, T-REQ39, T-REQ41
    """
    response = client_logged_in_user.post('/delete_category/1')
    logger.info(response.data)
    assert response.status_code == 302, f'Expected response status code: 200, actual: {response.status_code}'
    assert '<strong>Warning!</strong> There is no such category ID!' in response.data.decode(), \
        f'Application shall inform user there is no such category to delete\n{response.data}'


def test_functional_delete_category__is_transaction(logger, client_with_transactions):
    """
        Covers: T-REQ35, T-REQ36, T-REQ38, T-REQ40, T-REQ42
    """
    response = client_with_transactions.post('/delete_category/1')
    logger.info(response.data)
    assert response.status_code == 302, f'Expected response status code: 200, actual: {response.status_code}'
    assert '<strong>Success!</strong> Category was deleted successfully!' in response.data.decode(), \
        f'Application shall accept category addition while period is active\n{response.data}'
