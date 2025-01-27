import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

def delScraper(entity_name):
    # Set up Selenium WebDriver for MS Edge
    edge_driver_path = "C:/Users/avirat.sharma/Downloads/msedgedriver.exe"  # Update this path to your msedgedriver
    service = Service(executable_path=edge_driver_path)
    driver = webdriver.Edge(service=service)

    # Load the website
    url = "https://icis.corp.delaware.gov/ecorp/entitysearch/namesearch.aspx"
    driver.get(url)

    # Wait for the page to load
    time.sleep(5)  # You may adjust the sleep time as needed

    # Locate the search input box and enter the company name
    search_box = driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_frmEntityName")
    search_box.send_keys(entity_name)

    # Locate the search button and click it
    search_button = driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_btnSubmit")
    search_button.click()

    # Wait until the results table is visible
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "tblResults"))  # Wait for the table to load
        )
        print("Table loaded successfully.")
    except TimeoutException:
        print("Timed out waiting for the table to load.")
        driver.quit()
        return None

    # Get the page source after the table has loaded
    page_source = driver.page_source

    # Parse the page with BeautifulSoup
    soup = BeautifulSoup(page_source, 'html.parser')

    # Find the table with the ID 'tblResults'
    table = soup.find('table', {'id': 'tblResults'})

    # Extract the rows from the table
    rows = table.find_all('tr')

    # Initialize a list to store the table data
    table_data = []

    # Loop through each row and extract the data
    for row in rows[1:]:  # Skip the header row
        cols = row.find_all('td')  # Find all columns in the row
        cols = [col.text.strip() for col in cols]  # Get the text and strip extra spaces
        table_data.append(cols)

    # Close the WebDriver after scraping
    driver.quit()

    # Convert the list of rows into a pandas DataFrame
    df = pd.DataFrame(table_data, columns=[ "File Number","Entity Name"])

    return df

# # Example function call:
# entity_name = "Runway"
# company_info_df = delScraper(entity_name)

# # Print the DataFrame
# print(company_info_df)
