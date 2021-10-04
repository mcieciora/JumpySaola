from selenium.webdriver.support.ui import Select


def test_selenium_basic__connect_to_app(firefox_driver):
    assert '/login' in firefox_driver.current_url
    assert 'Login' == firefox_driver.title
    expected_content = ['<a href="/login">Login</a>', '<a href="/signup">Sign Up</a>', 'placeholder="Enter username"',
                        'placeholder="Enter pin code"']
    for content in expected_content:
        assert content in firefox_driver.page_source


def test_selenium_basic__sign_up_with_wrong_data(firefox_driver):
    firefox_driver.find_element_by_link_text('Sign Up').click()
    assert 'Sign Up' == firefox_driver.title
    assert '/signup' in firefox_driver.current_url
    firefox_driver.find_element_by_name('username').send_keys('')
    firefox_driver.find_element_by_id('submit').click()
    assert 'User name length must be greater than 3 characters.' in firefox_driver.page_source
    firefox_driver.find_element_by_name('username').send_keys('tester')
    firefox_driver.find_element_by_name('pin_code_1').send_keys('1234')
    firefox_driver.find_element_by_name('pin_code_2').send_keys('1233')
    firefox_driver.find_element_by_id('submit').click()
    assert 'Passwords do not match.' in firefox_driver.page_source


def test_selenium_basic__sign_up_user_and_log_out(firefox_driver):
    firefox_driver.find_element_by_link_text('Sign Up').click()
    firefox_driver.find_element_by_name('username').send_keys('tester')
    firefox_driver.find_element_by_name('pin_code_1').send_keys('1234')
    firefox_driver.find_element_by_name('pin_code_2').send_keys('1234')
    firefox_driver.find_element_by_id('submit').click()
    assert 'Home' == firefox_driver.title
    assert 'Account created!' in firefox_driver.page_source
    assert 'No active period! Go to settings and start one!' in firefox_driver.page_source
    firefox_driver.find_element_by_link_text('Logout').click()
    assert '/login' in firefox_driver.current_url
    assert 'Login' == firefox_driver.title
    expected_content = ['<a href="/login">Login</a>', '<a href="/signup">Sign Up</a>', 'placeholder="Enter username"',
                        'placeholder="Enter pin code"']
    for content in expected_content:
        assert content in firefox_driver.page_source


def test_selenium_basic__login_with_wrong_data(firefox_driver):
    firefox_driver.find_element_by_name('username').send_keys('no_tester')
    firefox_driver.find_element_by_name('pin_code').send_keys('1234')
    firefox_driver.find_element_by_id('login').click()
    assert 'Username does not exist.' in firefox_driver.page_source
    assert '/login' in firefox_driver.current_url
    assert 'Login' == firefox_driver.title
    firefox_driver.find_element_by_name('username').send_keys('tester')
    firefox_driver.find_element_by_name('pin_code').send_keys('1233')
    firefox_driver.find_element_by_id('login').click()
    assert 'Incorrect pin code, try again.' in firefox_driver.page_source
    assert '/login' in firefox_driver.current_url
    assert 'Login' == firefox_driver.title


def test_selenium_basic__login_user(firefox_driver):
    firefox_driver.find_element_by_name('username').send_keys('tester')
    firefox_driver.find_element_by_name('pin_code').send_keys('1234')
    firefox_driver.find_element_by_id('login').click()
    assert 'Home' == firefox_driver.title
    assert 'Logged in successfully!' in firefox_driver.page_source
    assert 'No active period! Go to settings and start one!' in firefox_driver.page_source


def test_selenium_basic__change_to_settings_tab(firefox_driver_logged_in):
    firefox_driver_logged_in.find_element_by_link_text('Settings').click()
    assert '/settings' in firefox_driver_logged_in.current_url
    assert 'Settings' == firefox_driver_logged_in.title
    expected_content = ['<h2 align="center">No active period</h2>', 'placeholder="Name"', 'placeholder="Limit"',
                        'placeholder="Period name"', '<h2 align="center">Categories</h2>']
    for content in expected_content:
        assert content in firefox_driver_logged_in.page_source


