import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd

def uKScraper(entity_name):
    # Set up Selenium WebDriver for MS Edge
    edge_driver_path = "C:/Users/avirat.sharma/Downloads/msedgedriver.exe"  # Update this path to your msedgedriver
    service = Service(executable_path=edge_driver_path)
    driver = webdriver.Edge(service=service)

    # Load the website
    url = "https://find-and-update.company-information.service.gov.uk/"
    driver.get(url)

    # Wait for the page to load
    time.sleep(5)  # You may adjust the sleep time as needed

    # Locate the search input box and enter the company name
    search_box = driver.find_element(By.ID, "site-search-text")
    search_box.send_keys(entity_name)

    # Locate the search button and click it
    search_button = driver.find_element(By.ID, "search-submit")
    search_button.click()

    # Wait until the results are visible
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "grid-row"))
        )
        print("Table loaded successfully.")
    except TimeoutException:
        print("Timed out waiting for the table to load.")
        driver.quit()
        return None

    # Get the page source after the table has loaded
    html = driver.page_source

    # Use BeautifulSoup to parse the HTML
    soup = BeautifulSoup(html, 'html.parser')

    # Find all the list items for companies
    company_items = soup.find_all('li', class_='type-company')

    # Initialize a list to store the structured data
    company_data = []

    # Loop through each company item and extract relevant data
    for company_item in company_items:
        # Extract the company name (from <a> inside <h3>)
        company_name = company_item.find('a', class_='govuk-link').text.strip()
        
        # Extract the company number and status (from <p> with class 'meta crumbtrail')
        meta_info = company_item.find_all('p', class_='meta crumbtrail')
        company_info = meta_info[0].text.strip()  # First <p> with company number & status
        
        # Extract the company address (from the <p> tag after the meta info)
        address = company_item.find_all('p')[-1].text.strip()  # Last <p> is the address
        
        # Extract matching previous names if present
        previous_names = None
        if len(meta_info) > 1:
            previous_names = meta_info[1].find('span').text.strip()
        
        # Extract the registration number and the status (from company_info)
        company_number, status = company_info.split(' - ', 1)  # Split by ' - '

        # Store the extracted data in a dictionary
        company_data.append({
            'Company Name': company_name,
            'Company Number': company_number,
            'Status': status,
            'Address': address,
            'Previous Names': previous_names
        })

    # Close the driver after scraping
    driver.quit()

    # Convert the structured data into a pandas DataFrame for tabular form
    if company_data:
        df = pd.DataFrame(company_data)
        return df
    else:
        return "No results found."

# Example function call:
entity_name = "ION Trading"
company_info_df = uKScraper(entity_name)

# Print the DataFrame
print(company_info_df)
