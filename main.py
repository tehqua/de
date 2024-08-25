from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from time import sleep
import random
import csv

# Path to msedgedriver.exe
service = Service("C:\\Users\\PC\\Downloads\\DE\\msedgedriver.exe")

# Set up headless option if needed
options = Options()
# options.headless = True  # Uncomment to run in headless mode

# Create Edge with Service
driver = webdriver.Edge(service=service, options=options)

# Open CSV file for writing
with open('real_estate_data.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Type', 'Price', 'Area', 'Place'])

    def login(username, password):
        driver.get('https://batdongsan.com.vn/dang-nhap')
        sleep(random.randint(5, 10))
        username_field = driver.find_element(By.NAME, '0943123827')  # Update as necessary
        password_field = driver.find_element(By.NAME, 'Bin041104')  # Update as necessary
        username_field.send_keys(username)
        password_field.send_keys(password)
        password_field.submit()
        sleep(random.randint(5, 10))

    def url_chungcu():
        driver.get('https://batdongsan.com.vn/ban-can-ho-chung-cu-ha-noi') 
        sleep(random.randint(5, 15))

    def url_nhadat():
        driver.get('https://batdongsan.com.vn/ban-nha-dat-ha-noi') 
        sleep(random.randint(5, 15))

    def get_data(property_type):
        try:
            prices = driver.find_elements(By.CSS_SELECTOR, ".re__card-config-price.js__card-config-item")
            areas = driver.find_elements(By.CSS_SELECTOR, ".re__card-config-area.js__card-config-item")
            places = driver.find_elements(By.CSS_SELECTOR, ".re__card-config-dot + span")

            if not prices or not areas or not places:
                print(f"No data found for {property_type}")
                return

            for price, area, place in zip(prices, areas, places):
                writer.writerow([property_type, price.text, area.text, place.text])
        except Exception as e:
            print(f"Error occurred while fetching data: {e}")

    # Log in
    login('your_username', 'your_password')  # Replace with your credentials

    # Crawl data for apartment prices
    url_nhadat()
    get_data('Nhà đất')

    # Crawl data for house prices
    url_chungcu()
    get_data('Chung cư')

# Close the browser after scraping
driver.quit()
