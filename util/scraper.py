import os
import time
import requests

from io import BytesIO
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import StaleElementReferenceException


from util import format
from util import dirs

class ImageSearcher:

    def __init__(self, user):
        self.user = user
        self.verify = "400x400."

    def __call__(self, driver):
        # search for the user profile pic
        image_tags = driver.find_elements(By.TAG_NAME, 'img')

        for tag in image_tags:
            src = tag.get_attribute('src')
            if format.valid_url(src) and self.verify in src:
                return src

class InputFieldSearcher():

    def __init__(self, field_name, field_value):
        self.field = field_name
        self.value = field_value

    def __call__(self, driver):
        input_fields = driver.find_elements(By.TAG_NAME, 'input')
        for input in input_fields:
            try:
                input.send_keys(self.value)
                return "done" 
            except Exception:
                pass

class ButtonSearcher:

    def __init__(self, button_name):
        self.button = button_name
        self.pattern = "//div[@role='button']"

    def __call__(self, driver):
        buttons = driver.find_elements(By.XPATH, self.pattern)
        button = next(iter([btn for btn in buttons if self.button == btn.text]), None)
        return button


def download_image(url):
    img_bytes = None
    try:
        resp = requests.get(url)
        img_bytes = BytesIO(resp.content)
    except Exception as e:
        raise e
    return img_bytes


def download_user_images(user_names):
    user, pswrd = os.getenv("TW_USER"), os.getenv("TW_PASSWORD")
    has_cookies = dirs.cookies_exist()
    opts = Options()
    # opts.add_argument("--headless")
    opts.add_argument("-inprivate")

    if not user or not pswrd:
        raise Exception("The envs for TW_USER and TW_PASSWORD have not been set!")


    driver = webdriver.Edge(options=opts)
    data_wait = WebDriverWait(driver, 10)

    # LOG INTO THE ACCOUNT
    # TODO: Check if the cookies are expired
    if not has_cookies:
        driver.get(f'https://twitter.com/i/flow/login')
        data_wait.until(InputFieldSearcher('text', user)) # can be null
        data_wait.until(ButtonSearcher('Next')).click() # can be null 
        data_wait.until(InputFieldSearcher('password', pswrd)) # can be null
        data_wait.until(ButtonSearcher('Log in')).click() # can be null
        time.sleep(5)
        dirs.save_cookies(driver.get_cookies())
    else:
        driver.get('https://twitter.com')
        cookies = dirs.load_cookies()
        for cookie in cookies:
            driver.add_cookie(cookie)

    accounts = {}
    count = 0
    for user in user_names:
        url = None
        subcount = 0
        
        """ 
        if count >= 45:
            # wait around 15 minutes
            print('Rate limit reached, waiting 15 minutes...!')
            time.sleep(60*15.5)
            count = 0 
        """
        while subcount < 6:
            try:
                driver.get(f'https://twitter.com/{user}/photo')
                url = data_wait.until(ImageSearcher(user))
                subcount = 7
            except StaleElementReferenceException as e: 
                subcount += 1
                print(f"[!!!] Reintentado... {e}")
            except Exception as e:
                url = None
                break;

        accounts[user] = url
        count += 1

    # close the driver
    driver.quit()

    invalid = ', '.join([name for name in accounts.keys() if accounts[name] is None])
    if len(invalid) > 0:
        raise Exception(f"Users not found: {invalid}")

    images = {acc: download_image(img) for acc, img in accounts.items()}

    return images
