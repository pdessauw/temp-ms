"""
"""
import pickle
from os.path import splitext, basename

import pandas as pd


class BaselineMetrics(object):
    def __init__(self, filepath):
        self.datafile_path = filepath
        self.prefix = basename(splitext(self.datafile_path)[0])
        self.baseline_path = "%s.baseline.bin" % splitext(self.datafile_path)[0]

    def _load_metrics(self):
        with open(self.baseline_path, "rb") as baseline_fp:
            return pickle.load(baseline_fp)

    def _save_metrics(self, metrics):
        with open(self.baseline_path, "wb") as baseline_fp:
            pickle.dump(metrics, baseline_fp)

    def init_baseline(self):
        dataframe = pd.read_csv(self.datafile_path)
        metrics = {
            key: round(value, 2)
            for key, value in dict(dataframe.mean()).items()
        }

        self._save_metrics(metrics)

    def get_metrics(self):
        metrics = self._load_metrics()
        return [
            "%s.%s=%s" % (self.prefix, key, value)
            for key, value in metrics.items()
        ]

    def set_metric(self, name, value):
        metrics = self._load_metrics()

        if name not in metrics.keys():
            return False

        metrics[name] = round(float(value), 2)
        self._save_metrics(metrics)
        return True
