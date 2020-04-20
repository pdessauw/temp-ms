"""
"""
from os.path import splitext, basename

import pandas as pd

from library.metrics import DataFileStore


class BaselineMetrics(DataFileStore):
    def __init__(self, filepath):
        self.datafile_path = filepath
        self.prefix = basename(splitext(self.datafile_path)[0])

        super().__init__("%s.baseline.bin" % splitext(self.datafile_path)[0])

    def init_baseline(self):
        dataframe = pd.read_csv(self.datafile_path)
        metrics = {
            key: round(value, 2)
            for key, value in dict(dataframe.mean()).items()
        }

        self._save_data(metrics)

    def get_metric_names(self):
        metrics = self._load_data()
        return list(metrics.keys())

    def get_metric(self, name):
        metrics = self._load_data()
        return metrics[name]

    def get_metrics(self):
        metrics = self._load_data()
        return [
            "%s.%s=%s" % (self.prefix, key, value)
            for key, value in metrics.items()
        ]

    def set_metric(self, name, value):
        metrics = self._load_data()

        if name not in metrics.keys():
            return False

        metrics[name] = round(float(value), 2)
        self._save_data(metrics)
        return True
