from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options

import json
import os


CHROME_DRIVER_PATH = (
    os.getenv('CHROME_DRIVER_PATH') or 'C:/Users/prouh/AppData/Local/Google/Chrome/Application/chromedriver.exe'
)


class LinkedinMessengerBot:

    def __init__(self):
        chrome_path = CHROME_DRIVER_PATH
        chrome_options = Options()
        chrome_options.add_argument('user-data-dir=selenium') 
        self.driver = webdriver.Chrome(chrome_path, chrome_options=chrome_options)

    def go_to_messaging(self):
        self.driver.get('https://www.linkedin.com')
        try:
            self.login()
        except NoSuchElementException:
            print('Already logged !')
            pass
        self.driver.find_element_by_id('messaging-nav-item').click()

    def login(self):
        if os.path.isfile('credentials.json'):
            with open('credentials.json', 'r') as f:
                credentials = json.load(f)
        email = self.driver.find_element_by_id('login-email')
        password = self.driver.find_element_by_id('login-password')
        email.send_keys(credentials['email'])
        password.send_keys(credentials['password'])
        self.driver.find_element_by_id('login-submit').click()


if __name__ == '__main__':
    LinkedinMessengerBot().go_to_messaging()
