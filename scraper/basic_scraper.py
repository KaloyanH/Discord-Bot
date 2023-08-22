import discord
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from bs4 import BeautifulSoup


def extract_products_from_site(search_term):
    options = webdriver.EdgeOptions()
    options.add_argument("--headless")
    driver = webdriver.Edge(options=options)
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


async def visualize_table(channel, df):
    plt.figure(figsize=(12, 8))

    df.sort_values(by='Price', inplace=True, ascending=False)

    bar_width = 0.6

    bars = plt.barh(df['Product Name'], df['Price'], color='skyblue', height=bar_width)
    plt.ylabel('Product Name')
    plt.title('Product Prices')
    plt.tight_layout()

    for index, bar in enumerate(bars):
        plt.text(bar.get_width(), bar.get_y() + bar.get_height() / 2, df['Price'][index],
                 ha='left', va='center', rotation=0)

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    await channel.send(file=discord.File(buffer, filename='product_chart.png'))

    plt.close()


async def find_product_command(channel, cmd):
    product_name = cmd.split(" ", 1)[1]
    df = extract_products_from_site(product_name)
    await visualize_table(channel, df)


target_url = "https://www.pazaruvaj.com/"
