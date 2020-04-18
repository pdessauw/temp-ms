from library.commands import AbstractCommand
import re


class SensorsCommand(AbstractCommand):
    def __init__(self):
        super().__init__(["sensors"])

    def parse_output(self):
        categories = list()
        # Split output into categories + remove last empty line
        output_categories = [
            raw_category.split("\n") for raw_category in self.output.split("\n\n")
        ][:-1]

        for output_category in output_categories:
            category = {
                "title": output_category[0].replace(" ", "_").lower()
            }

            # Manage duplicate titles
            duplicate_titles = dict()
            line_items_titles = list()
            line_items_values = list()

            for line in output_category[2:]:
                line_items = re.sub(r"^([^:]+:) +\+?([0-9.]+).*$", r"\g<1>\g<2>",
                                    line.strip()).split(":")
                line_title = re.sub(r"[^a-z0-9]", "_", line_items[0].lower())

                # If a duplicate line_title already exists, increment the counter
                if line_title in duplicate_titles.keys():
                    duplicate_titles[line_title] += 1
                    line_title = "%s_%d" % (line_title, duplicate_titles[line_title])

                # If a line_title already exitst, create the duplicate item
                if line_title in line_items_titles:
                    duplicate_titles[line_title] = 2

                    line_items_index = line_items_titles.index(line_title)
                    line_items_titles[line_items_index] += "_1"
                    line_title += "_2"

                line_items_titles.append(line_title)
                line_items_values.append(line_items[1])

            category.update(dict(zip(line_items_titles, line_items_values)))
            categories.append(category)

        return categories
