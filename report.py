"""
"""
import csv
import datetime
from os.path import join, exists

from library.csv import log_entry
from settings import COMMANDS, DATA_FOLDER

if __name__ == "__main__":
    date = datetime.datetime.now()
    date_str = date.strftime("%Y-%m-%d %H:%M")

    for command in COMMANDS:
        command_return = command().execute()

        if command_return is None:
            continue

        for entry in command_return:
            data_filepath = join(DATA_FOLDER, "%s.csv" % entry["title"])
            del entry["title"]
            entry["date"] = date_str

            log_entry(entry, data_filepath)
