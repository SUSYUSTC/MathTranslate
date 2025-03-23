import os
import socket
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import threading
import subprocess
import tempfile
import ctypes
import time
import socket
GUI = False


def find_free_port():
    """Finds an available port dynamically."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("", 0))  # Bind to any free port
        return s.getsockname()[1]  # Get assigned port number


libc = ctypes.CDLL("libc.so.6")


def set_pdeathsig():
    """Ensures the subprocess is killed if the parent process exits."""
    import signal
    libc.prctl(1, signal.SIGTERM)


class Translator:
    def __init__(self, target_lang, source_lang, port, tmpdir):
        """Initialize the Chrome WebDriver once."""

        os.environ["HOME"] = f"{tmpdir}_home"
        os.environ["XDG_DATA_HOME"] = f"{tmpdir}_home/.local/share"
        os.environ["XDG_CONFIG_HOME"] = f"{tmpdir}_home/.config"
        os.environ["XDG_CACHE_HOME"] = f"{tmpdir}_home/.cache"
        os.environ["FONTCONFIG_PATH"] = "/etc/fonts"
        os.environ["FONTCONFIG_FILE"] = "/etc/fonts/fonts.conf"
        os.makedirs(os.environ["XDG_DATA_HOME"], exist_ok=True)
        os.makedirs(os.environ["XDG_CONFIG_HOME"], exist_ok=True)
        os.makedirs(os.environ["XDG_CACHE_HOME"], exist_ok=True)

        # Step 1: Start a hidden virtual display (Xvfb)
        if not GUI:
            self.xvfb_process = subprocess.Popen(["Xvfb", f":{port}", "-screen", "0", "1920x1080x24"], preexec_fn=set_pdeathsig, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            time.sleep(2)  # Wait for Xvfb to start

        # Step 2: Start Chrome in the hidden display
        opts = dict() if GUI else dict(env={**os.environ, "DISPLAY": f":{port}"}, preexec_fn=set_pdeathsig)
        self.chrome_process = subprocess.Popen([
            "/usr/bin/google-chrome",
            f"--remote-debugging-port={port}",  # Allow Selenium to attach
            f"--user-data-dir={tmpdir}_user",  # Persistent user session
            "--start-maximized",
            #"--headless=new",  # changes the output
            #"--no-sandbox",
            "--no-first-run",
            "--disable-dev-shm-usage",
            "--disable-gpu",
            "--disable-software-rasterizer",
            "--disable-features=UseOzonePlatform"  # Fix Wayland-related issues
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, **opts)

        time.sleep(3)  # Wait for Chrome to start

        options = webdriver.ChromeOptions()
        options.debugger_address = f"127.0.0.1:{port}"
        #options.add_argument("--headless=new")
        #options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=options)
        self.target_lang, self.source_lang = target_lang, source_lang
        self.url = f"https://translate.google.com/?sl={self.source_lang}&tl={self.target_lang}&op=translate"
        self.input_box_xpath = '//textarea[@aria-label="Source text"]'
        self.output_box_xpath = '//span[@class="HwtZe"]'
        print(self.url)

    def translate(self, text):
        """Translate text using Google Translate."""

        self.driver.get(self.url)
        self.input_box = WebDriverWait(self.driver, 10, poll_frequency=0.05).until(
            EC.presence_of_element_located((By.XPATH, self.input_box_xpath))
        )
        self.input_box.clear()
        self.driver.execute_script("arguments[0].value = arguments[1];", self.input_box, text)
        self.input_box.send_keys(' ')

        def updated(driver):
            try:
                result = driver.find_element(By.XPATH, self.output_box_xpath)
                return result.text.strip() != ''
            except TimeoutException as e:
                raise e
            except Exception as e:
                return False

        WebDriverWait(self.driver, 10, poll_frequency=0.05).until(updated)

        translated_text = self.driver.find_element(By.XPATH, self.output_box_xpath).text
        #self.last_output = translated_text
        return translated_text

    def close(self):
        """Close the browser."""
        self.driver.quit()


class ParallelTranslator:
    def __init__(self, target_lang, source_lang):
        self.target_lang = target_lang
        self.source_lang = source_lang
        self.drivers = {}
        self.tempdir = tempfile.TemporaryDirectory().name

    def translate(self, text):
        thread_id = threading.get_ident()
        if thread_id not in self.drivers:
            port = find_free_port()
            print('init', port)
            self.drivers[thread_id] = Translator(self.target_lang, self.source_lang, port, f'{self.tempdir}_{port}')
            print('init', port, 'done')
        while True:
            try:
                return self.drivers[thread_id].translate(text)
            except Exception as e:
                import time
                time.sleep(15)
                port = find_free_port()
                print('init', port)
                self.drivers[thread_id] = Translator(self.target_lang, self.source_lang, port, f'{self.tempdir}_{port}')
                print('init', port, 'done')
                continue
