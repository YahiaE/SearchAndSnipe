import asyncio
import random
from typing import List, Dict
import httpx
from bs4 import BeautifulSoup

USER_AGENTS = [ 
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.91 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:116.0) Gecko/20100101 Firefox/116.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:115.0) Gecko/20100101 Firefox/115.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.136 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36"
]

async def fetch(client: httpx.AsyncClient, url: str) -> str:
    await asyncio.sleep(random.uniform(2, 6))
    headers = {"User-Agent": random.choice(USER_AGENTS)}
    response = await client.get(url, headers=headers)
    response.raise_for_status()
    return response.text

async def parse_search_page(html: str) -> List[Dict]:
    soup = BeautifulSoup(html, "lxml")
    results = []

    listings = soup.select(".srp-results li.s-item")
    
    for listing in listings:
        def get_attr(selector, attr=None):
            elem = listing.select_one(selector)
            if not elem:
                return ""
            return elem.get(attr) if attr else elem.get_text(strip=True)
        
        result = {
            "url": get_attr("a.s-item__link", "href").split("?")[0],
            "title": get_attr(".s-item__title > span"),
            "price": get_attr(".s-item__price"),
            "shipping": get_attr(".s-item__shipping"),
            "list_date": get_attr(".s-item__listingDate span"),
            "condition": get_attr(".s-item__subtitle .SECONDARY_INFO"),
            "photo": get_attr(".s-item__image img", "src"),
            "rating": get_attr(".s-item__reviews .clipped"),
            "rating_count": get_attr(".s-item__reviews-count span"),
            "subtitles": [s.get_text(strip=True) for s in listing.select(".s-item__subtitle > *")],
        }
        results.append(result)

    return results

async def main(search_url: str):
    async with httpx.AsyncClient(http2=True, follow_redirects=True, timeout=10) as client:
        html = await fetch(client, search_url)
        listings = await parse_search_page(html)
        
        for listing in listings:
            print(listing)
            print()

if __name__ == "__main__":
    url = "https://www.ebay.com/sch/i.html?_nkw=laptop"
    asyncio.run(main(url))
