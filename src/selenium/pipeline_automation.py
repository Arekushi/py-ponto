import logging
import pyautogui
from typing import List
from time import sleep
from config.config import settings

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from src.selenium.action_type import ActionType as AT


class PipelineAutomation:
    def __init__(self, url, actions, wait_time=60):
        self.url = url
        self.actions = actions
        self.wait_time = wait_time
        
        options = webdriver.ChromeOptions()
        has_chrome_userdata = getattr(settings, 'chrome', None) \
            and getattr(settings.chrome, 'userdata', None)
        
        if has_chrome_userdata:
            options.add_argument(rf"--user-data-dir={settings.chrome.userdata}")
            options.add_argument(r'--profile-directory=Default')
            options.add_experimental_option('detach', True)
        
        self.driver = webdriver.Chrome(
            options=options,
            service=Service(ChromeDriverManager().install())
        )
        
        self.wait = WebDriverWait(self.driver, self.wait_time)
        self.driver.get(self.url)

        self.action_map = {
            AT.CLICK: self.wait_and_click,
            AT.INPUT: self.wait_and_input_text,
            AT.WAIT_FOR: self.wait_for_element,
            AT.SLEEP: self.sleep_for_time,
            AT.KEYBOARD_SHORTCUT: self.execute_keyboard_shortcut,
            AT.CUSTOM: self.execute_custom_action
        }

    def wait_and_click(self, xpath: str):
        try:
            element = self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
            element.click()
            logging.info(f"Elemento com XPATH '{xpath}' clicado com sucesso.")
        except Exception as e:
            raise Exception(f"Erro ao clicar no elemento de XPATH: '{xpath}'\n{e}")

    def wait_and_input_text(self, xpath: str, value):
        try:
            element = self.wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
            element.clear()
            element.send_keys(value)
            
            logging.info(f"Texto foi inserido no elemento com XPATH '{xpath}'.")
        except Exception as e:
            raise Exception(f"Erro ao dar input no elemento de XPATH: '{xpath}'\n{e}")
    
    def sleep_for_time(self, time: float):
        sleep(time)
        logging.info(f"Dormiu por {time} segundo(s).")

    def wait_for_element(self, xpath: str):
        try:
            element = self.wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
            logging.info(f"Elemento com XPATH '{xpath}' encontrado.")
            return element
        except Exception as e:
            raise Exception(f"Erro ao tentar encontrar o elemento de XPATH: '{xpath}'\n{e}")
    
    def execute_custom_action(self, callback):
        try:
            callback(self.driver, self.wait)
            logging.info("Ação customizada executada com sucesso.")
        except Exception as e:
            raise Exception(f"Erro ao executar ação customizada: {e}")
    
    def execute_keyboard_shortcut(self, keys: List[str], redo_time: float):
        try:
            pyautogui.hotkey(*keys)
            
            if redo_time > 0:
                sleep(redo_time)
                pyautogui.hotkey(*keys)
            
            logging.info("Atalho de teclado executado com sucesso.")
        except Exception as e:
            raise Exception(f"Erro ao executar atalho de teclado: {e}")

    def execute_pipeline(self):
        for action in self.actions:
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
                else:
                    func(xpath)
                
                for callback in callbacks:
                    callback()

    def quit(self):
        self.driver.quit()
