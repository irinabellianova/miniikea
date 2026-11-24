from mappers.base import LinuxBase
import shlex

class Disks(LinuxBase):
    def lsblk(self):
        return self.exec("lsblk")

    def mkfs(self, fs, dev):
        return self.exec(f"mkfs.{fs} {shlex.quote(dev)}")

    def mount(self, src, point):
        return self.exec(f"mount {shlex.quote(src)} {shlex.quote(point)}")

    def umount(self, point):
        return self.exec(f"umount {shlex.quote(point)}")