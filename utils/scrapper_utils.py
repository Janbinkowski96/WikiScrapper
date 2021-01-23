import urllib.error
from contextlib import suppress
from typing import Tuple
from urllib.request import Request, urlopen

from bs4 import BeautifulSoup


def get_data(base_url: str, word: str) -> Tuple[str, str, str]:

    url = f"{base_url}{word}"
    req = Request(url)

    with suppress(urllib.error.HTTPError):
        html_page = urlopen(req)
        text = extract_text(html_page)

        return text, word, url


def extract_text(html_page: str) -> str:
    soup = BeautifulSoup(html_page, "html.parser")
    text = ''
    for paragraph in soup.find_all('p'):
        text += paragraph.text.replace("\n", "")

    return text
