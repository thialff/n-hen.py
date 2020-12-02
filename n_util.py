import re
import requests
from bs4 import BeautifulSoup
from typing import List, Optional

baseUrl = 'https://nhentai.net/g/{}/'
base_thumbnail_url = 'https://t.nhentai.net/galleries/{}/{}t.jpg'
base_image_url = 'https://i.nhentai.net/galleries/{}/{}.jpg'


class NEntry:
    """Represents a n-hentai doujin entry."""

    def __init__(self, digits: str, gallery_id: str, page_count: int, image_url_list: List[str]):
        self.digits: str = digits
        self.gallery_id: str = gallery_id
        self.page_count: int = page_count
        self.image_url_list: List[str] = image_url_list

    def __str__(self) -> str:
        return str(self.__class__) + ": " + str(self.__dict__)


def get_n_entry(n_digit: str) -> Optional[NEntry]:
    """Returns the doujin entry with the given digit."""
    r = requests.get(baseUrl.format(n_digit))
    soup = BeautifulSoup(r.text, 'html.parser')

    cover_image_url = soup.find(id='cover').img['data-src']
    gallery_id_match = re.search('/galleries/([0-9]*)/', cover_image_url)
    if gallery_id_match is None:
        return None
    gallery_id = gallery_id_match.group(1)

    page_count = len(soup.find(id='thumbnail-container').find('div', class_='thumbs').contents)

    image_url_list = []
    for i in range(page_count):
        image_url_list.append(base_image_url.format(gallery_id, i + 1))

    return NEntry(n_digit, gallery_id, page_count, image_url_list)


def parse_to_n_digit(url: str) -> Optional[str]:
    """Parses a n-hentai url to its digit."""
    n_digit_match = re.search('([1-9][0-9]*)', url)
    return n_digit_match.group(1) if n_digit_match is not None else None
