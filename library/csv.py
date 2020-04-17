from os.path import exists
import csv


def log_entry(entry, filepath):
    # Retrieve headers and create file if needed
    if not exists(filepath):
        # Insert data in the first position
        entries = list(entry.keys())
        entries.remove("date")
        entries.insert(0, "date")
        headers = ",".join(entries)
        with open(filepath, "w") as logfile:
            logfile.write("%s\n" % headers)

    # Read headers from CSV file
    with open(filepath, "r") as logfile:
        headers = logfile.readline().strip()

    # Add entry to the list
    with open(filepath, "a") as logfile:
        logfile_writer = csv.DictWriter(logfile, fieldnames=headers.split(","))
        logfile_writer.writerow(entry)
