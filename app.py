from accept import accept_cookies
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
chrome_options = webdriver.ChromeOptions()
import time
import os
from sendmail import send_email

from dotenv import load_dotenv
load_dotenv()
PASSWORD = os.getenv("PASSWORD")
EMAIL = os.getenv("EMAIL")
COOKIE_ELEMENT = ""


driver = webdriver.Chrome(options=chrome_options)
driver.get("https://www.jobruf.de/secure/login")
explicit_wait = WebDriverWait(driver, 5)

email_input = driver.find_element(By.ID, "username")
password_input = driver.find_element(By.ID, "password")

email_input.send_keys(EMAIL)
password_input.send_keys(PASSWORD)

login_button = driver.find_element(By.ID, "_submit")
login_button.click()
time.sleep(5)
print("Logged in successfully ✅")
COOKIE_ELEMENT = "button[data-cookiefirst-action='accept']"
accept_cookies(driver, COOKIE_ELEMENT)
processed_jobs = set()

while True:
    try:
        # Re-find job cards every time the page reloads
        wait = WebDriverWait(driver, 10)
        cards = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "job-card")))
        
        # Find the first card we haven't processed yet
        target_card = None 
        for card in cards:
            job_url = card.get_attribute("href")
            if job_url not in processed_jobs:
                target_card = card
                processed_jobs.add(job_url)
                break
        
        if not target_card:
            print("No more new jobs found. ✅")
            break

        print(f"Processing job: {job_url}")
        time.sleep(1) # Small buffer for scroll
        target_card.click()

        # Check for the simple "Bewerben" button
        try:
            apply_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.LINK_TEXT, "Bewerben"))
            )
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", apply_button)
            apply_button.click()
            print("Clicked apply button ✅")
            time.sleep(2) # Wait for potential page changes
            
            # Check if we are on a complex application page (Bewerbung abschicken appears)
            # or if we were redirected back to the job list.
            try:
                # Use a shorter wait to check for the complex application button
                button = driver.find_element(By.CSS_SELECTOR, '[data-component="letter-submit-element"]')
                print("Complex application detected (Bewerbung abschicken found). Skipping... ⏭️")
                send_email("Complex application detected", f"A complex application page was detected for job: {job_url}. Please review it manually.", EMAIL)
                driver.back() # Go back to the list

            except:
                # If "Bewerbung abschicken" doesn't appear, wait for redirect back to job list
                print("One-click apply successful or redirecting... ⏳")
            
            # Wait for the page to reload and take us back to the list
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, "job-card")))
            print("Returned to job list ✅")
            
        except Exception:
            print("Simple apply button not found or extra steps required. Skipping... ⏭️")
            driver.back() # Go back to the list if we hit a complex page
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, "job-card")))

    except Exception as e:
        print(f"An error occurred in the loop: {e}")
        break
print(processed_jobs)
time.sleep(5)
driver.quit()