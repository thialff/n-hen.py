import os

import n_util as nu
import dir_util as du
import n_download_util as ndu
from credentials import session_id

base_dir = 'saves'
request_url = 'https://nhentai.net/g/144725/'

n_digit = nu.parse_to_n_digit(request_url)
assert n_digit is not None
n_entry = nu.get_n_entry(n_digit)
assert n_entry is not None

n_entry_folder_path = os.path.join(base_dir, n_entry.digits)

du.create_dir_if_not_exists(base_dir)
du.create_dir_if_not_exists(n_entry_folder_path)
ndu.save_files_to_dir(n_entry.image_url_list, n_entry_folder_path)

n_user = nu.get_n_user(session_id)
if n_user is None:
    print('fetching user failed')
    exit()
ndu.download_all_favorites(n_user, base_dir)
