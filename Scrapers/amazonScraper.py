import requests 
import pandas as pd 
from bs4 import BeautifulSoup
import requests
from bs4 import BeautifulSoup


def get_amazon_price_and_name(isbn_upc):
    # TODO This might not actually redirect the request, make sure that ends up working 
    url = f"https://camelcamelcamel.com/search?sq={isbn_upc}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find the current price
    price_element = soup.find('div', class_='pwheader amazon').find('span', class_='price')
    price = price_element.text.strip() if price_element else 'Price not found'
    
    # Find the product name
    name_element = soup.find('a', href=url)
    name = name_element.text.strip() if name_element else 'Name not found'
    
    return price, name
