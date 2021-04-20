import urllib.request
import os
from typing import List
from util.n_util import NUser
from util.n_util import get_n_entry
import time
import threading
from util.array_util import slice_array

delay: float = 2.5


class ProgressWrapper:
    """The progress wrapper keeps track of the progress of a operation by wrapping a current number and a total number.
    It also wraps an optional function, which uses the current values and has to have the form 'func(current, total)'."""

    def __init__(self, start, total, update):
        self.current = start
        self.total = total
        self.update_callback = update

    def update(self):
        if self.update_callback is not None:
            self.update_callback(self.current, self.total)


def download_images(lock, file_url_list: List[str], path: str, progress=None):
    for file_url in file_url_list:
        filename = os.path.join(path, file_url.split('/')[-1])
        print('writing {} to {}'.format(file_url, filename))
        urllib.request.urlretrieve(file_url, filename)

        if progress is not None:
            with lock:
                progress.current += 1
                progress.update()


def save_files_to_dir(file_url_list: List[str], path: str, update=None, thread_count: int = 1) -> None:
    """Saves all files represented by a list of url resources to the folder specified.
    The files are being named after the last part of the url.
    The number of threads can be increased to use more threads for the downloading of the images."""

    # pretend to be normal user
    # opener=urllib.request.build_opener()
    # opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
    # urllib.request.install_opener(opener)

    progress = ProgressWrapper(0, len(file_url_list), update)
    progress.update()

    if thread_count < 1 or thread_count > 16:
        print(f'invalid thread count: {thread_count} not in [1, 16]')
        return
    else:
        lock = threading.Lock()
        threads = []
        for i in range(thread_count):
            slices = slice_array(file_url_list, thread_count)
            t = threading.Thread(target=download_images, kwargs=dict(lock=lock, file_url_list=slices[i], path=path,
                                                                     progress=progress),
                                 daemon=True)
            threads.append(t)
            t.start()
        for t in threads:
            t.join()


def download_all_favorites(n_user: NUser, base_dir: str, update_entry=None, update_page=None, thread_count=1) -> None:
    """Downloads all entries favorited by `n_user` using the number of `thread_count` threads."""
    print('downloading {}\'s {} favorites...'.format(n_user.username, n_user.fav_count))

    current_entry = 1
    total_entries = n_user.fav_count
    for min_entry in n_user.favorite_list:
        if update_entry is not None:
            update_entry(current_entry=min_entry, current=current_entry, total=total_entries)
        # get entry data
        print('downloading entry with id {}'.format(min_entry.n_id))
        entry = get_n_entry(min_entry.n_id)
        if entry is None:
            print('no connection possible, skipping...')
            current_entry += 1
            continue

        # check directory is valid
        if not os.path.exists(base_dir):
            print('base directory does not exist, aborting...')
            break
        save_dir = os.path.join(base_dir, entry.digits)
        if os.path.exists(save_dir):
            print('entry already exists, skipping...')
            current_entry += 1
            continue
        else:
            os.mkdir(save_dir)

        # download images
        save_files_to_dir(entry.image_url_list, save_dir, update=update_page, thread_count=thread_count)
        print('waiting for {} seconds...'.format(delay))
        time.sleep(delay)
        current_entry += 1

    if update_entry is not None:
        update_entry(current_entry=None, current=current_entry, total=total_entries)
    print('download finished')
