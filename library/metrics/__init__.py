import pickle
from pickle import UnpicklingError


class DataFileStore(object):
    def __init__(self, filepath):
        self.__filepath = filepath
        self.__data = None

    def _load_data(self):
        if self.__data is not None:
            return self.__data

        try:
            with open(self.__filepath, "rb") as baseline_fp:
                self.__data = pickle.load(baseline_fp)
        except FileNotFoundError:
            self.__data = None
        except UnpicklingError:
            self.__data = None

        return self.__data

    def _save_data(self, data):
        self.__data = data

        with open(self.__filepath, "wb") as baseline_fp:
            pickle.dump(self.__data, baseline_fp)
