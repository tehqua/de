import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from time import sleep
import random
import csv

driver = uc.Chrome()

with open('real_estate_data.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Type', 'Price', 'Area', 'Place', 'Link'])

    def handle_cloudflare():
        try:
            checkbox = driver.find_element(By.ID, "challenge-form")
            if checkbox:
                checkbox.click()
                sleep(random.randint(2, 5))  
        except NoSuchElementException:
            pass

    def get_data(property_type):
        places = driver.find_elements(By.CSS_SELECTOR, ".re__card-location span:last-child")  
        prices = driver.find_elements(By.CSS_SELECTOR, ".re__card-config-price.js__card-config-item")
        areas = driver.find_elements(By.CSS_SELECTOR, ".re__card-config-area.js__card-config-item")
        links = driver.find_elements(By.CSS_SELECTOR, "a.js__product-link-for-product-id")

        if not prices or not areas or not places or not links:
            print(f"No data found for {property_type}")
            return

        for price, area, place, link in zip(prices, areas, places, links):
            try:
                parent_element = link.find_element(By.XPATH, "./ancestor::div[contains(@class, 're__listing-verified-similar-v2')]")
                if parent_element:
                    continue  
            except NoSuchElementException:
                pass  

            writer.writerow([property_type, price.text, area.text, place.text, link.get_attribute('href')])

    def crawl_pages(base_url, property_type, max_pages=100):
        for page in range(1, max_pages + 1):
            page_url = f'{base_url}/p{page}' if page > 1 else base_url
            driver.get(page_url)
            sleep(random.randint(5, 10))
            handle_cloudflare()

            get_data(property_type)

            print(f"Crawled page {page} for {property_type}")

    crawl_pages('https://batdongsan.com.vn/ban-nha-dat-ha-noi', 'Nhà đất', max_pages=2)

    crawl_pages('https://batdongsan.com.vn/ban-can-ho-chung-cu-ha-noi', 'Chung cư', max_pages=2)

# Đóng trình duyệt sau khi crawl
driver.quit()
