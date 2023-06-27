import requests 
import pandas as pd 
from bs4 import BeautifulSoup

isv_df = pd.read_csv("ist.csv", header=0, delimiter='\t') 

def check_prices(comic: str): 
    comic_list = comic.split(" ")
    dashed_comic = "-".join(comic_list)
    print("OPB COMICS:", check_opb_prices(dashed_comic))
    
    
def check_opb_prices(opb_comic: str):
    res = requests.get(f'http://organicpricedbooks.com/products/{opb_comic}')
    soup = BeautifulSoup(res.content, 'html.parser')
    title=soup.find("h1", attrs={'class': 'product-title'}).string.strip()
    original_price = soup.find("span", attrs={'class': 'money price__compare-at--single'}).string.strip()
    current_price_min =soup.find("span", attrs={'class': 'money price__current--min'}).string.strip()
    current_price_max =soup.find("span", attrs={'class': 'money price__current--max'}).string.strip()
    return title, original_price, current_price_min, current_price_max
 
def check_ist_prices(ist_comic: str):
    print(isv_df) 


if __name__ == "__main__":
    print(check_prices('JLA BY GRANT MORRISON OMNIBUS HC'))
    check_ist_prices('') 