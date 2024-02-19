from ISTScraper import scrape_dc_comics, add_new_comics
import pandas as pd

if __name__ == "__main__":
    all_comics = scrape_dc_comics()
    # Read in IST CSV
    ist_df = pd.read_csv("ist_rw.csv", header=0)
    # Add new comics to the current DataFrame
    new_ist_df = add_new_comics(all_comics, ist_df)
    # Sort the DataFrame by "IST Title" column
    new_ist_df = new_ist_df.sort_values(by="IST Title")
    new_ist_df.to_csv("ist_rw.csv", index=False)
