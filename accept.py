import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def accept_cookies(driver, cookie_element):
        try:
            cookie_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, cookie_element)))
            cookie_button.click()
            print("Cookie clicked ✅")
            time.sleep(2)  # Wait for popup to close
        except Exception:
            print("No cookie popup found or error clicking it.")