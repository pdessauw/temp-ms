from library.commands import AbstractCommand


class MailCommand(AbstractCommand):
    def __init__(self, subject, recipient):
        super().__init__(["mail", "-s", subject, recipient])

    def parse_output(self):
        return True

