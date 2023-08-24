import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from bs4 import BeautifulSoup
from scraper.table_visualization import visualize_table


def extract_products_from_site(search_term):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    driver.get(target_url)

    search_input = driver.find_element(By.CSS_SELECTOR, ".c-search__input")
    search_input.send_keys(search_term)
    search_input.send_keys(Keys.RETURN)

    wait = WebDriverWait(driver, 10)

    sorting_button = wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, "#order-dropdown")))
    sorting_button.send_keys(Keys.RETURN)

    sort_by_cheapest = wait.until(ec.visibility_of_element_located((By.CSS_SELECTOR, "#product-list > "
                                                                                     "div.category-navbar.clearfix > "
                                                                                     "span > ul > li:nth-child(3) > a")))
    sort_by_cheapest.send_keys(Keys.RETURN)

    page_source = driver.page_source

    driver.quit()

    soup = BeautifulSoup(page_source, features="html.parser")

    product_elements = soup.select("#normal-product-list > div.list-view > div")

    data = []
    for index, element in enumerate(product_elements, start=1):
        if element.select_one("div#admanager-ad-category-rectangle.admanager-advertisement"):
            continue
        product_name_element = element.select_one("div.name.ulined-link > h2 > a")
        if not product_name_element:
            continue
        product_name = product_name_element.text.strip()

        price_element = element.select_one("div.col-lg-3.col-md-3.col-sm-3.top-right.hidden-xs > a.price")
        price = price_element.text.strip()

        data.append({'Product Name': product_name, 'Price': price})

    df = pd.DataFrame(data)

    return df


async def find_product_command(channel, cmd):
    product_name = cmd.split(" ", 1)[1]
    df = extract_products_from_site(product_name)
    await visualize_table(channel, df)


target_url = "https://www.pazaruvaj.com/"
