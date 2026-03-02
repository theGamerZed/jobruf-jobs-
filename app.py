from accept import accept_cookies
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
chrome_options = webdriver.ChromeOptions()
import time
import os
from dotenv import load_dotenv
load_dotenv()
password = os.getenv("PASSWORD")
email = os.getenv("EMAIL")
driver = webdriver.Chrome(options=chrome_options)
driver.get("https://www.jobruf.de/secure/login")
explicit_wait = WebDriverWait(driver, 5)

email_input = driver.find_element(By.ID, "username")
password_input = driver.find_element(By.ID, "password")

email_input.send_keys(email)
password_input.send_keys(password)

login_button = driver.find_element(By.ID, "_submit")
login_button.click()
time.sleep(5)
cookie_element = "button[data-cookiefirst-action='accept']"
print(cookie_element)
accept_cookies(driver, cookie_element)
# link = explicit_wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[href="/student/jobs/list"]')))
# link = driver.find_element(By.XPATH, "//span[text()='Bewerbungen']")
cards = driver.find_elements(By.CSS_SELECTOR, "a.job-card")
# print(cards)
for card in cards:
    card.click()
    apply_button = driver.find_element(By.LINK_TEXT, "Bewerben")
    apply_button.click()
    print(apply_button)
time.sleep(5)
driver.quit()