from mappers.base import LinuxBase

class Checks(LinuxBase):
    def md5sum(self, path):
        return self.exec(f"md5sum {path}")