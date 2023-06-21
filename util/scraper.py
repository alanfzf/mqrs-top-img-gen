import requests
from io import BytesIO
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.edge.options import Options
from util import format


class ImageSearcher:
    def __init__(self, user):
        self.user = user
        self.not_found = (
            "This account doesn’t exist", 
            "Hmm...this page doesn’t exist. Try searching for something else."
        )

    def __call__(self, driver):
        # search for user not found
        span_elements = driver.find_elements(By.TAG_NAME, 'span')
        for span in span_elements:
            if span.text in self.not_found:
                return self.user

        # search for the user profile pic
        image_tags = driver.find_elements(By.TAG_NAME, 'img')
        for tag in image_tags:
            src = tag.get_attribute('src')
            if format.valid_url(src):
                return src
        return None

def download_image(url):
    img_bytes = None
    try:
        resp = requests.get(url)
        img_bytes = BytesIO(resp.content)
    except Exception as e:
        raise e
    return img_bytes

def download_user_images(user_names):
    opts = Options()
    opts.add_argument("--headless")  
    opts.add_argument("--disable-extensions")  

    driver = webdriver.Edge(options=opts)
    images = {}
    invalid = []

    for user in user_names:
        driver.get(f'https://twitter.com/{user}/photo')
        data_wait = WebDriverWait(driver, 5)
        image_url = data_wait.until(ImageSearcher(user))
        if not format.valid_url(image_url):
            invalid.append(image_url)
            continue
        bytes = download_image(image_url)
        images[user] = bytes

    driver.quit()

    if len(invalid) > 0:
        bad = ', '.join(invalid)
        raise Exception(f"Users not found: {bad}")

    return images
