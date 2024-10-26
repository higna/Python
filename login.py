from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import os
import time

# Path to Chrome driver executable
chrome_driver_path = './chromedriver.exe'

# Setup Chrome options
chrome_options = Options()
# chrome_options.add_argument("--headless")  # Uncomment to run in headless mode

# Initialize WebDriver
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

# Login Function
def login(username, password):
    try:
        # Navigate to login page
        driver.get('https://data.seedtracker.org/login')
        print("Navigated to login page")
        
        # Find and fill in username and password fields
        username_field = driver.find_element(By.NAME, 'username')
        password_field = driver.find_element(By.NAME, 'password')
        username_field.send_keys(username)
        password_field.send_keys(password)
        password_field.send_keys(Keys.RETURN)
        
        # Wait for successful login indication
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, 'home-link'))
        )
        print("Login successful")
    except TimeoutException:
        print("Login timed out")
    except NoSuchElementException as e:
        print(f"Element not found: {e}")
    except Exception as e:
        print(f"An error occurred during login: {e}")
    finally:
        driver.quit()  # Ensure the driver is closed after operations

# Use environment variables for credentials
username = os.getenv("SEEDTRACKER_USERNAME", "your_username")
password = os.getenv("SEEDTRACKER_PASSWORD", "your_password")

# Call the login function
login(username, password)
