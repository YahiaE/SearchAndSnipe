import random
import httpx
import json
import asyncio
from typing import List
from urllib.parse import urlencode
from bs4 import BeautifulSoup


# Sort fields on ebay
SORTING_MAP = {
    "best_match": 12,
    "ending_soon": 1,
    "newly_listed": 10
}

# Rotate around different agents to prevent IP Ban / prevent Captcha
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
    "Mozilla/5.0 (X11; Linux x86_64)",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X)",
    "Mozilla/5.0 (iPad; CPU OS 13_2_3 like Mac OS X)"
]

def get_random_headers():
    return {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept-Language": "en-US,en;q=0.9"
    }

async def delay_search(min: int, max: int):
    delay = random.uniform(min,max)
    print(f"Delay search for {delay:.2f} seconds...")
    await asyncio.sleep(delay)


async def fetch_page(client: httpx.AsyncClient, url: str, min: int, max: int) -> httpx.Response:
    await delay_search(min,max)
    headers=get_random_headers()
    response = await client.get(url,headers=headers)
    response.raise_for_status()
    if "captcha" in response.text.lower():
        raise RuntimeError("Captcha Detected. Cannot scrape")
    return response # returns HTML page of given URL if we don't hit a captcha


async def scrape(query: str, max_pages: int = 1, category: int = 0, items_per_page: int = 240, sort: str="newly_listed") -> str:
    def build_url(page: int) -> str:
        params = {
            "_nkw": query,
            "_sacat": category,
            "_ipg": items_per_page,
            "_sop": SORTING_MAP.get(sort),
            "_pgn": page,
        }

        return f"https://www.ebay.com/sch/i.html?{urlencode(params)}"
    
    async with httpx.AsyncClient(http2=True, follow_redirects=True, timeout=10) as client:
        url = build_url(1)
        print(f"Fetch HTML from {url}...")
        first_response = await fetch_page(client,url,2,6)
        page = first_response.text

        soup = BeautifulSoup(first_response, "lxml")
        count_results = soup.select("li.s-item")
        
        print(f"Total results from first page: {len(count_results)}")
        return page

if __name__ == "__main__":

    async def test():
        from pathlib import Path
        query = input()
        pages = await scrape(query)
        Path("output.html").write_text(pages,encoding="utf-8")
    
    asyncio.run(test())
    