def test_selenium_basic__start_period_before_adding_categories(firefox_driver_logged_in):
    firefox_driver_logged_in.find_element_by_link_text('Settings').click()
    firefox_driver_logged_in.find_element_by_name('period_name').send_keys('period')
    firefox_driver_logged_in.find_element_by_id('start_period').click()
    assert 'You need to have at least one transaction category created before starting new period!' in \
           firefox_driver_logged_in.page_source


def test_selenium_basic__add_category_with_wrong_data(firefox_driver_logged_in):
    firefox_driver_logged_in.find_element_by_link_text('Settings').click()
    firefox_driver_logged_in.find_element_by_name('category_name').send_keys('')
    firefox_driver_logged_in.find_element_by_name('category_limit').send_keys('100')
    firefox_driver_logged_in.find_element_by_id('add_category').click()
    assert 'Category name should be at least 3 characters long' in firefox_driver_logged_in.page_source
    firefox_driver_logged_in.find_element_by_name('category_name').send_keys('category')
    firefox_driver_logged_in.find_element_by_name('category_limit').send_keys('')
    firefox_driver_logged_in.find_element_by_id('add_category').click()
    assert 'Category limit shall not be empty!' in firefox_driver_logged_in.page_source


def test_selenium_basic__add_category(firefox_driver_logged_in):
    firefox_driver_logged_in.find_element_by_link_text('Settings').click()
    firefox_driver_logged_in.find_element_by_name('category_name').send_keys('category')
    firefox_driver_logged_in.find_element_by_name('category_limit').send_keys('100')
    firefox_driver_logged_in.find_element_by_id('add_category').click()
    assert 'Category added!' in firefox_driver_logged_in.page_source
    expected_content = ['<h2 align="center">No active period</h2>', 'placeholder="Name"', 'placeholder="Limit"',
                        'placeholder="Period name"', '<h2 align="center">Categories</h2>', '<th>Category</th>',
                        '<th>Limit</th>', '<th>Options</th>', '<td>category</td>', '<td>100</td>',
                        '<button type="submit" name="edit" class="aslink">Edit</button>',
                        '<button type="submit" name="delete" class="aslink redlink">Delete</button>',
                        '<th>Summary</th>', '<th>100</th>']
    for content in expected_content:
        assert content in firefox_driver_logged_in.page_source


def test_selenium_basic__add_same_category_again(firefox_driver_logged_in):
    firefox_driver_logged_in.find_element_by_link_text('Settings').click()
    firefox_driver_logged_in.find_element_by_name('category_name').send_keys('category')
    firefox_driver_logged_in.find_element_by_name('category_limit').send_keys('100')
    firefox_driver_logged_in.find_element_by_id('add_category').click()
    assert 'Such category name already exists!' in firefox_driver_logged_in.page_source


def test_selenium_basic__change_to_edit_category_tab(firefox_driver_logged_in):
    firefox_driver_logged_in.find_element_by_link_text('Settings').click()
    firefox_driver_logged_in.find_element_by_name('edit').click()
    assert '/edit_category/1' in firefox_driver_logged_in.current_url
    assert 'Settings' == firefox_driver_logged_in.title
    expected_content = ['placeholder="Name"', 'value="category"', 'placeholder="Limit"', 'value="100"',
                        '<input id="submit" class="btn" type="submit" value="Submit">']
    for content in expected_content:
        assert content in firefox_driver_logged_in.page_source


def test_selenium_basic__edit_category_with_wrong_data(firefox_driver_logged_in):
    firefox_driver_logged_in.find_element_by_link_text('Settings').click()
    firefox_driver_logged_in.find_element_by_name('edit').click()
    firefox_driver_logged_in.find_element_by_name('category_name').clear()
    firefox_driver_logged_in.find_element_by_name('category_name').send_keys('')
    firefox_driver_logged_in.find_element_by_name('category_limit').clear()
    firefox_driver_logged_in.find_element_by_name('category_limit').send_keys('100')
    firefox_driver_logged_in.find_element_by_id('submit').click()
    assert 'Category name should be at least 3 characters long' in firefox_driver_logged_in.page_source


