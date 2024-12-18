import logging
import pyautogui
from typing import List
from time import sleep
from config.config import settings

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

from src.exceptions.automation_pipeline_exception import AutomationPipelineException
from src.automation.selenium_automation_context import SeleniumAutomationContext
from src.automation.action_type import ActionType as AT
from src.automation.web_browser import WebBrowser


class SeleniumAutomation:
    def __init__(self, url, wait_time=60):
        self.url = url        
        self.driver = self.__setup_driver()
        self.wait = WebDriverWait(self.driver, wait_time)
        self.driver.get(self.url)

        self.action_map = {
            AT.CLICK: self.wait_and_click,
            AT.INPUT: self.wait_and_input_text,
            AT.WAIT_FOR: self.wait_for_element,
            AT.SLEEP: self.sleep_for_time,
            AT.KEYBOARD_SHORTCUT: self.execute_keyboard_shortcut,
            AT.CUSTOM: self.execute_custom_action,
            AT.IF_ELSE: self.execute_if_else
        }
    
    def __setup_driver(self):
        web_browser = settings.browser.default
        
        if web_browser == WebBrowser.GOOGLE_CHROME.value:
            options = webdriver.ChromeOptions()
            
            if (getattr(settings.browser, 'userdata', None)):
                options.add_argument(rf"--user-data-dir={settings.browser.userdata}")
                options.add_argument(r'--profile-directory=Default')
                options.add_experimental_option('detach', True)
            
            return webdriver.Chrome(
                options=options,
                service=ChromeService(ChromeDriverManager().install())
            )
            
        elif web_browser == WebBrowser.FIREFOX.value:
            options = webdriver.FirefoxOptions()
            
            if (getattr(settings.browser, 'userdata', None)):
                options.add_argument("-profile")
                options.add_argument(settings.browser.userdata)
            
            return webdriver.Firefox(
                options=options,
                service=FirefoxService(GeckoDriverManager().install())
            )
        
        raise AutomationPipelineException(
            f'Opção de WebBrowser não suportada: {web_browser}'
        )
    
    def wait_and_click(self, xpath: str):
        try:
            element = self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
            element.click()
            logging.info(f"Elemento com XPATH '{xpath}' clicado com sucesso.")
        except Exception as e:
            raise AutomationPipelineException(
                message=f"Erro ao clicar no elemento de XPATH: '{xpath}'\n{e}"
            )

    def wait_and_input_text(self, xpath: str, value):
        try:
            element = self.wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
            element.clear()
            element.send_keys(value)
            
            logging.info(f"Texto foi inserido no elemento com XPATH '{xpath}'.")
        except Exception as e:
            raise AutomationPipelineException(
                message=f"Erro ao dar input no elemento de XPATH: '{xpath}'\n{e}"
            )
    
    def sleep_for_time(self, time: float):
        sleep(time)
        logging.info(f"Dormiu por {time} segundo(s).")

    def wait_for_element(self, xpath: str):
        try:
            element = self.wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
            logging.info(f"Elemento com XPATH '{xpath}' encontrado.")
            return element
        except Exception as e:
            raise AutomationPipelineException(
                message=f"Erro ao tentar encontrar o elemento de XPATH: '{xpath}'\n{e}"
            )
    
    def execute_custom_action(self, callback):
        try:
            callback(SeleniumAutomationContext(self.driver, self.wait))
            logging.info("Ação customizada executada com sucesso.")
        except Exception as e:
            raise AutomationPipelineException(
                message=f"Erro ao executar ação customizada: {e}"
            )
    
    def execute_keyboard_shortcut(self, keys: List[str], redo_time: float):
        try:
            pyautogui.hotkey(*keys)
            
            if redo_time > 0:
                sleep(redo_time)
                pyautogui.hotkey(*keys)
            
            logging.info("Atalho de teclado executado com sucesso.")
        except Exception as e:
            raise AutomationPipelineException(
                message=f"Erro ao executar atalho de teclado: {e}"
            )

    def execute_if_else(self, condition_callback, true_actions, false_actions):
        try:
            result = condition_callback(SeleniumAutomationContext(self.driver, self.wait))
            
            if result:
                self.execute_pipeline(true_actions)
            else:
                self.execute_pipeline(false_actions)
        except Exception as e:
            raise AutomationPipelineException(
                f"Não foi possível executar o IF e ELSE: {e}"
            )

    def execute_pipeline(self, actions):
        for action in actions:
            action_type = action.get('type')
            xpath = action.get('xpath', None)
            callbacks = action.get('callbacks', [])
            func = self.action_map.get(action_type)
            
            if func:
                if (action_type == AT.INPUT):
                    value = action.get('value')
                    func(xpath, value)
                elif (action_type == AT.CUSTOM):
                    callback = action.get('callback')
                    func(callback)
                elif (action_type == AT.SLEEP):
                    time = float(action.get('time'))
                    func(time)
                elif (action_type == AT.KEYBOARD_SHORTCUT):
                    keys = action.get('keys', [])
                    undo_time = float(action.get('redo_time', 0))
                    func(keys, undo_time)
                elif (action_type == AT.IF_ELSE):
                    condition_callback = action.get('condition')
                    true_actions = action.get('true', [])
                    false_actions = action.get('false', [])
                    func(condition_callback, true_actions, false_actions)
                else:
                    func(xpath)
                
                for callback in callbacks:
                    callback()

    def quit(self):
        self.driver.quit()
