import requests
import time
from bs4 import BeautifulSoup

def get_html(link):
    """Function that gets the HTML of a response"""
    try:
        response = requests.get(link, timeout=5)
        response.raise_for_status()
        return response.text
    except Exception as err:
        print(f'Error fetching {link}: {err}')
        return None
    
def parse_html(html):
    """Function that parses the HTML and looks for titles, along with their links"""
    soup = BeautifulSoup(html, "html.parser")
    for item in soup.select('.titleline > a'):
        yield {
            "title": item.text.strip(),
            "link": item["href"]
        }

def scrape(link):
    """Function that scrapes data from a link by using get_html and parse_html"""
    html = get_html(link)
    if html:
        return list(parse_html(html))