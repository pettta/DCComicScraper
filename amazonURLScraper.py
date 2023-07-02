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
        """ TODO maybe remove? 
        query = name.replace(":", "%3A")
        query = query.replace("(", "%28")
        query = query.replace(")", "%29")
        query = query.replace("&", "%26")
        query = query.replace(",", "%2C")
        query = query.replace("'", "%27")
        query = query.replace("!", "%21")
        query = query.replace("?", "%3F")
        query = query.replace(";", "%3B")
        query = query.replace("=", "%3D")
        query = query.replace("@", "%40")
        query = query.replace("#", "%23")
        query = query.replace("$", "%24")
        query = query.replace("%", "%25")
        query = query.replace("^", "%5E")
        query = query.replace("*", "%2A")
        query = query.replace("+", "%2B")
        query = query.replace("~", "%7E")
        query = query.replace("`", "%60")
        query = query.replace("<", "%3C")
        query = query.replace(">", "%3E")
        query = query.replace("|", "%7C")
        query = query.replace("{", "%7B")
        query = query.replace("}", "%7D")
        query = query.replace("[", "%5B")
        query = query.replace("]", "%5D")
        query = query.replace("\\", "%5C")
        query = query.replace("/", "%2F")
        query = query.replace(".", "%2E")
        query = query.replace("_", "%5F")
        query = query.replace("-", "%2D")
        query = query.replace('"', "%22")
        """
        query = name.replace(" ", "+")
        print(f"https://www.amazon.com/s?k={query}")
        headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}   
        res = requests.get(f"https://www.amazon.com/s?k={query}", headers=headers)
        soup = BeautifulSoup(res.content, 'html.parser')
        print(soup.prettify())
        break
    # TODO: Scrape Amazon for URLS for each of these and write to CSV file