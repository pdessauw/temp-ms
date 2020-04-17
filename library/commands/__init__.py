"""
"""
import subprocess
from abc import abstractmethod, ABC
from typing import List


class AbstractCommand(ABC):
    def __init__(self, command_list: List[str]):
        self.is_executed = False
        self.return_code = None
        self.output = None
        self.command = command_list

    def execute(self):
        self.is_executed = True
        try:
            process = subprocess.Popen(
                self.command,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT
            )
            stdout, _ = process.communicate()
            self.return_code = process.returncode
            self.output = stdout.decode("utf-8")
        except Exception:
            self.return_code = -1
        finally:
            if self.has_failed():
                return None

            return self.parse_output()

    def has_failed(self):
        if not self.is_executed:
            raise Exception("Command not executed yet")

        return self.return_code != 0

    @abstractmethod
    def parse_output(self):
        raise NotImplementedError(
            "Method 'parse_output(self)' has not been implemented"
        )


