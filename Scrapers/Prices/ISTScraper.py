import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np 

def scrape_ist_dc_comics() -> list:
    base_url = "https://www.instocktrades.com/publishers/dc"
    page = 1
    comics = []

    while page < 30:
        url = f"{base_url}?pg={page}"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")

        items = soup.find_all("div", class_="item")
        
        if not items:
            break

        for item in items:
            comic = {}
            comic["title"] = item.find("div", class_="title").text.strip()
            comic["href"] = f'https://www.instocktrades.com{item.find("a")["href"]}'
            comic["image"] = item.find("img")["src"]
            comics.append(comic)

        page += 1

    return comics


def add_new_ist_comics(new_comics: list, current_csv: pd.DataFrame) -> pd.DataFrame:
    '''
    Columns of csv: 
    IST Url,IST Title,OPB Url,Amazon URL,Target URL,Retail Price,OPB Status,OPB Current Price,IST Status,IST Current Price,Amazon Status,Amazon Current Price,Target Status,Target Current Price,Min Current Price,All time Low Price,Target Doc Name,Last Updated
    '''
    # Create a set of IST URLs and titles from the current DataFrame
    current_urls = set(current_csv['IST Url'])
    current_titles = set(current_csv['IST Title'])
    
    # Create a list to store new rows
    new_rows = []
    
    # Iterate over the new comics
    for comic in new_comics:
        url = comic['href']
        title = comic['title']
        
        # Check if the IST URL and title are not in the current DataFrame
        if url not in current_urls and title not in current_titles:
            # Create a new row with IST URL and title
            new_row = {
                'IST Url': url,
                'IST Title': title
            }
            new_rows.append(new_row)
    
    # Append the new rows to the current DataFrame
    new_csv = current_csv.append(new_rows, ignore_index=True)
    
    return new_csv


def get_upc_value_from_ist_product(url: str) -> str:
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    
    upc_element = soup.find("div", class_="upc")
    if upc_element:
        upc_value = upc_element.text.strip()
        # removethe "UPC: " prefix
        upc_value = upc_value.replace("UPC: ", "")
        return upc_value
    else:
        return np.nan
