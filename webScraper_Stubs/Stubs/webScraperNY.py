from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import Select
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC

# Set up Selenium WebDriver for MS Edge
edge_driver_path = "C:/Users/avirat.sharma/Downloads/msedgedriver.exe"  # Update this path to your msedgedriver
service = Service(executable_path=edge_driver_path)
driver = webdriver.Edge(service=service)

# Step 1: Load the website
url = "https://apps.dos.ny.gov/publicInquiry/"  # Replace with the URL you want to scrape
driver.get(url)

# Optional: Wait for dynamic content to load (you can adjust the time as needed)
time.sleep(5)  # Wait for 5 seconds for page to load, or use WebDriverWait for more control



# Locate the search input box
search_box = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, ".form-control.col-8"))
)

dropdown = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "nameType"))  # Adjust the ID as needed
)

# Create a Select object for the dropdown
select = Select(dropdown)

# Select an option by visible text
select.select_by_visible_text("Active")

# Enter the company name you want to search for
company_name = "ION Trading"
search_box.send_keys(company_name)

# Locate all checkboxes
checkboxes = driver.find_elements(By.CLASS_NAME, "mb-0")  # Adjust to your checkbox class

for checkbox in checkboxes:
    if not checkbox.is_selected():
        checkbox.click()  # Select the checkbox if it's not selected
        print("Checkbox selected.")
    else:
        print("Checkbox already selected.")



# Locate the search button and click it
search_button = driver.find_element(By.CLASS_NAME, "btn btn-primary float-right")
search_button.click()

# Wait until the table is visible (replace 'table-class' with the actual class or tag)

# try:
#     WebDriverWait(driver, 10).until(
#     EC.presence_of_element_located((By.ID, "tblResults"))  # Replace with the actual class of the table
# )
#     print("Table loaded successfully.")
# except TimeoutException:
#     print("Timed out waiting for the table to load.")

table = driver.find_element(By.XPATH, "//table[1]")

# Get the page source after the table has loaded
page_source = driver.page_source
soup = BeautifulSoup(page_source, 'html.parser')

# Use BeautifulSoup to find all tables
tables = soup.find_all('table')

# Loop through the tables and extract data from the one you're interested in
for table in tables:
    rows = table.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        cols = [col.text.strip() for col in cols]
        print(cols)

