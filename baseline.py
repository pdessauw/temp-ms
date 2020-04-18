"""
"""
import argparse
from os import listdir
from os.path import join, splitext
from typing import Dict

from library.metrics.baseline import BaselineMetric
from settings import DATA_FOLDER

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--init", action='store_true')
    group.add_argument("--list", action='store_true')
    group.add_argument("--set", metavar="prefix.metric=value", type=str, action="append")

    args = parser.parse_args()

    # Create the baseline objects
    baselines = [
        BaselineMetric(join(DATA_FOLDER, csv_filename))
        for csv_filename in listdir(DATA_FOLDER)
        if splitext(csv_filename)[1] == ".csv"
    ]
    baseline_dict = {
        baseline.prefix: baseline for baseline in baselines
    }

    if args.init:
        for baseline in baselines:
            baseline.init_baseline()
    elif args.list:
        for baseline in baselines:
            for metric in baseline.get_metrics():
                print(metric)
    else:  # baseline set
        for set_arg in args.set:
            key, value = set_arg.split("=")
            prefix, metric = key.split(".")

            if prefix not in baseline_dict.keys():
                continue

            baseline_dict[prefix].set_metric(metric, value)




