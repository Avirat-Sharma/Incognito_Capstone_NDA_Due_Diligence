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
url = "https://icis.corp.delaware.gov/ecorp/entitysearch/namesearch.aspx"  # Replace with the URL you want to scrape
driver.get(url)

# Optional: Wait for dynamic content to load (you can adjust the time as needed)
time.sleep(5)  # Wait for 5 seconds for page to load, or use WebDriverWait for more control
# Locate the search input box
search_box = driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_frmEntityName")

# Enter the company name you want to search for
company_name = "Runway"
search_box.send_keys(company_name)

# Locate the search button and click it
search_button = driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_btnSubmit")
search_button.click()

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC

# Wait until the table is visible (replace 'table-class' with the actual class or tag)

try:
    WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "tblResults"))  # Replace with the actual class of the table
)
    print("Table loaded successfully.")
except TimeoutException:
    print("Timed out waiting for the table to load.")

# Get the page source after the table has loaded
page_source = driver.page_source

# Parse the page with BeautifulSoup
soup = BeautifulSoup(page_source, 'html.parser')

# Find the table (replace with the correct selector for the table)
table = soup.find('table', {'id': 'tblResults'})  # Adjust the class or other attributes accordingly

# Extract the rows of the table
rows = table.find_all('tr')

# Loop through each row and extract data
for row in rows:
    cols = row.find_all('td')  # Find all columns in the row
    cols = [col.text.strip() for col in cols]  # Get the text and strip extra spaces
    print(cols)  # You can store or process this data as needed

driver.quit()

