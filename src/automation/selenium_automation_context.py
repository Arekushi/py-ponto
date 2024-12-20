from dataclasses import dataclass
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait


@dataclass
class SeleniumAutomationContext:
    driver: WebDriver
    wait: WebDriverWait
