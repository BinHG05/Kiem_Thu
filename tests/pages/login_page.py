from urllib.parse import urlparse

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from tests.pages.base_page import BasePage


class LoginPage(BasePage):
    URL = "https://vanphongdientu.utc.edu.vn/Login"

    USERNAME = (By.NAME, "username")
    PASSWORD = (By.NAME, "userpwd")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "input.submit_login")
    REMEMBER_ME = (By.ID, "persistent")
    REMEMBER_ME_LABEL = (By.CSS_SELECTOR, "label[for='persistent']")
    FORGOT_PASSWORD_LINK = (By.CSS_SELECTOR, "a[href='/Login/GetPass']")
    GOOGLE_LOGIN_LINK = (By.CSS_SELECTOR, "a.button[href*='accounts.google.com']")

    def open(self):
        self.driver.get(self.URL)
        self.wait_for_element(self.USERNAME)
        return self

    def login(self, username, password):
        self.enter_username(username)
        if password:
            self.enter_password(password)
        return self.click(self.LOGIN_BUTTON)

    def enter_username(self, username):
        self.type(self.USERNAME, username)

    def enter_password(self, password):
        self.type(self.PASSWORD, password)

    def is_login_page(self):
        path = urlparse(self.driver.current_url).path.rstrip("/").lower()
        return path.endswith("/login")

    def is_form_visible(self):
        return all(
            self.is_visible(locator)
            for locator in (self.USERNAME, self.PASSWORD, self.LOGIN_BUTTON)
        )

    def username_value(self):
        return self.get_attribute(self.USERNAME, "value")

    def password_value(self):
        return self.get_attribute(self.PASSWORD, "value")

    def password_input_type(self):
        return self.get_attribute(self.PASSWORD, "type")

    def login_button_text(self):
        return self.get_attribute(self.LOGIN_BUTTON, "value")

    def is_remember_me_selected(self):
        return self.driver.find_element(*self.REMEMBER_ME).is_selected()

    def select_remember_me(self):
        if not self.is_remember_me_selected():
            self.click(self.REMEMBER_ME_LABEL)

    def forgot_password_url(self):
        return self.get_attribute(self.FORGOT_PASSWORD_LINK, "href")

    def google_login_url(self):
        return self.get_attribute(self.GOOGLE_LOGIN_LINK, "href")

    def wait_for_form_submission(self, submit_button):
        """Wait until the POST response replaces the submitted login form."""
        self.wait.until(EC.staleness_of(submit_button))

    def wait_for_login_success(self, submit_button):
        self.wait_for_form_submission(submit_button)
        return not self.is_login_page()
