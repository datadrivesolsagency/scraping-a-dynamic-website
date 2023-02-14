from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

#Reading data from comma separated file

codes_file = pd.read_csv('austailian_postcodes_dataset.csv')

#An empty list so that data rendered from the html can be appended
dataset = []

"""This function is initializing the chrome driver and fetching the url in the browser"""

def driver_getting_function(postcodes):
    options = ChromeOptions()
    options.headless = True
    url = f'https://www.corelogic.com.au/our-data/recent-sales?postcode={postcodes}'
    print(url)
    global driver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options= options)
    driver.get(url)
    return driver


"""This function is to scrape the every row of the table line by line in and then by every cell
so that the table can be easily converted into a dataframe format that will help in created
a csv file"""


def scraping_function(object):
    try:
        for x in range(1,5,1):
            print('Iteration number:', f'{x}')
            element1 = driver.find_element(By.XPATH, f'.//tr[{x}]/td[1]')
            address = [element1.text]

            element2 = driver.find_element(By.XPATH, f'.//tr[{x}]/td[2]')
            property_type = [element2.text]

            element3 = driver.find_element(By.XPATH, f'.//tr[{x}]/td[3]')
            sold_by = [element3.text]

            element4 = driver.find_element(By.XPATH, f'.//tr[{x}]/td[4]')
            bed = [element4.text]

            element5 = driver.find_element(By.XPATH, f'.//tr[{x}]/td[5]')
            bath = [element5.text]

            element6 = driver.find_element(By.XPATH, f'.//tr[{x}]/td[6]')
            car = [element6.text]

            element7 = driver.find_element(By.XPATH, f'.//tr[{x}]/td[7]')
            sale_price = [element7.text]

            element8 = driver.find_element(By.XPATH, f'.//tr[{x}]/td[8]')
            sale_date = [element8.text]

            data = address + property_type + sold_by + bed + bath + car + sale_price + sale_date
            dataset.append(data)
            print(dataset)
        
    except:
        []

#looping all over the unique postcodes of the dataset

for i in range(2,4,1):
    try:
        c = driver_getting_function(codes_file.postcode.unique()[i])
        scraping_function(c)
    except:
        ''

#Converting the list into dataframe

df = pd.DataFrame(dataset)
df.columns = ['Address','Property Type', 'Sold by', ' Bed', 'Bath','Car', 'Sale Price', 'Sale Date']
df.to_csv('test_file.csv')
print(df)
