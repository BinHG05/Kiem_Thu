import allure
import pytest
from selenium import webdriver


@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    browser = webdriver.Chrome(options=options)
    try:
        yield browser
    finally:
        browser.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Attach browser evidence to the Allure report when a test fails."""
    outcome = yield
    report = outcome.get_result()

    if report.when != "call" or not report.failed:
        return

    browser = item.funcargs.get("driver")
    if browser is None:
        return

    allure.attach(
        browser.get_screenshot_as_png(),
        name=f"{item.name}-failure",
        attachment_type=allure.attachment_type.PNG,
    )
    allure.attach(
        browser.page_source,
        name=f"{item.name}-page-source",
        attachment_type=allure.attachment_type.HTML,
    )
