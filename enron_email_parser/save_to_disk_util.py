import gzip
import os
import pathlib
import pickle


def save_to_disk(path, data_dict, protocol=-1):
    __create_directories_to_path(path)

    with gzip.open(path, 'wb') as f:
        pickle.dump(data_dict, f, protocol)


def __create_directories_to_path(path):
    dirname = os.path.dirname(path)
    pathlib.Path(dirname).mkdir(parents=True, exist_ok=True)
