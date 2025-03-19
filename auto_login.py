# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "00CAD26AD95AB2D1257599B24CE447DB9BACD3F86568E89BAA8D19E356D83002AA41272FB4C81D37C4917D0B645D22BCF62C292C64584BA95FBEF7C4B5B45929668E9199256A49A4D6FF84B5F36D289535F4C4360760937129CF2C0EB1187D5035659EA60B2F1B87671767954AEBB8ACBF2A50DA719917843F33590FB113EDBDE327E9AC37F20F89F714FDEABE4FDBA004A019CEEBF2DD184891A29DF14359486476065379908A2254F3A679BA5C6FDBF75256F2B254B587FCEB2C3921FBDD0BE76B757F5F06EE718755D7E4528C997A0E7EDE1BF520F41C2E8B6E857CB7849C61DAC44AE74BECE7D2944BC723C223603A98699A843DD6C75B9A25910CB130B6AD764C88BD421A47758F19204F810AEEDD1518EFEB1D7B1CAAD9AB39D0C7A02AD7DA7B35EAE012B63A875E45C5657745BA2EFF900DAE824321114B537752ECB632EA40B092D2B0C3AA638A589252209D949156014FA1F3C8E0961FFEAC304F20B1"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
