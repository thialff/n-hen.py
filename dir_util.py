import os


def create_dir_if_not_exists(path: str) -> None:
    try:
        if not os.path.exists(path):
            os.mkdir(path)
    except OSError:
        print("dir creation failed")
