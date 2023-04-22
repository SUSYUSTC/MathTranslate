import time
from splinter import Browser
from selenium.common.exceptions import WebDriverException
username = 'xxx'
password = 'xxx'
zip_file_path = 'xxx'


def is_browser_available(browser_name):
    try:
        with Browser(browser_name, headless=True):
            pass
        return True
    except WebDriverException:
        return False


def get_available_browsers():
    available_browsers = []
    for browser_name in ['chrome', 'firefox', 'edge']:
        if is_browser_available(browser_name):
            available_browsers.append(browser_name)

    return available_browsers


browser = Browser('chrome')
browser.visit("https://www.overleaf.com/login")
browser.find_by_id('email').fill(username)
browser.find_by_id('password').fill(password)
browser.find_by_text('Log in with your email').click()
browser.find_by_text('New Project').click()
browser.find_by_text('Upload Project').click()
file_input = browser.find_by_css('input[type="file"]').first
file_input._element.send_keys('/home/jiace/arxiv/2page/arxiv.zip')
time.sleep(3)
browser.find_by_text('Menu').click()
browser.find_by_name('compiler').click()
browser.find_by_text('XeLaTeX').click()
browser.reload()
