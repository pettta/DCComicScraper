import requests 
import pandas as pd 
from bs4 import BeautifulSoup

def convert_IST_name_to_amazon_search(name: str):
    name_list = name.split(" ")
    for loc, word in enumerate(name_list):
        if word.isnumeric() and word[0] == "0":
            name_list[loc] = word[1:]  
        if word == "HC":
            name_list[loc] = "Hardcover"
        if word == "TP":
            name_list[loc] = "Paperback"
    return " ".join(name_list)

if __name__ == "__main__":
    # Read in IST CSV
    ist_df = pd.read_csv("ist.csv", header=0)
    print(ist_df.columns[0])
    # Convert IST name to Amazon search
    for name in list(ist_df['IST Title'].apply(convert_IST_name_to_amazon_search)):
        query = name.replace(" ", "+")
        print(f"https://www.amazon.com/s?k={query}")
        headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}   
        res = requests.get(f"https://www.amazon.com/s?k={query}", headers=headers)
        soup = BeautifulSoup(res.content, 'html.parser')
        print(soup.prettify())
        break
    # TODO: Scrape Amazon for URLS for each of these and write to CSV file