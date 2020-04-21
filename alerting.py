"""
"""
import argparse
import os
from os import listdir
from os.path import join, splitext

from library.commands.mail import MailCommand
from library.metrics.alerts import AlertManager
from library.string import to_bytes
from settings import DATA_FOLDER, ALERT_TIMEFRAME_MINUTES, ALERTS, DEFAULT_LEVEL

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--time", type=int, default=ALERT_TIMEFRAME_MINUTES)
    parser.add_argument("--all", action="store_true")

    args = parser.parse_args()

    datafiles = [join(DATA_FOLDER, csv_filename)
                 for csv_filename in listdir(DATA_FOLDER)
                 if splitext(csv_filename)[1] == ".csv"]
    alert_manager = AlertManager(datafiles)
    alert_manager.analyze(timeframe=args.time)

    html = alert_manager.to_html(all_data=args.all)

    if html is not None or (alert_manager.alert_level == DEFAULT_LEVEL and not args.all):
        print("Sending mail...")
        with open(ALERTS["content"], "r") as alert_content_fp:
            alert_template = alert_content_fp.read()

        alert_content = to_bytes(alert_template % (alert_manager.alert_level, html))

        with open(ALERTS["subject"], "r") as alert_subject_fp:
            alert_subject = alert_subject_fp.read()

        alert_subject = to_bytes(alert_subject % os.uname()[1])

        mail_command = MailCommand(alert_subject, ALERTS["recipient"])
        command_output = mail_command.execute(alert_content)

        if command_output is None:
            print("Error occured while sending mail!")
        else:
            print("Mail sent!")
    else:
        print("No mail to send.")
