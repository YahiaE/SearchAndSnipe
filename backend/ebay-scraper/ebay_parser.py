from typing import List,Dict
from bs4 import BeautifulSoup

def parse_search(html: str) -> List[Dict]:
    soup = BeautifulSoup(html, "lxml")
    results = []

    listings = soup.select(".srp-results li.s-item")

    def get_attribute(selector, attr=None): # Checks CSS selector string and see if the attribute of the selected HTML element (the listing) actually exist
        elem = listing.select_one(selector)
        if not elem:
            return ""
        return elem.get(attr) if attr else elem.get_text(strip=True)

    for listing in listings:
        result = { # Create json of listing
            "url": get_attribute("a.s-item__link", "href").split("?")[0],
            "title": get_attribute(".s-item__title > span"),
            "price": get_attribute(".s-item__price"),
            "shipping": get_attribute(".s-item__shipping"),
            "list_date": get_attribute(".s-item__listingDate span"),
            "condition": get_attribute(".s-item__subtitle .SECONDARY_INFO"),
            "photo": get_attribute(".s-item__image img", "src"),
            "rating": get_attribute(".s-item__reviews .clipped"),
            "rating_count": get_attribute(".s-item__reviews-count span"),
            "subtitles": [s.get_text(strip=True) for s in listing.select(".s-item__subtitle > *")],
        }

        results.append(result) # Append to list of listings

    return results

# if __name__ == "__main__":

#     with open("output.html", "r", encoding="utf-8") as file:
#         html = file.read()
    
#     listings = parse_search(html)

#     for listing in listings:
#         print(listing)