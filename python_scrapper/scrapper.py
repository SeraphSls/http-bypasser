import requests
import json
import time
from pathlib import Path

HEADERS = {
    "Content-Type": "application/json",
    "x-algolia-application-id": "OQUBRX6ZEQ",
    "x-algolia-api-key": "8ad949132d497255ffc04accd141f083",
    "Origin": "https://remotive.com",
    "Referer": "https://remotive.com/",
    "User-Agent": "PostmanRuntime/7.36.3"
}

ALGOLIA_AGENT_QUERY = (
    "x-algolia-agent=Algolia%20for%20JavaScript%20(4.14.2)%3B%20Browser%20(lite)&"
    "x-algolia-api-key=8ad949132d497255ffc04accd141f083&"
    "x-algolia-application-id=OQUBRX6ZEQ"
)

BASE_URL = f"https://oqubrx6zeq-dsn.algolia.net/1/indexes/*/queries?{ALGOLIA_AGENT_QUERY}"

def fetch_page(page, query="python"):
    payload = {
        "requests": [
            {
                "indexName": "live_jobs",
                "params": f'query={query}&hitsPerPage=50&page={page}&facets=["tags","job_type","company_name","locations","category"]'
            }
        ]
    }

    response = requests.post(BASE_URL, headers=HEADERS, json=payload)
    response.raise_for_status()
    return response.json()["results"][0]["hits"]

def main():
    all_jobs = []
    for page in range(5):
        try:
            hits = fetch_page(page, query="python")
            for h in hits:
                all_jobs.append({
                    "title": h.get("title", ""),
                    "company": h.get("company_name", ""),
                    "location": h.get("candidate_required_location", ""),
                    "type": h.get("job_type", ""),
                    "url": h.get("url", ""),
                    "publication_date": h.get("publication_date", "")
                })
            print(f"Page {page} OK ({len(hits)} records)")
            time.sleep(0.8)
        except Exception as e:
            print(f"Error on page {page}: {e}")
            time.sleep(1)

    output_path = Path("../output/jobs_node.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(all_jobs, f, indent=2, ensure_ascii=False)

    print(f"File saved with {len(all_jobs)} records at {output_path}")

if __name__ == "__main__":
    main()
