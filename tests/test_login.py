from tests.pages import LoginPage


def test_login_page_opens_with_a_visible_form(driver):
    login_page = LoginPage(driver).open()

    assert login_page.is_login_page()
    assert login_page.is_form_visible()


def test_username_and_password_are_empty_on_first_load(driver):
    login_page = LoginPage(driver).open()

    assert login_page.username_value() == ""
    assert login_page.password_value() == ""
