import os


def create_dir_if_not_exists(path: str) -> bool:
    try:
        if not os.path.exists(path):
            os.mkdir(path)
        return True
    except OSError:
        print("dir creation failed")
        return False
