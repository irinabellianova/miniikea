from mappers.files import Files
from mappers.disks import Disks
from mappers.checks import Checks
from mappers.base import LinuxBase

class LinuxMapper:
    def __init__(self, ssh):
        self._base = LinuxBase(ssh)
        self.files = Files(ssh)
        self.disks = Disks(ssh)
        self.checks = Checks(ssh)

    def command(self, command, timeout=30):
        return self._base.exec(command, timeout=timeout)