def test_selenium_basic__edit_category(firefox_driver_logged_in):
    firefox_driver_logged_in.find_element_by_link_text('Settings').click()
    firefox_driver_logged_in.find_element_by_name('edit').click()
    firefox_driver_logged_in.find_element_by_name('category_name').clear()
    firefox_driver_logged_in.find_element_by_name('category_name').send_keys('category')
    firefox_driver_logged_in.find_element_by_name('category_limit').clear()
    firefox_driver_logged_in.find_element_by_name('category_limit').send_keys('150')
    firefox_driver_logged_in.find_element_by_id('submit').click()
    assert '/settings' in firefox_driver_logged_in.current_url
    assert 'Settings' == firefox_driver_logged_in.title
    assert 'Category was updated!' in firefox_driver_logged_in.page_source
    assert 'category' in firefox_driver_logged_in.page_source
    assert '150' in firefox_driver_logged_in.page_source
    firefox_driver_logged_in.find_element_by_name('edit').click()
    firefox_driver_logged_in.find_element_by_name('category_name').clear()
    firefox_driver_logged_in.find_element_by_name('category_name').send_keys('new_category')
    firefox_driver_logged_in.find_element_by_name('category_limit').clear()
    firefox_driver_logged_in.find_element_by_name('category_limit').send_keys('200')
    firefox_driver_logged_in.find_element_by_id('submit').click()
    assert '/settings' in firefox_driver_logged_in.current_url
    assert 'Settings' == firefox_driver_logged_in.title
    assert 'Category was updated!' in firefox_driver_logged_in.page_source
    assert 'new_category' in firefox_driver_logged_in.page_source
    assert '200' in firefox_driver_logged_in.page_source


def test_selenium_basic__delete_category(firefox_driver_logged_in):
    firefox_driver_logged_in.find_element_by_link_text('Settings').click()
    firefox_driver_logged_in.find_element_by_name('delete').click()
    assert 'Category was deleted successfully!' in firefox_driver_logged_in.page_source
    assert '/settings' in firefox_driver_logged_in.current_url
    assert 'Settings' == firefox_driver_logged_in.title
    assert '<h2 align="center">No active period</h2>' in firefox_driver_logged_in.page_source
    not_expected_content = ['<th>Category</th>', '<th>Limit</th>', '<th>Options</th>', '<td>new_category</td>',
                            '<td>200</td>', '<button type="submit" name="edit" class="aslink">Edit</button>',
                            '<button type="submit" name="delete" class="aslink redlink">Delete</button>',
                            '<th>Summary</th>', '<th>200</th>']
    for content in not_expected_content:
        assert content not in firefox_driver_logged_in.page_source


def test_selenium_basic__add_more_categories(firefox_driver_logged_in):
    firefox_driver_logged_in.find_element_by_link_text('Settings').click()
    data = {'cat_1': 150, 'cat_2': 250, 'cat_3': 50, 'cat_4': 400}
    for k, v in data.items():
        firefox_driver_logged_in.find_element_by_name('category_name').send_keys(k)
        firefox_driver_logged_in.find_element_by_name('category_limit').send_keys(v)
        firefox_driver_logged_in.find_element_by_id('add_category').click()
        assert 'Category added!' in firefox_driver_logged_in.page_source
        assert k in firefox_driver_logged_in.page_source
    assert '<th>850</th>' in firefox_driver_logged_in.page_source


