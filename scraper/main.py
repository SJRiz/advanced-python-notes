import requests
import time
from bs4 import BeautifulSoup
from functools import lru_cache

def get_html(link, attempts):
    """Function that gets the HTML of a response"""
    try:
        response = requests.get(link, timeout=5)
        response.raise_for_status()
        return response.text
    except Exception as err:
        print(f'Error fetching {link}: {err}')
        if attempts > 0:
            print(f'Retrying... {attempts} attempts left')
            time.sleep(2)
            return get_html(link, attempts - 1)
        else:
            return None
    
def parse_html(html):
    """Function that parses the HTML and looks for titles, along with their links"""
    soup = BeautifulSoup(html, "html.parser")
    for item in soup.select('.titleline > a'):
        yield {
            "title": item.text.strip(),
            "link": item["href"]
        }

@lru_cache(maxsize=120)
def scrape(link):
    """Function that scrapes data from a link by using get_html and parse_html"""
    html = get_html(link, 3)
    if html:
        return list(parse_html(html))
    
data = scrape("https://news.ycombinator.com/")
print(data)