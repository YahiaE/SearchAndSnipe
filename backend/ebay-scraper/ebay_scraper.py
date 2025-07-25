import requests
import time
import random
import httpx
# from urllib.parse import quote_plus

# Rotate around different agents to prevent IP Ban
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

def delay_search():
    delay = random.uniform(2,6)
    print(f"Delay search for {delay:.2f} seconds...")
    time.sleep(delay)

def search(query: str) -> str:

    try:
        headers = get_random_headers()
        print(f"Searching for {query}...")
        url = f"https://www.ebay.com/sch/i.html?_nkw={query}"
        
        with httpx.Client(headers=headers, http2=True, follow_redirects=True, timeout=10) as session:
            response = session.get(url)
            if response.status_code == 200 and "captcha" not in response.text.lower():
                return response.text
            else:
                print(f"Request blocked / failed: {response.status_code}")
                return None
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    query = input("Enter your eBay search: ")
    html = search(query)

    if html:
        print(html)
        