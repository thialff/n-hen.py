import os

import n_util as nu
import dir_util as du
import n_download_util as ndu

baseDir = 'saves'
request_url = 'https://nhentai.net/g/144725/'

n_digit = nu.parse_to_n_digit(request_url)
assert n_digit is not None
n_entry = nu.get_n_entry(n_digit)
assert n_entry is not None

n_entry_folder_path = os.path.join(baseDir, n_entry.digits)

du.create_dir_if_not_exists(baseDir)
du.create_dir_if_not_exists(n_entry_folder_path)
ndu.save_files_to_dir(n_entry.image_url_list, n_entry_folder_path)
