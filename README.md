# Scraping 
## Issues Scraping 
- Need to write a highly concurrent webcrawler in go to make a database of issues, using dc fandom, noting the following: 
- (1) they use character_vol_num for each volume https://dc.fandom.com/wiki/Superman_Vol_1 https://dc.fandom.com/wiki/Superman_Vol_2 
- (2) they add underscores for spaces between that and the issue number https://dc.fandom.com/wiki/Superman_Vol_2_0
- make sure to go through ALL the story arcs for the issues to assemble the following object 
- { "sections" :["section 1 title" , ...], "main_characters": ["superman", ...], "supporting_characters": ["jimmy olsen", ...], "writers" : ["Dan Jurgens", ...], "pencilers": [], "cover_artists": [], "inkers": [], "colorists": [], "letterers": [], "executive_editor": "", "editors": []} 


## Sales Tracking 
- Mainly using requests and beautiful soups in python to create dataframes and write them to csvs
- Plan to eventually normalize this and hook into ORM for backend 
- The main use case of this will be tracking sales, prices, and the general status of books.

# Backend 
- Using python
- Using fastapi 
- To start the backend for development use ``` python local_setup.py  ```

# Frontend 
- Using Vue + TS for the general framework 
- Using Vite for tooling https://vitejs.dev/
- Using Vuetify for all UI-related concerns 
- To start the frontend for development first run ``` npm install  ``` then ``` npm run dev   ``` 


# Database 
- making massive JSON files out of the existing google docs I have via feeding it info and having LLM scrape + format 
- using said JSON files to in combination with upsert python scripts to recreate and refill normalized SQL database on the fly 
- using postgresql https://www.postgresql.org/ 
- note that i will have "children" and "equivalents" in the JSON file, but I really just want them all to be loaded into the database without that distinction. We can do the overlaying logic in the frontend, so that users can see clearly that some books double dip the same title. (then maybe we do a minimum spanning tree of issues, or minimum spanning tree of recommended issues, etc...)
