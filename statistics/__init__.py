import json
import os
import threading

import util.n_util as n_util
from util.array_util import slice_array


class Statistics:
    """
    Holds aggregated statistics about artists and tags of a number of entries.
    """

    def __init__(self):
        self.total_num_entries = 0
        self.artists = {}
        self.tags = {}

    def record_artist(self, artist):
        if artist not in self.artists:
            self.artists[artist] = 1
        self.artists[artist] += 1

    def record_tag(self, tag):
        if tag not in self.tags:
            self.tags[tag] = 1
        self.tags[tag] += 1

    def include(self, other: 'Statistics'):
        """Includes all entries from the `other` into this one."""
        self.total_num_entries += other.total_num_entries
        for artist, count in other.artists.items():
            if artist not in self.artists:
                self.artists[artist] = count
            else:
                self.artists[artist] += count

        for tag, count in other.tags.items():
            if tag not in self.tags:
                self.tags[tag] = count
            else:
                self.tags[tag] += count

    def save_to_file(self, path: str):
        with open(path, 'w') as f:
            f.write(json.dumps(self.__dict__, indent=4))

    def load_from_file(self, path: str):
        """Loads the given statistics file saved via `save_to_file`. Overrides the current attributes of this object."""
        with open(path, 'r') as f:
            self.__dict__ = json.load(f)


def accumulate_directory_statistics(favorites_directory_path: str, thread_count: int = 1) -> Statistics:
    """
    Accumulates statistics from all directories in the given directory.
    This reads the `info.json` file which contains information about the entry.
    """
    if thread_count < 1:
        raise ValueError('thread_count must be at least 1')

    # get all directories
    files_in_directory = [os.path.join(favorites_directory_path, file_name) for file_name in
                          os.listdir(favorites_directory_path)]
    entry_directories = [path for path in files_in_directory if os.path.isdir(path)]

    threads = []
    statistics = []
    slices = slice_array(entry_directories, thread_count)
    for i in range(thread_count):
        statistics.append(Statistics())
        t = threading.Thread(target=_accumulate_directory_statistics_thread,
                             kwargs=dict(entry_directory_paths=slices[i], statistics=statistics[i]),
                             daemon=True)
        threads.append(t)
        t.start()
    for t in threads:
        t.join()

    overall_statistics = Statistics()
    for statistic in statistics:
        overall_statistics.include(statistic)

    return overall_statistics


def _accumulate_directory_statistics_thread(entry_directory_paths: list[str], statistics: Statistics) -> None:
    for entry_dir in entry_directory_paths:
        info_file_path = os.path.join(entry_dir, 'info.json')
        if not os.path.exists(info_file_path):
            print(f'info file ({info_file_path}) not found, skipping...')
            continue

        with open(os.path.join(entry_dir, 'info.json'), 'r') as f:
            entry_info = json.loads(f.read())

            for artist in entry_info['artists']:
                statistics.record_artist(artist)

            for tag in entry_info['tags']:
                statistics.record_tag(tag)

            statistics.total_num_entries += 1


def accumulate_favorites_statistics(session_id: str, thread_count: int = 1) -> Statistics | None:
    """
    Accumulates statistics from all favorites of the user with the session id.
    """
    if thread_count < 1:
        raise ValueError('thread_count must be at least 1')

    # get user
    user = n_util.get_n_user(session_id)
    if user is None:
        # todo replace with raising error
        print('fetching user failed')
        return None

    threads = []
    statistics = []
    slices = slice_array(user.favorite_list, thread_count)
    for i in range(thread_count):
        statistics.append(Statistics())
        t = threading.Thread(target=_accumulate_favorites_statistics_thread,
                             kwargs=dict(entries=slices[i], statistics=statistics[i]),
                             daemon=True)
        threads.append(t)
        t.start()
    for t in threads:
        t.join()

    overall_statistics = Statistics()
    for statistic in statistics:
        overall_statistics.include(statistic)

    return overall_statistics


def _accumulate_favorites_statistics_thread(entries: list[n_util.MinimizedNEntry], statistics: Statistics) -> None:
    for min_entry in entries:
        # get entry data
        entry = n_util.get_n_entry(min_entry.n_id)
        if entry is None:
            print('no connection possible, skipping...')
            continue

        for artist in entry.artists:
            statistics.record_artist(artist)

        for tag in entry.tags:
            statistics.record_tag(tag)

        statistics.total_num_entries += 1


def print_top_10_stats(statistics: Statistics):
    """
    Prints the top 5 artists and tags from the given statistics.
    Meant for testing only.
    # todo remove
    """

    print('Top 10 artists:')
    for artist, count in sorted(statistics.artists.items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f'{artist}: {count}')
    print('\nTop 10 tags:')
    for tag, count in sorted(statistics.tags.items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f'{tag}: {count}')
