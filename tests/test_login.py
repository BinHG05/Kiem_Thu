import os

import allure
import pytest

from tests.pages import LoginPage


@allure.epic("UTC Electronic Office")
@allure.feature("Login page")
@allure.story("Login form availability")
@allure.title("TC01 - Login form is visible")
@allure.severity(allure.severity_level.CRITICAL)
def test_login_page_opens_with_a_visible_form(driver):
    login_page = LoginPage(driver).open()

    assert login_page.is_login_page()
    assert login_page.is_form_visible()


@allure.epic("UTC Electronic Office")
@allure.feature("Login page")
@allure.story("Initial form state")
@allure.title("TC02 - Login fields start empty")
@allure.severity(allure.severity_level.NORMAL)
def test_username_and_password_are_empty_on_first_load(driver):
    login_page = LoginPage(driver).open()

    assert login_page.username_value() == ""
    assert login_page.password_value() == ""


@allure.epic("UTC Electronic Office")
@allure.feature("Login page")
@allure.story("Username input")
@allure.title("TC03 - Username accepts text")
@allure.severity(allure.severity_level.NORMAL)
def test_username_field_accepts_text(driver):
    login_page = LoginPage(driver).open()

    login_page.enter_username("student-test")

    assert login_page.username_value() == "student-test"


@allure.epic("UTC Electronic Office")
@allure.feature("Login page")
@allure.story("Password input")
@allure.title("TC04 - Password accepts text")
@allure.severity(allure.severity_level.NORMAL)
def test_password_field_accepts_text(driver):
    login_page = LoginPage(driver).open()

    login_page.enter_password("sample-password")

    assert login_page.password_value() == "sample-password"


@allure.epic("UTC Electronic Office")
@allure.feature("Login page")
@allure.story("Password input")
@allure.title("TC05 - Password is masked")
@allure.severity(allure.severity_level.CRITICAL)
def test_password_field_is_masked(driver):
    login_page = LoginPage(driver).open()

    assert login_page.password_input_type() == "password"


@allure.epic("UTC Electronic Office")
@allure.feature("Login page")
@allure.story("Login form controls")
@allure.title("TC06 - Login button has the expected label")
@allure.severity(allure.severity_level.MINOR)
def test_login_button_has_expected_label(driver):
    login_page = LoginPage(driver).open()

    assert login_page.login_button_text() == "Đăng nhập"


@allure.epic("UTC Electronic Office")
@allure.feature("Login page")
@allure.story("Remember me")
@allure.title("TC07 - Remember me is unselected by default")
@allure.severity(allure.severity_level.NORMAL)
def test_remember_me_is_unselected_on_first_load(driver):
    login_page = LoginPage(driver).open()

    assert not login_page.is_remember_me_selected()


@allure.epic("UTC Electronic Office")
@allure.feature("Login page")
@allure.story("Remember me")
@allure.title("TC08 - Remember me can be selected")
@allure.severity(allure.severity_level.NORMAL)
def test_remember_me_can_be_selected(driver):
    login_page = LoginPage(driver).open()

    login_page.select_remember_me()

    assert login_page.is_remember_me_selected()


@allure.epic("UTC Electronic Office")
@allure.feature("Login page")
@allure.story("Password recovery")
@allure.title("TC09 - Forgot password link targets recovery")
@allure.severity(allure.severity_level.NORMAL)
def test_forgot_password_link_targets_password_recovery(driver):
    login_page = LoginPage(driver).open()

    assert login_page.forgot_password_url().endswith("/Login/GetPass")


@allure.epic("UTC Electronic Office")
@allure.feature("Login page")
@allure.story("External authentication")
@allure.title("TC10 - Google login link targets Google Accounts")
@allure.severity(allure.severity_level.NORMAL)
def test_google_login_link_targets_google_accounts(driver):
    login_page = LoginPage(driver).open()

    assert "accounts.google.com" in login_page.google_login_url()


@allure.epic("UTC Electronic Office")
@allure.feature("Authentication")
@allure.story("Valid credentials")
@allure.title("TC11 - User can log in with valid credentials")
@allure.severity(allure.severity_level.BLOCKER)
def test_login_success(driver):
    username = os.getenv("UTC_USER")
    password = os.getenv("UTC_PASS")
    if not username or not password:
        pytest.fail(
            "TC11 needs credentials: set both UTC_USER and UTC_PASS environment variables."
        )

    login_page = LoginPage(driver).open()
    submit_button = login_page.login(username, password)

    assert login_page.wait_for_login_success(submit_button), (
        "The server responded but remained on /Login. Check the UTC credentials or "
        "the account's access to the office system."
    )
