from library.commands import AbstractCommand
import re


class SensorsCommand(AbstractCommand):
    def __init__(self):
        super().__init__(["sensors"])

    def parse_output(self):
        categories = list()
        output_categories = [
            raw_category.split("\n") for raw_category in self.output.split("\n\n")
        ][:-1]

        for output_category in output_categories:
            category = {
                "title": output_category[0].replace(" ", "_").lower()
            }

            for line in output_category[2:]:
                line_items = re.sub(r"^([^:]+:) +\+?([0-9.]+).*$", r"\g<1>\g<2>",
                                    line.strip()).split(":")
                category[
                    re.sub(r"[^a-z0-9]", "_", line_items[0].lower())
                ] = line_items[1]

            categories.append(category)

        return categories
