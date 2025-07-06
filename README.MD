# http-bypasser

Scraping modern websites using **raw HTTP requests** — no Selenium, no Playwright, no headless browsers.  
This project demonstrates how to extract data from [Remotive](https://remotive.io/), a remote job platform, by **bypassing the frontend** and directly querying the underlying Algolia API.

## What was done

The site was inspected using the browser's DevTools (Network tab).  
An XHR request was identified during job searches and pagination.  
It revealed the use of **Algolia** as the search engine, based on the endpoint:

`https://<appid>-dsn.algolia.net/1/indexes/*/queries`

Inside the request payload:

- The `page=X` parameter controls pagination
- The `query=python` or `query=node` parameter defines the search term
- Up to 50 results per page using `hitsPerPage=50`

## Required headers

- `X-Algolia-API-Key` (public key, no real auth)
- `X-Algolia-Application-Id` (Algolia app ID)
- Standard browser headers like User-Agent, Origin, and Referer

Requests are sent via **POST**.  
Although the site uses `application/x-www-form-urlencoded`, we switched to `application/json` for cleaner and easier payload handling.

## Manual pagination

Pagination is controlled via the `params` field. Example:

```json
"params": "query=python&page=0&hitsPerPage=50"
```

This returns the first 50 job listings for "python".  
To get more results, increment the `page` value.

## Project structure

```
http-bypasser/
├── node_scrapper/
│   ├── index.js
│   ├── package.json
├── python/
│   ├── scraper.py
│   ├── requirements.txt
├── output/
│   ├── jobs_python.json
│   ├── jobs_node.json
└── README.md
```

## Exported data

Each scraper saves a `.json` file containing:

- Job title
- Company name
- Location
- Job type
- Direct job URL
- Date posted

## No browser involved

This project does **not** rely on Selenium, Playwright, Puppeteer, or any browser engine.  
The goal is to showcase **real reverse engineering** — understanding how the web app works and hitting the underlying APIs directly.

## License

Licensed under **Creative Commons BY-NC 4.0**.  
You may use, modify, and share this code **for non-commercial purposes only**.  
For commercial use or integration into paid products, contact me first.
