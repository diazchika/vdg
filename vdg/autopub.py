import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC


class WebAutomationBase:
    def __init__(self):
        self.driver = None

    def random_delay(self, min_delay=0.5, max_delay=1):
        time.sleep(random.uniform(min_delay, max_delay))

    def get_driver(self):
        options = Options()
        options.add_argument("--width=1920")
        options.add_argument("--height=1080")
        profile = webdriver.FirefoxProfile()
        profile.set_preference("general.useragent.override", "Mozilla/5.0 (iPhone14,3; U; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/19A346 Safari/602.1")
        profile.set_preference("dom.webdriver.enabled", False)
        profile.set_preference("useAutomationExtension", False)
        profile.set_preference("privacy.trackingprotection.enabled", True)
        profile.update_preferences()
        options.profile = profile
        self.driver = webdriver.Firefox(options=options)

    def wait_for_element(self, by, value, timeout=10):
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )

    def wait_for_clickable(self, by, value, timeout=10):
        return WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable((by, value))
        )

    def wait_for_staleness(self, element, timeout=10):
        WebDriverWait(self.driver, timeout).until(EC.staleness_of(element))

    def attribute_value_is(self, locator, attribute, value):
        def _predicate(driver):
            element = driver.find_element(*locator)
            return value in element.get_attribute(attribute)
        return _predicate

    # def load_config(self, config_file):
    #     config = configparser.ConfigParser()
    #     config.read(config_file)
    #     return config

    def click_element(self, xpath):
        element = self.wait_for_clickable(By.XPATH, xpath)
        element.click()
        self.random_delay()

    def enter_text(self, xpath, text):
        field = self.wait_for_element(By.XPATH, xpath)
        field.send_keys(text)
        self.random_delay()

    def select_dropdown_by_text(self, xpath, text):
        dropdown = self.wait_for_element(By.XPATH, xpath)
        select = Select(dropdown)
        select.select_by_visible_text(text)
        self.random_delay()

    def upload_file(self, xpath, file_path):
        upload_field = self.wait_for_element(By.XPATH, xpath)
        upload_field.send_keys(file_path)
        self.random_delay()

    def switch_to_frame(self, xpath):
        frame = self.wait_for_element(By.XPATH, xpath)
        self.driver.switch_to.frame(frame)

    def select_dropdown_by_value(self, xpath, value):
        dropdown = self.wait_for_element(By.XPATH, xpath)
        select = Select(dropdown)
        select.select_by_value(value)
        self.random_delay()

class BangumiUploader(WebAutomationBase):
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

    def run(self, username, password, title, cat, desc, torrent_path):
        self.get_driver()
        self.driver.get("https://bangumi.moe")

        # Close Tutorial
        self.wait_for_element(By.XPATH, "/html/body/div[6]/div/div[4]/a[1]")
        overlay = self.driver.find_element(By.XPATH, "/html/body/div[5]")
        self.click_element("/html/body/div[6]/div/div[4]/a[1]")
        self.wait_for_staleness(overlay)

        # Login
        self.click_element(self.LOGIN_BUTTON_XPATH)
        self.enter_text(self.USERNAME_FIELD_XPATH, username)
        self.enter_text(self.PASSWORD_FIELD_XPATH, password)
        self.click_element(self.SIGNIN_BUTTON_XPATH)

        # Form filling
        self.click_element(self.PUBLISH_BUTTON_XPATH)
        self.click_element(self.OLD_VERSION_BUTTON_XPATH)
        self.enter_text(self.TITLE_FIELD_XPATH, title)
        self.select_dropdown_by_value(self.CAT_SELECT_DROPDOWN_XPATH, cat)
        self.click_element(self.SOURCE_CODE_BUTTON_XPATH)
        self.enter_text(self.SOURCE_CODE_FIELD_XPATH, desc)
        self.upload_file(self.UPLOAD_BUTTON_XPATH, torrent_path)
        self.click_element(self.VCB_IDENTITY_BUTTON_XPATH)
        self.click_element(self.TEAM_SYNC_CHECKBOX_XPATH)
        print("Please press the Upload button manually and close the geckodriver after you are done.")
        input("Press Enter to quit...")
        self.driver.close()
        # self.click_element(self.FINAL_PUBLISH_BUTTON_XPATH)

class NyaaUploader(WebAutomationBase):
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

    def run(self, username, password, title, cat, desc, torrent_path):
        self.get_driver()
        self.driver.get("https://nyaa.si/login")

        # Wait for page to load
        self.wait_for_element(By.XPATH, self.CAPTCHA_IFRAME_XPATH)

        # Login
        self.enter_text(self.USERNAME_FIELD_XPATH, username)
        self.enter_text(self.PASSWORD_FIELD_XPATH, password)
        print("Please finish captcha manually.")
        self.switch_to_frame(self.CAPTCHA_IFRAME_XPATH) # Switch to CAPTCHA iframe
        # Wait for CAPTCHA to be checked
        WebDriverWait(self.driver, 300).until(self.attribute_value_is(
            (By.XPATH, self.CAPTCHA_ANCHOR_XPATH), 'class', 'recaptcha-checkbox-checked')
        )
        self.driver.switch_to.default_content() # Switch back
        self.click_element(self.LOGIN_BUTTON_XPATH)

        # Form filling
        self.click_element(self.UPLOAD_BUTTON_XPATH)
        self.upload_file(self.TORRENT_PATH_FIELD_XPATH, torrent_path)
        self.enter_text(self.TITLE_FIELD_XPATH, title)
        self.select_dropdown_by_value(self.CATEGORY_DROPDOWN_XPATH, cat)
        self.click_element(self.COMPLETE_BUTTON_XPATH)
        self.enter_text(self.INFORMATION_FIELD_XPATH, "https://vcb-s.com/archives/138")
        self.enter_text(self.DESCRIPTION_FIELD_XPATH, desc)
        print("Please press the Upload button manually and close the geckodriver after you are done.")
        input("Press Enter to quit...")
        self.driver.close()