def test_selenium_basic__start_period(firefox_driver_logged_in):
    firefox_driver_logged_in.find_element_by_link_text('Settings').click()
    firefox_driver_logged_in.find_element_by_name('period_name').send_keys('new_period')
    firefox_driver_logged_in.find_element_by_id('start_period').click()
    assert 'Period started!' in firefox_driver_logged_in.page_source
    assert 'Actual period: new_period' in firefox_driver_logged_in.page_source
    assert '<input id="stop_period" class="btn" type="submit" style="background-color: #ff0000" value="Stop period">' \
           in firefox_driver_logged_in.page_source
    assert '/settings' in firefox_driver_logged_in.current_url
    assert 'Settings' == firefox_driver_logged_in.title
    firefox_driver_logged_in.find_element_by_link_text('Home').click()
    assert 'Home' == firefox_driver_logged_in.title
    assert 'No active period! Go to settings and start one!' not in firefox_driver_logged_in.page_source
    expected_content = ['new_period', 'placeholder="Transaction value"', 'placeholder="Description"',
                        '<option>cat_1</option>', '<option>cat_2</option>', '<option>cat_3</option>',
                        '<option>cat_4</option>']
    for content in expected_content:
        assert content in firefox_driver_logged_in.page_source


def test_selenium_basic__add_transaction(firefox_driver_logged_in):
    firefox_driver_logged_in.find_element_by_name('transaction_value').send_keys('25')
    firefox_driver_logged_in.find_element_by_name('transaction_desc').send_keys('transaction_1')
    select = Select(firefox_driver_logged_in.find_element_by_id('transaction_category'))
    select.select_by_visible_text('cat_3')
    firefox_driver_logged_in.find_element_by_id('add_transaction').click()
    assert 'Home' == firefox_driver_logged_in.title
    assert 'Transaction added!' in firefox_driver_logged_in.page_source
    expected_content = ['<th>Value</th>', '<th>Description</th>', '<th>Category</th>', '<th>Options</th>',
                        '<td>transaction_1</td>', '<td>-25</td>', '<td>cat_3</td>',
                        '<button type="submit" name="edit" class="aslink">Edit</button>',
                        '<button type="submit" name="delete" class="aslink redlink">Delete</button>',
                        '<th>Summary</th>', '<th>-25</th>', '<a href="/">Overall</a>',
                        '<a href="/categories">Categories</a>']
    for content in expected_content:
        assert content in firefox_driver_logged_in.page_source


def test_selenium_basic__edit_transaction_with_wrong_data(firefox_driver_logged_in):
    firefox_driver_logged_in.find_element_by_name('edit').click()
    firefox_driver_logged_in.find_element_by_name('transaction_value').clear()
    firefox_driver_logged_in.find_element_by_name('transaction_value').send_keys('')
    firefox_driver_logged_in.find_element_by_name('transaction_desc').clear()
    firefox_driver_logged_in.find_element_by_name('transaction_desc').send_keys('desc')
    select = Select(firefox_driver_logged_in.find_element_by_id('transaction_category'))
    select.select_by_visible_text('cat_3')
    firefox_driver_logged_in.find_element_by_id('submit').click()
    assert 'Home' == firefox_driver_logged_in.title
    assert 'Transaction value should be a number!'
    firefox_driver_logged_in.find_element_by_name('transaction_value').clear()
    firefox_driver_logged_in.find_element_by_name('transaction_value').send_keys('100')
    firefox_driver_logged_in.find_element_by_name('transaction_desc').clear()
    firefox_driver_logged_in.find_element_by_name('transaction_desc').send_keys('')
    select = Select(firefox_driver_logged_in.find_element_by_id('transaction_category'))
    select.select_by_visible_text('cat_3')
    firefox_driver_logged_in.find_element_by_id('submit').click()
    assert 'Home' == firefox_driver_logged_in.title
    assert 'Please insert transaction description' in firefox_driver_logged_in.page_source
    firefox_driver_logged_in.find_element_by_name('transaction_value').clear()
    firefox_driver_logged_in.find_element_by_name('transaction_value').send_keys('100')
    firefox_driver_logged_in.find_element_by_name('transaction_desc').clear()
    firefox_driver_logged_in.find_element_by_name('transaction_desc').send_keys('desc')
    select = Select(firefox_driver_logged_in.find_element_by_id('transaction_category'))
    select.select_by_value('0')
    firefox_driver_logged_in.find_element_by_id('submit').click()
    assert 'Home' == firefox_driver_logged_in.title
    assert 'Category was not set!'


