from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from src.selenium.action_type import ActionType as AT
from time import sleep
import logging


class PipelineAutomation:
    def __init__(self, url, wait_time=60):
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install())
        )
        self.wait = WebDriverWait(self.driver, wait_time)
        self.driver.get(url)

        self.action_map = {
            AT.CLICK: self.wait_and_click,
            AT.INPUT: self.wait_and_input_text,
            AT.WAIT_FOR: self.wait_for_element,
            AT.SLEEP: self.sleep_for_time,
            AT.CUSTOM: self.execute_custom_action
        }

    def wait_and_click(self, xpath):
        try:
            element = self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
            element.click()
            logging.info(f"Elemento com XPATH '{xpath}' clicado com sucesso.")
        except Exception as e:
            raise Exception(f"Erro ao clicar no elemento de XPATH: '{xpath}'\n{e}")

    def wait_and_input_text(self, xpath, value):
        try:
            element = self.wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
            element.clear()
            element.send_keys(value)
            
            logging.info(f"Texto foi inserido no elemento com XPATH '{xpath}'.")
        except Exception as e:
            raise Exception(f"Erro ao dar input no elemento de XPATH: '{xpath}'\n{e}")
            
    def sleep_for_time(self, time):
        sleep(time)
        logging.info(f"Dormido por {time} segundos")

    def wait_for_element(self, xpath):
        try:
            element = self.wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
            logging.info(f"Elemento com XPATH '{xpath}' encontrado.")
            return element
        except Exception as e:
            raise Exception(f"Erro ao tentar encontrar o elemento de XPATH: '{xpath}'\n{e}")
    
    def execute_custom_action(self, callback):
        try:
            callback(self.driver, self.wait)
            logging.info("Ação customizada executada com sucesso")
        except Exception as e:
            raise Exception(f"Erro ao executar ação customizada: {e}")

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
                    time = action.get('time')
                    func(time)
                else:
                    func(xpath)
                
                for callback in callbacks:
                    callback()

    def quit(self):
        self.driver.quit()
