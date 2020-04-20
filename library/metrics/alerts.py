from datetime import datetime, timedelta
from os.path import join

import pandas as pd

from library.metrics import DataFileStore
from library.metrics.baseline import BaselineMetrics
from settings import DATA_FOLDER, ALERT_TIMEFRAME_MINUTES, WARNING_LEVELS, DEFAULT_LEVEL, FAIL_LEVEL


class AlertManager(DataFileStore):
    def __init__(self, data_files):
        self.data_files = data_files
        self.alert_level = DEFAULT_LEVEL

        super().__init__(join(DATA_FOLDER, "alert_man.bin"))

    def analyze(self, timeframe=ALERT_TIMEFRAME_MINUTES):
        updated_data = list()

        date_now = datetime.now()
        date_min = date_now - timedelta(minutes=timeframe)

        for data_filepath in self.data_files:
            csv_metrics = BaselineMetrics(data_filepath)
            csv_dataframe = pd.read_csv(data_filepath)
            csv_dataframe["date"] = pd.to_datetime(csv_dataframe["date"])

            csv_current_dataframe = csv_dataframe[csv_dataframe["date"] > date_min]

            columns = [column for column in csv_dataframe.columns
                       if column in csv_metrics.get_metric_names()]

            for column in columns:
                metric_full_name = "%s.%s" % (csv_metrics.prefix, column)
                metric_baseline = csv_metrics.get_metric(column)

                abnormal_level = metric_baseline * list(WARNING_LEVELS.values())[-1][0]
                total_alerts = csv_dataframe[
                    csv_dataframe[column] > abnormal_level
                ].shape[0]
                current_alerts = 0
                alert_level = DEFAULT_LEVEL

                for warning_level, warning_value in WARNING_LEVELS.items():
                    if csv_current_dataframe.shape[0] == 0:  # No up-to-date value available
                        alert_level = FAIL_LEVEL
                        self.alert_level = alert_level
                        break

                    limit_level = metric_baseline * warning_value[0]
                    warning_dataframe = csv_current_dataframe[
                        csv_current_dataframe[column] > limit_level
                    ]
                    current_alerts = warning_dataframe.shape[0]

                    if current_alerts > 0:  # If we have values over the warning size
                        alert_level = warning_level
                        if self.alert_level == DEFAULT_LEVEL:
                            self.alert_level = alert_level
                        break

                updated_data.append([
                    metric_full_name,
                    alert_level,
                    total_alerts - current_alerts,  # Past alerts
                    current_alerts,
                    metric_baseline,
                    csv_dataframe[column].max(),  # Max. past value
                    csv_current_dataframe[column].max(),  # Max. current value
                    csv_dataframe[column].iat[-1]  # Last recorded value
                ])

        self._save_data(updated_data)

    def list(self):
        headers = [[
            "name", "alert_level", "past_alerts", "current_alerts", "base_line", "past_max",
            "current_max", "last_recorded"
        ]]
        return headers + self._load_data()

    def to_html(self, all_data=False):
        row_template = "<tr>%s</tr>"
        row_styled_template = "<tr style='background-color:%s'>%s</tr>"
        header_template = "<th>%s</th>"
        column_template = "<td>%s</td>"

        headers_data = ""
        rows_data = ""

        list_data = self.list()

        if len(list_data) == 1:
            return None

        for header_data in list_data[0]:
            headers_data += header_template % header_data

        headers = row_template % headers_data

        for rows in list_data[1:]:
            if rows[1] == DEFAULT_LEVEL and all_data:
                row_html = ''.join([column_template % row_data for row_data in rows])
                rows_data += row_template % row_html
            elif rows[1] != DEFAULT_LEVEL and rows[1] != FAIL_LEVEL:
                row_html = ''.join([column_template % row_data for row_data in rows])
                rows_data += row_styled_template % (WARNING_LEVELS[rows[1]][1], row_html)
            elif rows[1] == FAIL_LEVEL:
                row_html = ''.join([column_template % row_data for row_data in rows])
                rows_data += row_styled_template % ("lightgrey", row_html)

        return "<table border='1'>%s%s</table>" % (headers, rows_data)
