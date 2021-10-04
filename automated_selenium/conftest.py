import pytest
from selenium.webdriver import Firefox


@pytest.fixture
def firefox_driver():
    test_driver = Firefox('.')
    test_driver.get('')
    yield test_driver
    test_driver.close()


@pytest.fixture
def firefox_driver_logged_in():
    test_driver = Firefox('.')
    test_driver.get('')
    test_driver.find_element_by_name('username').send_keys('tester')
    test_driver.find_element_by_name('pin_code').send_keys('1234')
    test_driver.find_element_by_id('login').click()
    assert 'Logged in successfully!' in test_driver.page_source
    yield test_driver
    test_driver.close()
