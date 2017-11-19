import gzip
import os
import pathlib
import pickle


def save_to_disk(path, data_dict, protocol=-1):
    # creates directories recursively for saving file
    pathlib.Path(os.path.dirname(path)).mkdir(parents=True, exist_ok=True)

    with gzip.open(path, 'wb') as f:
        pickle.dump(data_dict, f, protocol)
