import os
import pathlib
import shutil


def get_base_dir():
    return pathlib.Path(__file__).resolve().parent.parent


def create_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)


def clear_dir(path):
    if os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path)


def get_path(path):
    return os.path.join(get_base_dir(), path)
