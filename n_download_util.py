import urllib.request
import os
from typing import List


def save_files_to_dir(file_url_list: List[str], path: str) -> None:
    """Saves all files represented by a list of url resources to the folder specified.
    The files are being named after the last part of the url."""

    # pretend to be normal user
    # opener=urllib.request.build_opener()
    # opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
    # urllib.request.install_opener(opener)

    for file_url in file_url_list:
        filename = os.path.join(path, file_url.split('/')[-1])
        print('writing {} to {}'.format(file_url, filename))
        urllib.request.urlretrieve(file_url, filename)
