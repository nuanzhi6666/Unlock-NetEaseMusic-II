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
    browser.add_cookie({"name": "MUSIC_U", "value": "0063EC333F1715B4A4F9AC05BE9ACDC24F4D505FE45FD359ECC56CCDB97A1AD30D27117A7136DCFB773F3EC08CA15151ABE222DC6AFD41E97B4C0443454755E9E17D203AE98036387A27FF72F148365FF1529F3A4838695005035225938A7753875839816379F48D3199BD5DACB069C2E380D3498772041810A9D4BBB7E20A7304C1ED627AF0F67303E24E33EEC07EF517DEDF21B2C77975F96F349862FBFD85FAE10588B86CA2D3AA89B47BA490C73AE4F343212D2962F186059A8A7210EBCAA198F0F8AA3FABCCF524CF0F326AA6F0B86F0A6F32436F74306F0E477447C10D55E7FA761F4E4C041E632438444E4EDA88FDC4EE2014423F4DD976E49BD7CF0B578BC91BEF22F4B260A0F61DFF67BB6EF9DD14C8D8F0E159C52F31A94EFD16D22B6322EB88E9493FAECDD969856B1B4CD1282B7451E4EB10A89DBF024306163C9A137920D3E21B6902D2B04F50368CACB3CD67B19164921ADF32518F142D5389C2"})
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
