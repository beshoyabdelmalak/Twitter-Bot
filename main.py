from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from random import randint
import time
import configparser


class TwitterBot:
    def __init__(self, username, password):
        self.base_url = "https://twitter.com/"
        self.username = username
        self.password = password
        option = Options()
        option.add_extension("./goodTwitter.crx")
        self.bot = webdriver.Chrome(options=option)
        # so that the login form is shown
        self.bot.set_window_size(1024, 1024)

    def login(self):
        bot = self.bot
        bot.get(self.base_url)
        time.sleep(3)
        email = bot.find_element_by_name("session[username_or_email]")
        password = bot.find_element_by_name("session[password]")
        email.clear()
        password.clear()
        email.send_keys(self.username)
        password.send_keys(self.password)
        password.send_keys(Keys.ENTER)
        time.sleep(3)

    def like_retweet(self, hastag):
        bot = self.bot
        bot.get(self.base_url + "search?q=%23" + hastag + "&src=trend_click")
        time.sleep(2)
        # scorll the window to get more tweets
        for i in range(1, 2):
            bot.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)

        links = bot.find_elements_by_class_name("tweet")
        links = [link.get_attribute("data-permalink-path") for link in links]

        for link in links:
            # get a random action
            action = self.get_random_action()
            bot.get(self.base_url + link)
            if action == "like":
                like_button = bot.find_element_by_class_name("js-actionFavorite")
                like_button.click()
                time.sleep(3)
            elif action == "retweet":
                retweet_button = bot.find_element_by_class_name("js-actionRetweet")
                retweet_button.click()
                retweet_confirm_button = bot.find_element_by_class_name(
                    "retweet-action"
                )
                retweet_confirm_button.click()
                time.sleep(3)
            else:
                time.sleep(3)
                continue

    def get_random_action(self):
        actions = ["like", "retweet", "pass"]
        value = randint(0, 2)
        return actions[value]

    def close_browser(self):
        self.bot.quit()


if __name__ == "__main__":
    # set the email and password for a valid account in config.ini
    config = configparser.ConfigParser()
    config.read("config.ini")
    twitter_bot = TwitterBot(
        config["TWITTER-ACCOUNT"]["email"], config["TWITTER-ACCOUNT"]["password"]
    )
    twitter_bot.login()
    # search for any hashtag you like
    twitter_bot.like_tweet("webdeveloper")
    twitter_bot.close_browser()
