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

    def get_property_type(link):
        # Extract the property type from the URL
        if "nha-biet-thu-lien-ke" in link:
            return "Nhà biệt thự liền kề"
        elif "can-ho-chung-cu" in link:
            return "Căn hộ chung cư"
        elif "ban-nha-rieng" in link:
            return "Nhà riêng"
        elif "nha-mat-pho" in link:
            return "Nhà mặt phố"
        elif "shophouse" in link:
            return "Shophouse"
        elif "ban-dat" in link: 
            return "Đất bán"
        elif "ban-trang-trai-khu-nghi-duong" in link: 
            return "Trang trại khu nghỉ dưỡng"
        elif "ban-condotel" in link: 
            return "Condotel"
        elif "ban-kho-nha-xuong" in link: 
            return "Nhà kho nhà xưởng"
        elif "ban-loai-bat-dong-san-khac" in link: 
            return "Bất động sản khác"
        else:
            # Fallback type if none match
            return "khong-xac-dinh"

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
                # Get the actual link for each property
                property_link = link.get_attribute('href')
                property_type = get_property_type(property_link)  # Determine the property type from the link

                writer.writerow([property_type, price.text, area.text, place.text, property_link])
            except NoSuchElementException:
                pass  # Handle missing elements gracefully


    def crawl_pages(base_url, property_type, max_pages=100):
        for page in range(1, max_pages + 1):
            page_url = f'{base_url}/p{page}' if page > 1 else base_url
            driver.get(page_url)
            sleep(random.randint(5, 10))
            handle_cloudflare()

            get_data(property_type)

            print(f"Crawled page {page} for {property_type}")

    crawl_pages('https://batdongsan.com.vn/nha-dat-ban', 'Nhà', max_pages=5)


# Đóng trình duyệt sau khi crawl
driver.quit()
