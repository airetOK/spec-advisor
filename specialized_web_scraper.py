from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

import json

from constants import BASE_URL


options = Options()
options.headless = True


def handle_exceptions(func):
    def wrapper(*args, **kwargs):
        products = []
        try:
            products = func(*args, **kwargs)
        except TimeoutException as te:
            print(te)
        except Exception as e:
            print(e)
        finally:
            return products
    return wrapper


@handle_exceptions
def get_products(url: str) -> list:
    driver = webdriver.Firefox(options=options)
    driver.get(url)
    products = []
    with driver as d:
        w = WebDriverWait(driver, 10)
        w.until(EC.presence_of_element_located(
            (By.CLASS_NAME, "product-list__item")))
        elements = d.find_elements(By.CLASS_NAME, "product-list__item")

        for elem in elements:
            soup = BeautifulSoup(elem.get_attribute(
                'innerHTML'), 'html.parser')
            product_image = soup.find('div', class_='main-product-list-image')
            product_link = soup.find('a', class_='product-image')
            product_dict = json.loads(soup.div['data-product-ic'])

            for key in list(product_dict.keys()):
                if key != 'name' and key != 'price':
                    del product_dict[key]

            product_dict['photo_url'] = product_image.get('data-src')
            product_dict['link'] = f'{BASE_URL}{product_link.get("href")}'
            products.append(product_dict)
        elements.clear()
    return products
