import time
import urllib.error
from contextlib import suppress
from typing import Tuple
from urllib.request import Request, urlopen

from bs4 import BeautifulSoup
from cleantext import clean


def get_data(base_url: str, word: str) -> Tuple[str, str, str]:
    url = f"{base_url}{word}"
    req = Request(url)
    time.sleep(5.)

    with suppress(urllib.error.HTTPError):
        html_page = urlopen(req, timeout=5.)
        text = extract_text(html_page)

        return text, word, url


def extract_text(html_page: str) -> str:
    soup = BeautifulSoup(html_page, "html.parser")
    text = ''

    for paragraph in soup.find_all('p'):
        paragraph = paragraph.text
        text += clean(paragraph)

    return text


def print_record(data: dict) -> None:
    echo = f"Phrase {data.get('key-phrase')}:'{data.get('content')[:20]} ...' from {data.get('from')},\
    {data.get('date')}"
    print(echo)
