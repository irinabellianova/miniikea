from mappers.base import LinuxBase
import shlex

class Disks(LinuxBase):
    def lsblk(self):
        return self.exec("lsblk")

    def prepare_multipath(self):
        self.exec("iscsiadm -m node --login")
        self.exec("iscsiadm -m session")
        self.exec("systemctl restart multipathd")
        return self.exec("multipath -ll")

    def get_mpath_device(self, multipath_output):
        for line in multipath_output.splitlines():
            name = line.strip().split()[0]
            if name.startswith("mpath"):
                return name
        raise RuntimeError("В выводе multipath -ll не найден mpath* диск")

    def mkfs(self, fs, dev):
        return self.exec(f"mkfs.{fs} {shlex.quote(dev)}")

    def mount(self, src, point):
        return self.exec(f"mount {shlex.quote(src)} {shlex.quote(point)}")

    def umount(self, point):
        return self.exec(f"umount {shlex.quote(point)}")