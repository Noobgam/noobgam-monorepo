# heavily inspiered by https://github.com/blue-codes-yep/AI_STEAM/blob/main/utils/scraper.py
import json
import logging
import os
import queue
import re
import threading
import time
from typing import List, Optional, TypedDict

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from playwright._impl._api_structures import SetCookieParam
from scraper_api import ScraperAPIClient
from tqdm import tqdm

load_dotenv()
username = os.environ["STEAM_USERNAME"]
password = os.environ["STEAM_PASSWORD"]
cookies = os.environ["STEAM_COOKIES"]
api_key = os.environ["SCRAPER_API_KEY"]

PAGE_SIZE = 50
client = ScraperAPIClient(api_key=api_key)


class ScrapeResult(TypedDict):
    link: str
    item_nameid: str


SCRAPED_LINKS_PATH = "data/scraped_links.json"


def save_scraped(file_name: str, res: List[ScrapeResult]):
    import os

    if not os.path.exists("data"):
        os.makedirs("data")
    with open(file_name, "w") as f:
        f.write(json.dumps(res))


def load_scraped(file_name: str) -> List[ScrapeResult]:
    try:
        with open(file_name, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []


class BackOffSteamException(Exception):
    pass


def parse_cookie_to_set(cookie: str) -> List[SetCookieParam]:
    parts = [part.strip().split("=") for part in cookie.split(";")]
    return [
        SetCookieParam(
            name=part[0],
            value=part[1],
            domain=".steamcommunity.com",
            path="/",
            sameSite="None",
            secure=True,
        )
        for part in parts
    ]


def get_headers():
    return {"Cookie": cookies}


def get_item_links(start=0) -> List[str]:
    url = f"https://steamcommunity.com/market/search/render/?appid=730&start={start}&count={PAGE_SIZE}&search_descriptions=0&sort_column=popular&sort_dir=desc"
    response = requests.get(url, headers=get_headers())
    if response.status_code != 200:
        raise BackOffSteamException(f"response status code {response.status_code}")
    data = response.json()
    # Parse the HTML from the response
    soup = BeautifulSoup(data["results_html"], "html.parser")

    # Get all item elements
    item_elements = soup.select(".market_listing_row_link")

    # Extract item links
    item_links = [item["href"] for item in item_elements]
    return item_links


def get_item_id(link):
    logging.info(f"Parsing a link {link}")
    item_nameid: str
    res = client.get(link)
    full_text = res.text
    srch = re.search(r"Market_LoadOrderSpread.*\( +(\d+)", full_text)
    item_nameid = srch.group(1)
    return item_nameid


def fetch_all_item_links(max_pages=None):
    shift = 0
    item_links = []
    iteration = 1
    while True:
        if max_pages and iteration > max_pages:
            break
        logging.info(f"Doing iteration {iteration}")
        iteration += 1
        try:
            this_page = get_item_links(shift)
        except Exception as e:
            logging.error(f"Couldn't parse page, will retry {e}")
            time.sleep(10)
            continue
        if not this_page:
            break
        item_links += this_page
        shift += len(this_page)
    return item_links


item_links_queue = queue.Queue()
item_link_results: queue.Queue[ScrapeResult] = queue.Queue()

pbar: tqdm


def process_links():
    while True:
        link: Optional[str] = None
        res: Optional[str] = None
        try:
            link = item_links_queue.get_nowait()
            logging.info(f"Processing link {link}")
            res = get_item_id(link)
            tqdm.update(1)
            item_links_queue.task_done()
            logging.info(f"ItemId: {link}:{res}")
        except queue.Empty:
            return
        except Exception as e:
            logging.error(f"Something bad happened, returning link back {e}")
            pass
        finally:
            if res:
                item_link_results.put_nowait(
                    ScrapeResult(
                        link=link,
                        item_nameid=res,
                    )
                )
            elif not res and link:
                item_links_queue.put_nowait(link)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    item_links = fetch_all_item_links(max_pages=1)
    already_scraped = load_scraped(SCRAPED_LINKS_PATH)
    scraped_links = set(map(lambda x: x["link"], already_scraped))
    filtered_item_links = [
        item_link for item_link in item_links if item_link not in scraped_links
    ]

    tqdm = tqdm(total=len(filtered_item_links))
    for i in filtered_item_links:
        item_links_queue.put(i)

    tt = []
    for i in range(5):
        tt.append(threading.Thread(target=process_links, daemon=True))
    for t in tt:
        t.start()

    for t in tt:
        t.join()

    save_scraped(SCRAPED_LINKS_PATH, already_scraped + list(item_link_results.queue))
