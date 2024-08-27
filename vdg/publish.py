import os
import configparser
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from contextlib import contextmanager

class WebAutomationBase:
    def __init__(self):
        self.driver = None

    @contextmanager
    def get_driver(self):
        """Context manager for WebDriver to ensure it is properly closed."""
        self.driver = webdriver.Firefox()
        try:
            yield self.driver
        finally:
            self.driver.quit()

    def wait_for_element(self, by, value, timeout=10):
        """Wait until the element is present in the DOM."""
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )

    def wait_for_clickable(self, by, value, timeout=10):
        """Wait until the element is clickable."""
        return WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable((by, value))
        )

    def wait_for_staleness(self, element, timeout=10):
        """Wait until the element is no longer attached to the DOM."""
        WebDriverWait(self.driver, timeout).until(EC.staleness_of(element))

    def attribute_value_is(self, locator, attribute, value):
        """An expectation for checking that an element's attribute has a specific value."""
        def _predicate(driver):
            element = driver.find_element(*locator)
            return value in element.get_attribute(attribute)
        return _predicate

    def load_config(self, config_file):
        """Load configuration from the specified file."""
        config = configparser.ConfigParser()
        config.read(config_file)
        return config

    def click_element(self, xpath):
        """Click an element specified by the XPath."""
        element = self.wait_for_clickable(By.XPATH, xpath)
        element.click()

    def enter_text(self, xpath, text):
        """Enter text into an input field specified by the XPath."""
        field = self.wait_for_element(By.XPATH, xpath)
        field.send_keys(text)

    def select_dropdown_by_text(self, xpath, text):
        """Select an option from a dropdown by visible text."""
        dropdown = self.wait_for_element(By.XPATH, xpath)
        select = Select(dropdown)
        select.select_by_visible_text(text)

    def upload_file(self, xpath, file_path):
        """Upload a file using the input field specified by the XPath."""
        upload_field = self.wait_for_element(By.XPATH, xpath)
        upload_field.send_keys(file_path)

class BangumiMoeAutomation(WebAutomationBase):
    LOGIN_BUTTON_XPATH = '//*[@id="main-menu-button"]'
    USERNAME_FIELD_XPATH = '/html/body/div[4]/md-dialog/md-content/form/md-input-group[1]/input'
    PASSWORD_FIELD_XPATH = '/html/body/div[4]/md-dialog/md-content/form/md-input-group[3]/input'
    SIGNIN_BUTTON_XPATH = '/html/body/div[4]/md-dialog/div/button[3]'
    PUBLISH_BUTTON_XPATH = '/html/body/div[1]/ul[2]/li[3]'
    OLD_VERSION_BUTTON_XPATH = '/html/body/div[4]/md-dialog/h2/span/button[2]/i'
    TITLE_FIELD_XPATH = '//*[@id="torrent-title"]'
    CAT_SELECT_DROPDOWN_XPATH = '/html/body/div[4]/md-dialog/md-content/div[1]/select'
    SOURCE_CODE_BUTTON_XPATH = '/html/body/div[4]/md-dialog/md-content/div[3]/ul/li[1]/a'
    SOURCE_CODE_FIELD_XPATH = '/html/body/div[4]/md-dialog/md-content/div[3]/textarea'
    VCB_IDENTITY_BUTTON_XPATH = '/html/body/div[4]/md-dialog/md-content/div[4]/md-list/md-item'
    TEAM_SYNC_CHECKBOX_XPATH = '/html/body/div[4]/md-dialog/md-content/md-checkbox'
    UPLOAD_BUTTON_XPATH = '/html/body/div[4]/md-dialog/md-content/input'
    FINAL_PUBLISH_BUTTON_XPATH = '/html/body/div[4]/md-dialog/div/button[2]'

    def login(self):
        """Perform login operation."""
        self.click_element(self.LOGIN_BUTTON_XPATH)
        self.enter_text(self.USERNAME_FIELD_XPATH, "littlepox")
        self.enter_text(self.PASSWORD_FIELD_XPATH, "bangumi_moe@VCB-Studio@Publish")
        self.click_element(self.SIGNIN_BUTTON_XPATH)

    def publish_torrent(self):
        """Perform torrent publishing operation."""
        self.click_element(self.PUBLISH_BUTTON_XPATH)
        self.click_element(self.OLD_VERSION_BUTTON_XPATH)
        self.enter_text(self.TITLE_FIELD_XPATH, "test")
        self.select_dropdown_by_value(self.CAT_SELECT_DROPDOWN_XPATH, "0")
        self.click_element(self.SOURCE_CODE_BUTTON_XPATH)
        self.enter_text(self.SOURCE_CODE_FIELD_XPATH, "test")
        self.click_element(self.VCB_IDENTITY_BUTTON_XPATH)
        self.click_element(self.TEAM_SYNC_CHECKBOX_XPATH)
        self.upload_file(self.UPLOAD_BUTTON_XPATH, "/home/damocles/Downloads/test.torrent")
        # self.click_element(self.FINAL_PUBLISH_BUTTON_XPATH)

    def run(self):
        with self.get_driver() as driver:
            driver.get("https://bangumi.moe")
            self.wait_for_element(By.XPATH, "/html/body/div[6]/div/div[4]/a[1]")
            print("Page is fully loaded")
            self.click_element("/html/body/div[6]/div/div[4]/a[1]")
            overlay = driver.find_element(By.XPATH, "/html/body/div[5]")
            self.wait_for_staleness(overlay)
            self.login()
            self.publish_torrent()

