from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from bs4 import BeautifulSoup 
import time

# Set up Selenium WebDriver for MS Edge
edge_driver_path = "C:/Users/avirat.sharma/Downloads/msedgedriver.exe"  # Update this path to your msedgedriver
service = Service(executable_path=edge_driver_path)
driver = webdriver.Edge(service=service)

# Step 1: Load the website
url = "https://www.registroimprese.it/"  # Replace with the URL you want to scrape
driver.get(url)

# Optional: Wait for dynamic content to load (you can adjust the time as needed)
time.sleep(5)  # Wait for 5 seconds for page to load, or use WebDriverWait for more control
# Locate the search input box
deny_cookies = driver.find_element(By.ID, "didomi-notice-disagree-button")
deny_cookies.click()
search_box = driver.find_element(By.ID, "inputSearchFieldMob")

# Enter the company name you want to search for
company_name = "ION Trading"
search_box.send_keys(company_name)

# Locate the search button and click it
search_button = driver.find_element(By.ID, "btnCercaGratuitaMob")
search_button.click()


from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC

# Wait until the table is visible (replace 'table-class' with the actual class or tag)
# Get the page source after the table has loaded

time.sleep(10)
# try:
#     WebDriverWait(driver, 10).until(
#     EC.presence_of_element_located((By.CLASS_NAME, "span12.spanHaiCercato"))  # Replace with the actual class of the table
# )
#     print("Table loaded successfully.")
# except TimeoutException:
#     print("Timed out waiting for the table to load.")

page_source = driver.page_source

# Parse the page with BeautifulSoup
soup = BeautifulSoup(page_source, 'html.parser')
company_spans = soup.find_all('span', class_='visible-phone.visible-tablet.denomMobile')
info1 = soup.find_all('span', class_='span1.forma-giuridica-mobile')
info2= soup.find_all('span', class_='span4.attivita-mobile')

# Initialize a list to store the structured data
data = []

# Loop through the company names and registration numbers and pair them
for company, reg_num in zip(company_spans,info1,info2):
    row_data = {
        'company_name': company.text.strip(),
        'registration_number': reg_num.text.strip()
    }
    data.append(row_data)

# Print the structured data (a list of dictionaries)
print(data)


driver.quit()

