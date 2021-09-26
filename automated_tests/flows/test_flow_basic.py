from ..conftest import sign_up, log_in, log_out, add_category, edit_category, delete_category, add_transaction, \
    edit_transaction, delete_transaction, start_period, stop_period


def test_flow_basic__f_req_1(logger, client):
    """
        Covers: F-REQ1
    """
    username = "user1"
    pin_code = "1234"
    test_client = client
    sign_up(logger, test_client, dict(username=username, pin_code_1=pin_code, pin_code_2=pin_code))
    log_out(logger, test_client)
    log_in(logger, test_client, dict(username=username, pin_code=pin_code))
    add_category(logger, test_client, dict(category_name='category', category_limit=100))
    edit_category(logger, test_client, dict(category_name='category', category_limit=250), 1)
    delete_category(logger, test_client, 1)
    add_category(logger, test_client, dict(category_name='category', category_limit=100))
    start_period(logger, test_client, dict(period_name='new_period'))
    add_transaction(logger, test_client, dict(transaction_value='-25', transaction_desc='shopping',
                                              transaction_category='category',
                                              transaction_outcome=None))
    edit_transaction(logger, test_client, dict(transaction_value='25', transaction_desc='shopping',
                                               transaction_category='category', transaction_outcome=None), 1)
    delete_transaction(logger, test_client, 1)
    add_transaction(logger, test_client, dict(transaction_value='-25', transaction_desc='shopping',
                                              transaction_category='category',
                                              transaction_outcome=None))
    add_transaction(logger, test_client, dict(transaction_value='-50', transaction_desc='shopping',
                                              transaction_category='category',
                                              transaction_outcome='transaction_outcome'))
    stop_period(logger, test_client)
    response = client.get('/history')
    logger.info(response.data)
    assert '<td>new_period</td>' in response.data.decode(), 'Table field is wrong or missing'
    assert '<td>-50</td>' in response.data.decode(), 'Table field is wrong or missing'
    assert '<td>25</td>' in response.data.decode(), 'Table field is wrong or missing'
    assert '<embed class="chart" type="image/svg+xml" src= data:image/svg+xml' in response.data.decode(), \
        f'Application shall inform in history view that there are periods data available\n{response.data}'


def test_flow_basic__f_req_2(logger, client_logged_in_user):
    """
        Covers: F-REQ2
    """
    username = "user1"
    pin_code = "1234"
    test_client = client_logged_in_user
    add_category(logger, test_client, dict(category_name='category', category_limit=100))
    response = test_client.get('/settings')
    logger.info(response.data)
    assert '<td>category</td>' in response.data.decode(), 'Table field is wrong or missing'
    assert '<td>100</td>' in response.data.decode(), 'Table field is wrong or missing'
    log_out(logger, test_client)
    log_in(logger, test_client, dict(username=username, pin_code=pin_code))
    response = test_client.get('/settings')
    logger.info(response.data)
    assert '<td>category</td>' in response.data.decode(), 'Table field is wrong or missing'
    assert '<td>100</td>' in response.data.decode(), 'Table field is wrong or missing'
    edit_category(logger, test_client, dict(category_name='category', category_limit=150), 1)
    response = test_client.get('/settings')
    logger.info(response.data)
    assert '<td>category</td>' in response.data.decode(), 'Table field is wrong or missing'
    assert '<td>150</td>' in response.data.decode(), 'Table field is wrong or missing'
    log_out(logger, test_client)
    log_in(logger, test_client, dict(username=username, pin_code=pin_code))
    response = test_client.get('/settings')
    logger.info(response.data)
    assert '<td>category</td>' in response.data.decode(), 'Table field is wrong or missing'
    assert '<td>150</td>' in response.data.decode(), 'Table field is wrong or missing'
    delete_category(logger, test_client, 1)
    response = test_client.get('/settings')
    logger.info(response.data)
    assert '<th>Category</th>' not in response.data.decode(), 'Table field is wrong or missing'
    assert '<th>Limit</th>' not in response.data.decode(), 'Table field is wrong or missing'
    assert '<th>Options</th>' not in response.data.decode(), 'Table field is wrong or missing'
    log_out(logger, test_client)
    log_in(logger, test_client, dict(username=username, pin_code=pin_code))
    response = test_client.get('/settings')
    logger.info(response.data)
    assert '<th>Category</th>' not in response.data.decode(), 'Table field is wrong or missing'
    assert '<th>Limit</th>' not in response.data.decode(), 'Table field is wrong or missing'
    assert '<th>Options</th>' not in response.data.decode(), 'Table field is wrong or missing'
    add_category(logger, test_client, dict(category_name='first_category', category_limit=100))
    add_category(logger, test_client, dict(category_name='second_category', category_limit=250))
    response = test_client.get('/settings')
    logger.info(response.data)
    assert '<td>first_category</td>' in response.data.decode(), 'Table field is wrong or missing'
    assert '<td>100</td>' in response.data.decode(), 'Table field is wrong or missing'
    assert '<td>second_category</td>' in response.data.decode(), 'Table field is wrong or missing'
    assert '<td>250</td>' in response.data.decode(), 'Table field is wrong or missing'
    assert '<th>350</th>' in response.data.decode(), 'Table field is wrong or missing'
    log_out(logger, test_client)
    log_in(logger, test_client, dict(username=username, pin_code=pin_code))
    response = test_client.get('/settings')
    logger.info(response.data)
    assert '<td>first_category</td>' in response.data.decode(), 'Table field is wrong or missing'
    assert '<td>100</td>' in response.data.decode(), 'Table field is wrong or missing'
    assert '<td>second_category</td>' in response.data.decode(), 'Table field is wrong or missing'
    assert '<td>250</td>' in response.data.decode(), 'Table field is wrong or missing'
    assert '<th>350</th>' in response.data.decode(), 'Table field is wrong or missing'


