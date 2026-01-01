import argparse 

import pandas as pd
import numpy as np

from Scrapers.ISTScraper import scrape_ist_dc_comics, add_new_ist_comics, get_upc_value_from_ist_product

# NOTE: if you need headers use something like this headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}   

def is_nan_upc(row: pd.Series) -> bool:
    try:
        fp_val = float(row['UPC'])
        return np.isnan(fp_val)
    except:
        return True

def update_all_upcs_in_df(current_df: pd.DataFrame, next_n_rows: int):
    # cover the case where the UPC column is not in the DataFrame
    if 'UPC' not in current_df.columns:
        current_df['UPC'] = np.nan
    mask = current_df.apply(is_nan_upc, axis=1)
    # make the next line only the first 50 instances 
    current_df.loc[mask, 'UPC'] = current_df.loc[mask, 'IST Url'].head(next_n_rows).apply(get_upc_value_from_ist_product)
    return current_df

def write_ist_data_to_csv():
    all_comics = scrape_ist_dc_comics()
    # Read in IST CSV
    ist_df = pd.read_csv("ist_rw.csv", header=0, delimiter=',', dtype={'UPC': str})
    # Add new comics to the current DataFrame
    new_ist_df = add_new_ist_comics(all_comics, ist_df)
    # Sort the DataFrame by "IST Title" column
    new_ist_df = new_ist_df.sort_values(by="IST Title")
    # Go through csv and get UPC values
    new_ist_df = update_all_upcs_in_df(new_ist_df.copy(), 75)
    new_ist_df.to_csv("ist_rw.csv", index=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Scrape comic book data from various sources')
    parser.add_argument('--ist', action='store_true', help='Scrape IST data')
    parser.add_argument('--amazon', action='store_true', help='Scrape Amazon data')
    parser.add_argument('--opb', action='store_true', help='Scrape OPB data')
    args = parser.parse_args()
    use_ist = args.ist
    use_amazon = args.amazon
    use_opb = args.opb

    if use_ist:
        write_ist_data_to_csv()
        exit(0)
    if use_amazon:
        pass 
        exit(0)
    if use_opb:
        pass
        exit(0) 
    
    print("No scraper selected")
        