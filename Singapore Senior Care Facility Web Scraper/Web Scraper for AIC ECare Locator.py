import requests 

from bs4 import BeautifulSoup
import urllib
import re
import time
import pandas as pd
import os
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

# Define target website
home_page = "https://www.aic.sg/care-services/e-care-locator-advance"

# Use urllib to open home page, and BeautifulSoup to parse HTML
home_page_content = urllib.request.urlopen(home_page)
home_page_html = BeautifulSoup(home_page_content, 'html.parser')
home_page_html

### WebDriver initiation
# Set wait times
waittime = 20
sleeptime = 2

# Initiate web driver
try:
    # Close any existing WebDrivers
    driver.close() 
except Exception:
    pass

# Set webdriver options
options = webdriver.ChromeOptions()
options.add_argument('--no-sandbox')
options.add_argument('ignore-certificate-errors')

# Initiate WebDriver
driver = webdriver.Chrome(options=options)

# Direct WebDriver to the target home page
driver.get(home_page)

# Click on Day Centres which is under the "#category2" element
day_centre = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '[data-target="#category-2"]')))
day_centre.click()
driver.implicitly_wait(10)

# Find the 'Select All' label containing the 'group2' word to select all day centres
select_all_label = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#category-2 .text-checkbox.select-all")))

# Check if the word 'group2' is present in the 'onclick' attribute of the 'input' element within the 'Select All' label
if "group2" in select_all_label.get_attribute('innerHTML'):
    # Find the input element inside the label
    select_all_checkbox = select_all_label.find_element(By.CSS_SELECTOR, "input[type='checkbox']")
    print(f'Found the element containing "group2": {select_all_checkbox}')
else:
    print('Element containing "group2" not found.')

select_all_label.click()

# Find the 'Search' button with the specified attributes
search_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#nextBtn.btn.btn-asearch.btn.btn-orange.btn-custom')))

# Click the 'Search' button
search_button.click()

# Sleep a short while for page loading to be fully completed
time.sleep(sleeptime)

# Click to open every search result
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '[data-target="#result-0"]'))).click()
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '[data-target="#result-1"]'))).click()
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '[data-target="#result-2"]'))).click()
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '[data-target="#result-3"]'))).click()
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '[data-target="#result-4"]'))).click()
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '[data-target="#result-5"]'))).click()
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '[data-target="#result-6"]'))).click()
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '[data-target="#result-7"]'))).click()

WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '[data-target="#result-8"]'))).click()
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '[data-target="#result-9"]'))).click()
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '[data-target="#result-10"]'))).click()
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '[data-target="#result-11"]'))).click()
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '[data-target="#result-12"]'))).click()
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '[data-target="#result-13"]'))).click()
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '[data-target="#result-14"]'))).click()
driver.implicitly_wait(10)


# Get the HTML content of the search results page
search_results_html = driver.page_source

# Save the HTML content to a file
with open("search_results.html", "w", encoding="utf-8") as file:
    file.write(search_results_html)

print("Search results HTML saved to 'search_results.html'.")

# Get list of institutions on current page

hc_name = driver.find_elements(By.XPATH, "//p[@class='title mb-3']")
hc_name_list = []   
for i in hc_name:
      hc_name_list.append(i.text)
      print(hc_name_list)

# Get list of healthcare institutions' addresses on current page

hc_address = driver.find_elements(By.XPATH, "//p[@class='desprition']")
hc_address_list = []   
for i in hc_address:
      hc_address_list.append(i.text)
      print(hc_address_list)

postal_list = [item[-8:] for item in hc_address_list] # change -6 to -8 if want to retain 0 in postal codes starting with 0

## (1) Setup master list CSV to store first page records

# Set file name (based on your own preference)
file_name = 'aic_daycare.csv'

# Check if file already exists
if os.path.isfile(f'./{file_name}'):
    print(f'Filename {file_name} already exists')
else:
    # Set names of fields we want to extract
    column_names = ['Name','Address', 'postalCode']

    print('Created new master list file')

# Generate template dataframe
dict = {'Name': hc_name_list, 'Address': hc_address_list, 'postalCode': postal_list}  
df_template = pd.DataFrame(dict)

# Generate csv file from the dataframe template
df_template.to_csv(f'{file_name}', mode='a', header=False)

# Display time concluded
print(time.strftime("%H:%M:%S", time.localtime()))


##############################
### SCRAPE COMMUNITY HOSPITALS

# Initiate web driver
try:
    # Close any existing WebDrivers
    driver.close() 
except Exception:
    pass

# Set webdriver options
options = webdriver.ChromeOptions()
options.add_argument('--no-sandbox')
options.add_argument('ignore-certificate-errors')

# Initiate WebDriver
driver = webdriver.Chrome(options=options)

# Direct WebDriver to the target home page
driver.get(home_page)

# Click on stay-facilities which is under the "#category5" element. Change category5 to whatever medical facility you need, by looking at the html
day_centre = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '[data-target="#category-5"]')))
day_centre.click()
driver.implicitly_wait(10)

# click on comm hosps yourself 

# Find the 'Search' button with the specified attributes
search_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#nextBtn.btn.btn-asearch.btn.btn-orange.btn-custom')))

# Click the 'Search' button
search_button.click()

# Sleep a short while for page loading to be fully completed
time.sleep(sleeptime)


# Get the HTML content of the search results page
search_results_html = driver.page_source

# Save the HTML content to a file
with open("search_results.html", "w", encoding="utf-8") as file:
    file.write(search_results_html)

print("Search results HTML saved to 'search_results.html'.")


# Click to open every search result
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '[data-target="#result-0"]'))).click()
driver.implicitly_wait(10)

# Get list of institutions on current page

hc_name = driver.find_elements(By.XPATH, "//p[@class='title mb-3']")
hc_name_list = []   
for i in hc_name:
      hc_name_list.append(i.text)
      print(hc_name_list)

# Get list of healthcare institutions' addresses on current page

hc_address = driver.find_elements(By.XPATH, "//p[@class='desprition']")
hc_address_list = []   
for i in hc_address:
      hc_address_list.append(i.text)
      print(hc_address_list)

postal_list = [item[-6:] for item in hc_address_list] # change -6 to -8 if want to retain 0 in postal codes starting with 0

## (1) Setup master list CSV to store first page records

# Set file name (based on your own preference)
file_name = 'communityhosps.csv'

# Check if file already exists
if os.path.isfile(f'./{file_name}'):
    print(f'Filename {file_name} already exists')
else:
    # Set names of fields we want to extract
    column_names = ['Name','Address', 'postalCode']

    print('Created new master list file')

# Generate template dataframe
dict = {'Name': hc_name_list, 'Address': hc_address_list, 'postalCode': postal_list}  
df_template = pd.DataFrame(dict)

# Generate csv file from the dataframe template
df_template.to_csv(f'{file_name}', mode='a', header=False)

# Display time concluded
print(time.strftime("%H:%M:%S", time.localtime()))
