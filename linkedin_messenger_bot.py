from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options

import json
import os
import time


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
        self.driver.find_element_by_id('messaging-nav-item').click()

    def get_nth_conversation(self, n):
        time.sleep(5)
        conversation_list = self.driver.find_element_by_class_name(
            'msg-conversations-container__conversations-list'
        )
        conversations = conversation_list.find_elements_by_tag_name('li')
        if len(conversations) <= n:
            return 'This conversation does not exist.'
        conversations[n].click()
        first_conversation = self.driver.find_element_by_class_name('msg-s-message-list')
        messages = first_conversation.find_elements_by_tag_name('li')[1:]
        for message in messages:
            links = message.find_elements_by_class_name('msg-s-message-group__profile-link')
            if links:
                name = links[0].get_attribute('href')
            message = message.find_element_by_class_name('msg-s-event-listitem__message-bubble').find_element_by_tag_name('p').text
            print(name, message)


    def login(self):
        self.driver.get('https://www.linkedin.com')
        if os.path.isfile('credentials.json'):
            with open('credentials.json', 'r') as f:
                credentials = json.load(f)
        try:
            email = self.driver.find_element_by_id('login-email')
            password = self.driver.find_element_by_id('login-password')
            email.send_keys(credentials['email'])
            password.send_keys(credentials['password'])
            self.driver.find_element_by_id('login-submit').click()
        except NoSuchElementException:
            print('Already logged !')
            pass

    def run(self):
        self.login()
        self.go_to_messaging()
        self.get_nth_conversation(0)


if __name__ == '__main__':
    LinkedinMessengerBot().run()
