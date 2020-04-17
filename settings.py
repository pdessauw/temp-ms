from os.path import dirname, join

from library.commands.nvidia import NvidiaSmiCommand
from library.commands.sensors import SensorsCommand

ROOT_DIR = dirname(__file__)

DATA_FOLDER = join(ROOT_DIR, "data")

COMMANDS = [
    SensorsCommand,
    NvidiaSmiCommand
]

