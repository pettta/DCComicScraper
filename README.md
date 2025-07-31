# Scraping 
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