def test_flow_basic__f_req_3(logger, client_with_categories):
    """
        Covers: F-REQ3
    """
    username = "user1"
    pin_code = "1234"
    test_client = client_with_categories
    response = test_client.get('/settings')
    logger.info(response.data)
    assert '<h2 align="center">No active period</h2>' in response.data.decode(), \
        'Table field is wrong or missing'
    log_out(logger, test_client)
    log_in(logger, test_client, dict(username=username, pin_code=pin_code))
    response = test_client.get('/')
    logger.info(response.data)
    assert '<h1 align="center">No active period! Go to settings and start one!</h1>' in response.data.decode(), \
        'Table field is wrong or missing'
    response = test_client.get('/settings')
    logger.info(response.data)
    assert '<h2 align="center">No active period</h2>' in response.data.decode(), \
        'Table field is wrong or missing'
    start_period(logger, test_client, dict(period_name='new_period'))
    response = test_client.get('/')
    logger.info(response.data)
    assert '<h1>new_period</h1>' in response.data.decode(), 'Table field is wrong or missing'
    response = test_client.get('/settings')
    logger.info(response.data)
    assert '<h2 align="center">Actual period: new_period</h2>' in response.data.decode(), \
        'Table field is wrong or missing'
    log_out(logger, test_client)
    log_in(logger, test_client, dict(username=username, pin_code=pin_code))
    response = test_client.get('/')
    logger.info(response.data)
    assert '<h1>new_period</h1>' in response.data.decode(), 'Table field is wrong or missing'
    response = test_client.get('/settings')
    logger.info(response.data)
    assert '<h2 align="center">Actual period: new_period</h2>' in response.data.decode(), \
        'Table field is wrong or missing'
    stop_period(logger, test_client)
    response = test_client.get('/')
    logger.info(response.data)
    assert '<h1 align="center">No active period! Go to settings and start one!</h1>' in response.data.decode(), \
        'Table field is wrong or missing'
    response = test_client.get('/settings')
    logger.info(response.data)
    assert '<h2 align="center">No active period</h2>' in response.data.decode(), \
        'Table field is wrong or missing'
    log_out(logger, test_client)
    log_in(logger, test_client, dict(username=username, pin_code=pin_code))
    response = test_client.get('/')
    logger.info(response.data)
    assert '<h1 align="center">No active period! Go to settings and start one!</h1>' in response.data.decode(), \
        'Table field is wrong or missing'
    response = test_client.get('/settings')
    logger.info(response.data)
    assert '<h2 align="center">No active period</h2>' in response.data.decode(), \
        'Table field is wrong or missing'


