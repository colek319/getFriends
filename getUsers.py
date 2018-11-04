import pandas as pd
import time

from pyvirtualdisplay import Display

import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

import urllib

from bs4 import BeautifulSoup

import requests

class Scraper:
    def getFriends(self, username):
        url = "https://twitter.com/%s/following" % (username)
        self.browser.get(url)

        # we dont want to get our ip banned....
        self.browser.wait = WebDriverWait(self.browser, 5)

        self.scroll_to_end_page()

        source = self.browser.page_source

        # parse the html using beautiful soup and store in variable `soup`
        soup = BeautifulSoup(source, 'html.parser')

        #grabs div tag with user_ids
        friends_list = soup.find_all('div', {'class':'js-stream-item'})

        # Stores ids
        friend_ids = []
        for friend in friends_list:
            friend_ids.append(friend['data-item-id'])

        return friend_ids

    def scroll_to_end_page(self):
        SCROLL_PAUSE_TIME = 0.5


        while True:

            # Get scroll height
            ### This is the difference. Moving this *inside* the loop
            ### means that it checks if scrollTo is still scrolling 
            last_height = self.browser.execute_script("return document.body.scrollHeight")

            # Scroll down to bottom
            self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)

            # Calculate new scroll height and compare with last scroll height
            new_height = self.browser.execute_script("return document.body.scrollHeight")
            if new_height == last_height:

                # try again (can be removed)
                self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

                # Wait to load page
                time.sleep(SCROLL_PAUSE_TIME)

                # Calculate new scroll height and compare with last scroll height
                new_height = self.browser.execute_script("return document.body.scrollHeight")

                # check if the page height has remained the same
                if new_height == last_height:
                    # if so, you are done
                    break
                # if not, move on to the next loop
                else:
                    last_height = new_height
                    continue

        


    ##############INIT FUNCTIONS ###################

    def end_scraper(self):
        self.browser.close()
        #self.display.stop()

    def start_scraper(self):
        s_options = webdriver.ChromeOptions()
        s_options.add_argument('--ignore-certificate-errors')
        s_options.add_argument("--test-type")
        s_options.binary_location = "/usr/bin/chromium"
        self.browser = webdriver.Chrome(options = s_options)
        self.browser.wait = WebDriverWait(self.browser, 5)

    # sign in to your twitter account
    def sign_in(self, username, password):
        
        # open the web page in the browser:
        self.browser.get("https://twitter.com/login")
 
        # find the boxes for username and password
        username_field = self.browser.find_element_by_class_name("js-username-field")
        password_field = self.browser.find_element_by_class_name("js-password-field")
 
        # enter your username:
        username_field.send_keys(username)
        self.browser.implicitly_wait(1)
 
        # enter your password:
        password_field.send_keys(password)
        self.browser.implicitly_wait(1)
 
        # click the "Log In" button:
        self.browser.find_element_by_class_name("EdgeButtom--medium").click()

    def __init__(self, username, password):
        #self.display = Display( size=(800, 600))
        #self.display.start()
        self.start_scraper()
        self.sign_in(username, password)
