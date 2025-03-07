from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Translator:
    def __init__(self):
        """Initialize the Chrome WebDriver once."""
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")  # Run in headless mode (no GUI)
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")

        # Initialize Chrome WebDriver
        self.driver = webdriver.Chrome(options=options)

    def translate(self, text, source_lang="en", target_lang="zh"):
        """Translate text using Google Translate."""
        url = f"https://translate.google.com/?sl={source_lang}&tl={target_lang}&op=translate"
        self.driver.get(url)

        # Find input text area and enter text
        input_box = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//textarea[@aria-label="Source text"]'))
        )
        input_box.clear()
        input_box.send_keys(text)

        # Wait for the translated text to appear dynamically
        output_box_xpath = '//span[@class="HwtZe"]'
        WebDriverWait(self.driver, 10).until(
            lambda driver: driver.find_element(By.XPATH, output_box_xpath).text.strip() != ""
        )

        # Extract the translated text
        translated_text = self.driver.find_element(By.XPATH, output_box_xpath).text
        return translated_text

    def close(self):
        """Close the browser."""
        self.driver.quit()