class NyaaSiAutomation(WebAutomationBase):
    LOGIN_URL = "https://nyaa.si/login"
    CAPTCHA_IFRAME_XPATH = "/html/body/div[1]/form/div[3]/div/div/div/div/iframe"
    USERNAME_FIELD_XPATH = '//*[@id="username"]'
    PASSWORD_FIELD_XPATH = '//*[@id="password"]'
    CAPTCHA_ANCHOR_XPATH = '//*[@id="recaptcha-anchor"]'
    LOGIN_BUTTON_XPATH = '/html/body/div[1]/form/div[4]/div/input'
    UPLOAD_BUTTON_XPATH = '/html/body/nav/div/div[2]/ul[1]/li[1]/a'
    TORRENT_PATH_FIELD_XPATH = '//*[@id="torrent_file"]'
    TITLE_FIELD_XPATH = '//*[@id="display_name"]'
    CATEGORY_DROPDOWN_XPATH = '//*[@id="category"]'
    COMPLETE_BUTTON_XPATH = '/html/body/div/form/div[3]/div[2]/div[3]/label[2]'
    INFORMATION_FIELD_XPATH = '//*[@id="information"]'
    DESCRIPTION_FIELD_XPATH = '//*[@id="description"]'

    def login(self):
        """Perform login operation."""
        self.driver.get(self.LOGIN_URL)
        self.wait_for_element(By.XPATH, self.CAPTCHA_IFRAME_XPATH)
        print("Page is fully loaded")
        self.enter_text(self.USERNAME_FIELD_XPATH, "nyaa@vcb-s.com")
        self.enter_text(self.PASSWORD_FIELD_XPATH, "nyaa_si@VCB-Studio@Publish")
        print("Please finish captcha manually.")
        self.switch_to_frame(self.CAPTCHA_IFRAME_XPATH)
        WebDriverWait(self.driver, 300).until(self.attribute_value_is((By.XPATH, self.CAPTCHA_ANCHOR_XPATH), 'class', 'recaptcha-checkbox-checked'))
        self.driver.switch_to.default_content()
        self.click_element(self.LOGIN_BUTTON_XPATH)

    def publish_torrent(self):
        """Perform torrent publishing operation."""
        self.click_element(self.UPLOAD_BUTTON_XPATH)
        self.upload_file(self.TORRENT_PATH_FIELD_XPATH, "/home/damocles/Downloads/test.torrent")
        self.enter_text(self.TITLE_FIELD_XPATH, "test")
        self.select_dropdown_by_value(self.CATEGORY_DROPDOWN_XPATH, "1_3")
        self.click_element(self.COMPLETE_BUTTON_XPATH)
        self.enter_text(self.INFORMATION_FIELD_XPATH, "test")
        self.enter_text(self.DESCRIPTION_FIELD_XPATH, "test")

    def run(self):
        with self.get_driver() as driver:
            self.login()
            self.publish_torrent()

    def switch_to_frame(self, xpath):
        """Switch to the iframe specified by the XPath."""
        frame = self.wait_for_element(By.XPATH, xpath)
        self.driver.switch_to.frame(frame)

    def select_dropdown_by_value(self, xpath, value):
        """Select an option from a dropdown by value."""
        dropdown = self.wait_for_element(By.XPATH, xpath)
        select = Select(dropdown)
        select.select_by_value(value)

# Example usage:
# if __name__ == "__main__":
#     automation = BangumiMoeAutomation()
#     automation.run()
#     nyaa_automation = NyaaSiAutomation()
#     nyaa_automation.run()