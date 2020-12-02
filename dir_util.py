import os


def create_dir_if_not_exists(path):
    print('attempt creation of dir "{}"'.format(path))
    try:
        if not os.path.exists(path):
            os.mkdir(path)
    except OSError:
        print("dir creation failed")
