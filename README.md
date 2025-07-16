# Scraping 
- Mainly using requests and beautiful soups in python to create dataframes and write them to csvs
- Plan to eventually normalize this and hook into ORM for backend 

# Backend 
- Using golang  https://go.dev/
- Using chi for routing for http https://github.com/go-chi/chi might swap to grpc at some point 
- To start the backend for development use ``` go run . ```

# Frontend 
- Using React + TS for the general framework https://react.dev/
- Using Vite for tooling https://vitejs.dev/
- Using MUI for all UI-related concerns https://mui.com/
- To start the frontend for development first run ``` npm install  ``` then ``` npm run dev   ``` 


# Database 
- making massive JSON files out of the existing google docs I have via feeding it info and having LLM scrape + format 
- using said JSON files to in combination with upsert python scripts to recreate and refill normalized SQL database on the fly 
- using postgresql https://www.postgresql.org/ 
