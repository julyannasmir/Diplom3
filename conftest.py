import pytest
from selenium import webdriver
import helper
import requests
from pages.login_page import LoginPage
from pages.main_page import MainPage
from urls import Url


@pytest.fixture(params=["firefox"])
def driver(request):
    if request.param == 'chrome':
        driver = webdriver.Chrome()
    elif request.param == 'firefox':
        driver = webdriver.Firefox()

    driver.maximize_window()
    driver.get(Url.MAIN_PAGE)
    yield driver
    driver.quit()


@pytest.fixture()
def user_data():
    user_data = helper.generate_user_data()
    response = requests.post(Url.REGISTER_USER, user_data)
    yield user_data
    headers = {'Authorization': response.json()['accessToken']}
    requests.delete(Url.DELETE_USER, headers=headers)


@pytest.fixture()
def login_user(driver, user_data):
    MainPage(driver).enter_in_account()
    LoginPage(driver).login_user(user_data)