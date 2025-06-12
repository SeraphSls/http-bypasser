# http-bypasser

Scraping modern websites using **raw HTTP requests** — no Selenium, no Playwright, no headless browsers.  
This project demonstrates how to extract data from [Remotive](https://remotive.io/) — a remote job platform — by **bypassing the frontend** and directly querying the underlying Algolia API.

## 🧠 What I did

- Opened the site and jumped straight into the Network tab (DevTools).
- Spotted an XHR request triggered during job search and pagination.
- Found that the site uses **Algolia** as a search engine — the endpoint gives it away:  
  `https://<appid>-dsn.algolia.net/1/indexes/*/queries`
- Inside the request payload:
  - There’s a `page=X` param to control pagination.
  - You can set `query=python`, `query=node`, etc.
  - Up to **50 results per page** using `hitsPerPage=50`.

### 🔐 Headers detected

- `X-Algolia-API-Key` → public key, no real auth
- `X-Algolia-Application-Id` → Algolia app instance ID
- Standard User-Agent, Origin, and Referer from the browser

These requests are sent via **POST**, and by default the site uses:

```
Content-Type: application/x-www-form-urlencoded
```

But for cleaner structure, we use **`application/json`** — it works the same, and it's easier to manage.

## 🔁 Manual pagination

Scrape page by page using the param:

```json
"params": "query=python&page=0&hitsPerPage=50"
```

> That gives the first 50 “python” job results.  
> Then increment to `page=1`, `page=2`, and so on.

## 📁 Project structure

```bash
http-bypasser/
├── node_scrapper/
│   ├── index.js         # Node.js scraper using Axios
│   ├── package.json
├── python/
│   ├── scraper.py       # Python scraper using requests
│   ├── requirements.txt
├── output/
│   ├── jobs_python.json
│   ├── jobs_node.json
└── README.md            # You are here
```

## 📤 Exported data

Each scraper dumps a structured `.json` output with:

- Job title
- Company
- Location
- Job type
- Direct URL
- Date posted

## 🚫 No browser needed

This project **does NOT use**:
- Selenium
- Playwright
- Puppeteer

The idea is **real reverse engineering** — inspecting the web app, understanding how data flows, and hitting the exact endpoints yourself.

## 📜 License

This project is licensed under **Creative Commons BY-NC 4.0**.  
You may use, modify, and share this code **for non-commercial purposes only**.  
Wanna sell it or embed into a paid product? Contact me first.
