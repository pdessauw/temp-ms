from collections import OrderedDict
from os.path import dirname, join

from library.commands.nvidia import NvidiaSmiCommand
from library.commands.sensors import SensorsCommand

ROOT_DIR = dirname(__file__)

DATA_FOLDER = join(ROOT_DIR, "data")

COMMANDS = [
    SensorsCommand,
    NvidiaSmiCommand
]

# How far to look back in the
ALERT_TIMEFRAME_MINUTES = 5

# Number of alert to trigger sending an email
ALERTS_NB_MAIL_TRIGGER = 5

# Difference from baseline level where a mail should be sent
WARNING_LEVELS = OrderedDict({
    "CRIT": [1.30, "red"],
    "HIGH": [1.15, "orange"],
    "WARM": [1.10, "yellow"]
})

# Default alerting level names
DEFAULT_LEVEL = "NORM"
FAIL_LEVEL = "FAIL"

# Default alerting file
ALERTS = {
    "recipient": "fist.last@mail.ext",
    "subject": join(ROOT_DIR, "mail/headers.txt"),
    "content": join(ROOT_DIR, "mail/content.html"),
}
