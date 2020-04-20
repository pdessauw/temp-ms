from library.commands import AbstractCommand
import re


class NvidiaSmiCommand(AbstractCommand):
    def __init__(self):
        super().__init__(["nvidia-smi"])

    def parse_output(self):
        def split_line(line):
            line = line.replace("|", "")
            line = re.sub(r" +", " ", line)
            line = re.sub(r" / [^ ]+ ", " ", line)

            line_items = line.split(" ")

            del line_items[0]  # Empty field
            del line_items[2]  # Performance

            return line_items[:-2]  # Compute Module

        raw_output = [
            raw_category.split("\n") for raw_category in self.output.split("\n\n")
        ][0]

        headers = [
            re.sub(r"[^a-z0-9]", "_", item.lower())
            for item in split_line(raw_output[5])
        ]
        values = [
            float(re.sub(r"[^0-9.]", "", item.lower()))
            for item in split_line(raw_output[8])
        ]

        entry = dict(zip(headers, values))
        entry["title"] = "gpu"

        return [entry]