def test_selenium_basic__edit_transaction(firefox_driver_logged_in):
    firefox_driver_logged_in.find_element_by_name('edit').click()
    firefox_driver_logged_in.find_element_by_name('transaction_value').clear()
    firefox_driver_logged_in.find_element_by_name('transaction_value').send_keys('100')
    firefox_driver_logged_in.find_element_by_name('transaction_desc').clear()
    firefox_driver_logged_in.find_element_by_name('transaction_desc').send_keys('desc')
    select = Select(firefox_driver_logged_in.find_element_by_id('transaction_category'))
    select.select_by_visible_text('cat_2')
    firefox_driver_logged_in.find_element_by_id('submit').click()
    assert 'Transaction was updated!'
    assert 'Home' == firefox_driver_logged_in.title
    expected_content = ['<th>Value</th>', '<th>Description</th>', '<th>Category</th>', '<th>Options</th>',
                        '<td>desc</td>', '<td>-100</td>', '<td>cat_2</td>',
                        '<button type="submit" name="edit" class="aslink">Edit</button>',
                        '<button type="submit" name="delete" class="aslink redlink">Delete</button>',
                        '<th>Summary</th>', '<th>-100</th>', '<a href="/">Overall</a>',
                        '<a href="/categories">Categories</a>']
    for content in expected_content:
        assert content in firefox_driver_logged_in.page_source


def test_selenium_basic__home_page_overall_charts(firefox_driver_logged_in):
    firefox_driver_logged_in.find_element_by_link_text('Overall').click()
    assert 3 == firefox_driver_logged_in.page_source.count('type="image/svg+xml"')


def test_selenium_basic__home_page_categories_charts(firefox_driver_logged_in):
    firefox_driver_logged_in.find_element_by_link_text('Categories').click()
    assert 4 == firefox_driver_logged_in.page_source.count('type="image/svg+xml"')


def test_selenium_basic__delete_transaction(firefox_driver_logged_in):
    firefox_driver_logged_in.find_element_by_name('delete').click()
    assert 'Transaction was updated!'
    assert 'Home' == firefox_driver_logged_in.title
    not_expected_content = ['<th>Value</th>', '<th>Description</th>', '<th>Category</th>', '<th>Options</th>',
                            '<td>desc</td>', '<td>-100</td>', '<td>cat_2</td>',
                            '<button type="submit" name="edit" class="aslink">Edit</button>',
                            '<button type="submit" name="delete" class="aslink redlink">Delete</button>',
                            '<th>Summary</th>', '<th>-100</th>', '<a href="/">Overall</a>',
                            '<a href="/categories">Categories</a>']
    for content in not_expected_content:
        assert content not in firefox_driver_logged_in.page_source


def test_selenium_basic__history_page_history_chart(firefox_driver_logged_in):
    firefox_driver_logged_in.find_element_by_link_text('History').click()
    assert 'There are no periods in history to show!' in firefox_driver_logged_in.page_source


def test_selenium_basic__stop_period(firefox_driver_logged_in):
    firefox_driver_logged_in.find_element_by_link_text('Settings').click()
    firefox_driver_logged_in.find_element_by_id('stop_period').click()
    assert 'Period finished!' in firefox_driver_logged_in.page_source


def test_selenium_basic__history_page_history_chart_after_period_stop(firefox_driver_logged_in):
    firefox_driver_logged_in.find_element_by_link_text('History').click()
    assert 1 == firefox_driver_logged_in.page_source.count('type="image/svg+xml"')


def test_selenium_basic__delete_period(firefox_driver_logged_in):
    firefox_driver_logged_in.find_element_by_link_text('History').click()
    firefox_driver_logged_in.find_element_by_name('delete').click()
    assert 'Period was deleted successfully!' in firefox_driver_logged_in.page_source
    assert 'There are no periods in history to show!' in firefox_driver_logged_in.page_source
