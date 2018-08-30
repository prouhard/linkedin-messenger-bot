from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options

from copy import deepcopy

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
        time.sleep(5)

    def wait_for_new_conversation(self):
        cached_top_conversation = self.get_nth_conversation(0)
        while True:
            current_top_conversation = self.get_nth_conversation(0)
            print(current_top_conversation)
            if cached_top_conversation != current_top_conversation:
                print('New message !')
                yield current_top_conversation

    def get_nth_conversation(self, n):
        conversation_list = self.driver.find_element_by_class_name(
            'msg-conversations-container__conversations-list'
        )
        conversations = conversation_list.find_elements_by_tag_name('li')
        if len(conversations) <= n:
            raise IndexError('This conversation does not exist.')
        return conversations[n]

    def get_nth_conversations_messages(self, n):
        time.sleep(5)
        self.get_nth_conversation(n).click()
        first_conversation = self.driver.find_element_by_class_name('msg-s-message-list')
        messages = first_conversation.find_elements_by_tag_name('li')[1:]
        for message in messages:
            links = message.find_elements_by_class_name('msg-s-message-group__profile-link')
            if links:
                name = links[0].get_attribute('href')
            message = message.find_element_by_class_name(
                'msg-s-event-listitem__message-bubble'
            ).find_element_by_tag_name('p').text
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
        for i in self.wait_for_new_conversation():
            print(i)


if __name__ == '__main__':
    LinkedinMessengerBot().run()
