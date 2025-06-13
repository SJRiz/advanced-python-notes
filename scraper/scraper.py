import requests
import time
import argparse
import json
from tqdm import tqdm
from bs4 import BeautifulSoup

def get_html(link, attempts):
    """
    Function that gets the HTML of a response.

    Args:
        link (string): link to a website
        attempts (int): How many times to try requesting
    
    Returns:
        HTML structure of the website (string)
    
    """

    # Header to not get detected by anti-bots
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(link, headers=headers, timeout=5)
        response.raise_for_status()
        return response.text
    except Exception as err:
        if attempts > 0:
            print(f'Error fetching {link}: {err}')
            print(f'Retrying... {attempts} attempts left')
            time.sleep(1)
            return get_html(link, attempts - 1)
        else:
            return None

def parse_html(html, depth, visited):
    """
    Generator that parses the HTML structure to look for any links.
    Also parses internal links up to depth

    Args:
        html (string): HTML structure of a website
        depth (int): How many layers of links to crawl through
        visited (set): A set of all visited links

    Yields:
        Dict containing a title, link, internalInfo
    """

    soup = BeautifulSoup(html, "html.parser")

    for item in tqdm(soup.find_all('a', href=True), desc="Parsing titles", leave=False):
        href = item["href"]

        # Ignore links already scraped
        if href in visited:
            continue
        visited.add(href)

        # Scrape internal links recursively up to --depth
        internal = scrape(href, 0, depth - 1, visited)
        internal_data = list(internal) if internal else ""
        yield {
            "title": item.text.strip(),
            "link": href,
            "internalInfo": internal_data
        }

def scrape(link, attempts, depth, visited):
    """
    Function that scrapes data from a link by using get_html and parse_html.

    Args:
        link (string): link to a website
        attempts (int): How many times to try requesting
        depth (int): How many layers of links to crawl through
        visited (set): A set of all visited links

    Returns:
        List of all links found within a website, as well as internal links
    """

    if depth > 0:
        html = get_html(link, attempts)
        if html:
            return list(parse_html(html, depth, visited))
    else:
        return None

def main():

    # Set up the CLI
    parser = argparse.ArgumentParser(description="Scrape a news site")
    parser.add_argument('--url', required=True, help="URL to scrape")
    parser.add_argument('--attempts', type=int, default=3, help="Number of retries")
    parser.add_argument('--depth', type=int, default=2, help="How many internal links to crawl through")

    args = parser.parse_args()
    data = scrape(args.url, args.attempts, args.depth, set())

    # Dump the results in a results.json file
    with open("results.json", "w", encoding='utf-8') as file:
        json.dump(data, file, indent=2, ensure_ascii=False)
        print("Scrape complete")

if __name__ == '__main__':
    main()