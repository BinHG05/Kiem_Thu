from tests.pages import LoginPage


def test_login_page_opens_with_a_visible_form(driver):
    login_page = LoginPage(driver).open()

    assert login_page.is_login_page()
    assert login_page.is_form_visible()


def test_username_and_password_are_empty_on_first_load(driver):
    login_page = LoginPage(driver).open()

    assert login_page.username_value() == ""
    assert login_page.password_value() == ""


def test_username_field_accepts_text(driver):
    login_page = LoginPage(driver).open()

    login_page.enter_username("student-test")

    assert login_page.username_value() == "student-test"


def test_password_field_accepts_text(driver):
    login_page = LoginPage(driver).open()

    login_page.enter_password("sample-password")

    assert login_page.password_value() == "sample-password"


def test_password_field_is_masked(driver):
    login_page = LoginPage(driver).open()

    assert login_page.password_input_type() == "password"


def test_login_button_has_expected_label(driver):
    login_page = LoginPage(driver).open()

    assert login_page.login_button_text() == "Đăng nhập"


def test_remember_me_is_unselected_on_first_load(driver):
    login_page = LoginPage(driver).open()

    assert not login_page.is_remember_me_selected()