def test_flow_basic__f_req_4(logger, client_with_period):
    """
        Covers: F-REQ4
    """
    username = "user1"
    pin_code = "1234"
    test_client = client_with_period
    add_transaction(logger, test_client, dict(transaction_value='-25', transaction_desc='shopping',
                                              transaction_category='category',
                                              transaction_outcome='transaction_outcome'))
    response = test_client.get('/')
    logger.info(response.data)
    assert '<table id="transactions_table">' in response.data.decode(), 'Table field is wrong or missing'
    log_out(logger, test_client)
    log_in(logger, test_client, dict(username=username, pin_code=pin_code))
    response = test_client.get('/')
    logger.info(response.data)
    assert '<table id="transactions_table">' in response.data.decode(), 'Table field is wrong or missing'
    edit_transaction(logger, test_client, dict(transaction_value='50', transaction_desc='transport',
                                               transaction_category='category_plus',
                                               transaction_outcome='transaction_outcome'), 1)
    response = test_client.get('/')
    logger.info(response.data)
    assert '<td>-50</td>' in response.data.decode(), 'Table field is wrong or missing'
    assert '<td>transport</td>' in response.data.decode(), 'Table field is wrong or missing'
    assert '<td>category_plus</td>' in response.data.decode(), 'Table field is wrong or missing'
    log_out(logger, test_client)
    log_in(logger, test_client, dict(username=username, pin_code=pin_code))
    response = test_client.get('/')
    logger.info(response.data)
    assert '<td>-50</td>' in response.data.decode(), 'Table field is wrong or missing'
    assert '<td>transport</td>' in response.data.decode(), 'Table field is wrong or missing'
    assert '<td>category_plus</td>' in response.data.decode(), 'Table field is wrong or missing'
    delete_transaction(logger, test_client, 1)
    response = test_client.get('/')
    logger.info(response.data)
    assert '<table id="transactions_table">' not in response.data.decode(), 'Table field is wrong or missing'
    log_out(logger, test_client)
    log_in(logger, test_client, dict(username=username, pin_code=pin_code))
    response = test_client.get('/')
    logger.info(response.data)
    assert '<table id="transactions_table">' not in response.data.decode(), 'Table field is wrong or missing'
    add_transaction(logger, test_client, dict(transaction_value='-25', transaction_desc='shopping',
                                              transaction_category='category',
                                              transaction_outcome='transaction_outcome'))
    add_transaction(logger, test_client, dict(transaction_value='75', transaction_desc='transport',
                                              transaction_category='category',
                                              transaction_outcome='transaction_outcome'))
    add_transaction(logger, test_client, dict(transaction_value='100', transaction_desc='income',
                                              transaction_category='category_plus',
                                              transaction_outcome=None))
    response = test_client.get('/')
    logger.info(response.data)
    assert '<td>-25</td>' in response.data.decode(), 'Table field is wrong or missing'
    assert '<td>-75</td>' in response.data.decode(), 'Table field is wrong or missing'
    assert '<td>100</td>' in response.data.decode(), 'Table field is wrong or missing'
    assert '<td>shopping</td>' in response.data.decode(), 'Table field is wrong or missing'
    assert '<td>transport</td>' in response.data.decode(), 'Table field is wrong or missing'
    assert '<td>income</td>' in response.data.decode(), 'Table field is wrong or missing'
    assert '<th>0</th>' in response.data.decode(), 'Table field is wrong or missing'
    log_out(logger, test_client)
    log_in(logger, test_client, dict(username=username, pin_code=pin_code))
    response = test_client.get('/')
    logger.info(response.data)
    assert '<td>-25</td>' in response.data.decode(), 'Table field is wrong or missing'
    assert '<td>-75</td>' in response.data.decode(), 'Table field is wrong or missing'
    assert '<td>100</td>' in response.data.decode(), 'Table field is wrong or missing'
    assert '<td>shopping</td>' in response.data.decode(), 'Table field is wrong or missing'
    assert '<td>transport</td>' in response.data.decode(), 'Table field is wrong or missing'
    assert '<td>income</td>' in response.data.decode(), 'Table field is wrong or missing'
    assert '<th>0</th>' in response.data.decode(), 'Table field is wrong or missing'


def test_flow_basic__f_req_5(logger, client_with_period):
    """
        Covers: F-REQ4
    """
    username = "user1"
    pin_code = "1234"
    test_client = client_with_period
    add_transaction(logger, test_client, dict(transaction_value='-25', transaction_desc='shopping',
                                              transaction_category='category',
                                              transaction_outcome='transaction_outcome'))
    add_transaction(logger, test_client, dict(transaction_value='75', transaction_desc='transport',
                                              transaction_category='category',
                                              transaction_outcome='transaction_outcome'))
    add_transaction(logger, test_client, dict(transaction_value='125', transaction_desc='income',
                                              transaction_category='category_plus',
                                              transaction_outcome=None))
    stop_period(logger, test_client)
    response = test_client.get('/')
    logger.info(response.data)
    assert '<h1 align="center">No active period! Go to settings and start one!</h1>' in response.data.decode(), \
        'Table field is wrong or missing'
    response = test_client.get('/settings')
    logger.info(response.data)
    assert '<h2 align="center">No active period</h2>' in response.data.decode(), \
        'Table field is wrong or missing'
    log_out(logger, test_client)
    log_in(logger, test_client, dict(username=username, pin_code=pin_code))
    response = test_client.get('/')
    logger.info(response.data)
    assert '<h1 align="center">No active period! Go to settings and start one!</h1>' in response.data.decode(), \
        'Table field is wrong or missing'
    response = test_client.get('/settings')
    logger.info(response.data)
    assert '<h2 align="center">No active period</h2>' in response.data.decode(), \
        'Table field is wrong or missing'
    response = test_client.get('/history')
    logger.info(response.data)
    assert '<td>125</td>' in response.data.decode(), 'Table field is wrong or missing'
    assert '<td>-100</td>' in response.data.decode(), 'Table field is wrong or missing'
    assert '<td>new_period</td>' in response.data.decode(), 'Table field is wrong or missing'
    assert '<embed class="chart" type="image/svg+xml" src= data:image/svg+xml' in response.data.decode(), \
        f'Application shall inform in history view that there are periods data available\n{response.data}'
