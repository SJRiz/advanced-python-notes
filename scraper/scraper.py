import requests
import time
import argparse
import json
from bs4 import BeautifulSoup

def get_html(link, attempts):
    """Function that gets the HTML of a response"""

    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (compatible; MyScraper/1.0)"
        }
        response = requests.get(link, headers=headers, timeout=5)
        response.raise_for_status()
        return response.text
    except Exception as err:
        print(f'Error fetching {link}: {err}')
        if attempts > 0:
            print(f'Retrying... {attempts} attempts left')
            time.sleep(1)
            return get_html(link, attempts - 1)
        else:
            return None

def parse_html(html, depth):
    """Function that parses the HTML and looks for titles, along with their links"""

    soup = BeautifulSoup(html, "html.parser")

    # Look for the anchor tag within titleline
    for item in soup.select('.titleline > a'):
        # Look for more info within the internal link through recursion
        internal = scrape(item['href'], depth - 1, 3)
        internal_data = list(internal) if internal else None
        yield {
            "title": item.text.strip(),
            "link": item["href"],
            "internal": internal_data
        }

def scrape(link, attempts, depth):
    """Function that scrapes data from a link by using get_html and parse_html"""
    if depth > 0:
        html = get_html(link, attempts)
        if html:
            return list(parse_html(html, depth))
    else:
        return None
    
def main():
    parser = argparse.ArgumentParser(description="Scrape a news site")
    parser.add_argument('--url', required=True, help="URL to scrape")
    parser.add_argument('--attempts', type=int, default=3, help="Number of retries")
    parser.add_argument('--depth', type=int, default=2, help="How many internal links to crawl through")

    args = parser.parse_args()
    data = scrape(args.url, args.attempts, args.depth)

    with open("results.json", "w") as file:
        json.dump(data, file, indent=2)
        print("Scrape complete")

if __name__ == '__main__':
    main()