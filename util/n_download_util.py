import urllib.request
import os
from typing import List
from util.n_util import NUser
from util.n_util import get_n_entry
import time

delay: int = 5


def save_files_to_dir(file_url_list: List[str], path: str, update=None) -> None:
    """Saves all files represented by a list of url resources to the folder specified.
    The files are being named after the last part of the url."""

    # pretend to be normal user
    # opener=urllib.request.build_opener()
    # opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
    # urllib.request.install_opener(opener)
    current = 1
    total = len(file_url_list)
    for file_url in file_url_list:
        filename = os.path.join(path, file_url.split('/')[-1])
        print('writing {} to {}'.format(file_url, filename))
        if update is not None:
            update(current, total)
        urllib.request.urlretrieve(file_url, filename)
        current += 1
    if update is not None:
        update(current, total)


def download_all_favorites(n_user: NUser, base_dir: str, update_entry=None, update_page=None) -> None:
    print('downloading {}\'s {} favorites...'.format(n_user.username, n_user.fav_count))
    current = 1
    total = n_user.fav_count
    for min_entry in n_user.favorite_list:

        if update_entry is not None:
            update_entry(current_entry=min_entry, current=current, total=total)
        print('downloading entry with id {}'.format(min_entry.n_id))
        entry = get_n_entry(min_entry.n_id)
        if entry is None:
            print('no connection possible, skipping...')
            continue
        if update_page is not None:
            update_page(0, len(entry.image_url_list))
        if not os.path.exists(base_dir):
            print('base directory does not exist, aborting...')
            break
        save_dir = os.path.join(base_dir, entry.digits)
        if os.path.exists(save_dir):
            print('entry already exists, skipping...')
            continue
        else:
            os.mkdir(save_dir)
        save_files_to_dir(entry.image_url_list, save_dir, update=update_page)
        print('waiting for {} seconds...'.format(delay))
        time.sleep(delay)
        current += 1

    if update_entry is not None:
        update_entry(current_entry=None, current=current, total=total)
    print('download finished')

