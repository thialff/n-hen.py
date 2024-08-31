import re
import requests
from bs4 import BeautifulSoup
from typing import Optional
from util.n_util_data_classes import NEntry, NUser, MinimizedNEntry
import sys

base_url = 'https://nhentai.net/g/{}/'
base_thumbnail_url = 'https://t.nhentai.net/galleries/{}/{}t.{}'
base_image_url = 'https://i.nhentai.net/galleries/{}/{}.{}'
base_favorite_url = 'https://nhentai.net/favorites/'
paged_favorite_url = 'https://nhentai.net/favorites/?page={}'


def __match_tag_container(tag, match):
    if tag.name != 'div':
        return False
    return match in tag.next


def get_n_entry(n_digit: str) -> Optional[NEntry]:
    """Returns the doujin entry with the given digit."""

    r = requests.get(base_url.format(n_digit))
    soup = BeautifulSoup(r.text, 'html.parser')

    # parse gallery id
    cover_image_url = soup.find(id='cover').img['data-src']
    gallery_id_match = re.search('/galleries/([0-9]*)/', cover_image_url)
    if gallery_id_match is None:
        return None
    gallery_id = gallery_id_match.group(1)

    tag_container = soup.find(id='info').find(id='tags')

    # parse title
    title = soup.find(id='info').find('h1', class_='title').find("span", class_='pretty').text

    # parse artists
    artist_divs = tag_container.find_all(lambda tag: __match_tag_container(tag, 'Artists:'))
    if len(artist_divs) != 1:
        print('Tag container \'Artists\' not found exactly once.', file=sys.stderr)
        return None
    artists = list(map(lambda x: x.text, artist_divs[0].find_all('span', class_='name')))

    # parse tags
    tags_divs = tag_container.find_all(lambda tag: __match_tag_container(tag, 'Tags:'))
    if len(tags_divs) != 1:
        print('Tag container \'Tags\' not found exactly once.', file=sys.stderr)
        return None
    tags = list(map(lambda x: x.text, tags_divs[0].find_all('span', class_='name')))

    thumbnails = soup.find(id='thumbnail-container').find('div', class_='thumbs').contents

    page_count = len(thumbnails)

    cover_url = soup.find(id='cover').find('img', class_='lazyload')['data-src']

    image_url_list = []
    for i, entry in enumerate(thumbnails):
        file_type_match = re.search(r'/galleries/[1-9][0-9]*/[1-9][0-9]*t\.([a-z]+)', entry.find('a').find('img')['data-src'])
        if file_type_match is None:
            return None
        image_url_list.append(base_image_url.format(gallery_id, i + 1, file_type_match.group(1)))

    return NEntry(digits=n_digit, gallery_id=gallery_id, page_count=page_count, image_url_list=image_url_list, artists=artists, title=title, tags=tags, cover_url=cover_url)


def parse_to_n_digit(url: str) -> Optional[str]:
    """Parses a n-hentai url to its digit."""

    n_digit_match = re.search('([1-9][0-9]*)', url)
    return n_digit_match.group(1) if n_digit_match is not None else None


def get_n_user(user_auth_cookie: str) -> Optional[NUser]:
    """Return basic user information and information about the user's favorites. Uses the 'sessionid' cookie for authentication."""

    cookies = {'sessionid': user_auth_cookie}
    r = requests.get(base_favorite_url, cookies=cookies)
    if r.status_code != 200:
        print('auth failed')
        return None
    soup = BeautifulSoup(r.text, 'html.parser')

    # parse basic data
    div_content = soup.find(id='content')
    div_content_header = div_content.find('h1')

    # user name
    user_name_match = re.search(r' ?(.+)\'s favorites', div_content_header.text)
    if user_name_match is None:
        return None
    user_name = user_name_match.group(1)

    # fav_count
    fav_count_match = re.search(r'\(([1-9][0-9]*)\)', div_content_header.find('span', class_='count').text.replace(",", ""))
    if fav_count_match is None:
        return None
    fav_count = int(fav_count_match.group(1))

    # page_count
    last_page_link = div_content.find('section')
    if last_page_link is None:
        page_count = 1
    else:
        last_page_link = last_page_link.find(class_='last')['href']
        page_count_match = re.search(r'/favorites/\?page=([1-9][0-9]*)', last_page_link)
        if page_count_match is None:
            return None
        page_count = int(page_count_match.group(1))

    # parse favorites
    favorite_list = []
    for i in range(0, page_count):
        # parse one page
        for div_favorite in soup.find(id='favcontainer').children:
            a_cover = div_favorite.find('div', class_='gallery').find('a', class_='cover')
            n_id_match = re.search(r'/g/([1-9][0-9]*)/', a_cover['href'])
            if n_id_match is None:
                return None
            gallery_id_match = re.search(r'/galleries/([1-9][0-9]*)/thumb\.', a_cover.find('img', class_='lazyload')['data-src'])
            if gallery_id_match is None:
                return None
            full_name = div_favorite.find('div', class_='caption').text
            normalized_name = __normalizeName(full_name)
            favorite_list.append(MinimizedNEntry(n_id_match.group(1), gallery_id_match.group(1), full_name, normalized_name))

        # get new page and soup
        if i + 2 > page_count:
            break
        r = requests.get(paged_favorite_url.format(i + 2), cookies=cookies)
        if r.status_code != 200:
            print('auth failed')
        else:
            soup = BeautifulSoup(r.text, 'html.parser')

    return NUser(user_name, fav_count, page_count, favorite_list)


def __normalizeName(full_name: str):
    normalized_name_match = re.search(r'](.*?)\[', full_name)
    if normalized_name_match is None:
        return full_name
    else:
        normalized_name = normalized_name_match.group(1)
        return normalized_name.strip()
