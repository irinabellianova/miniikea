from mappers.base import LinuxBase
import shlex

class Files(LinuxBase):
    def cat(self, path):
        return self.exec(f"cat {path}")

    def touch(self, path):
        return self.exec(f"touch {path}")

    def pwd(self):
        return self.exec("pwd")

    def echo(self, text, path):
        return self.exec(f"echo {shlex.quote(text)} > {path}")

    def mkdir(self, path):
        return self.exec(f"mkdir -p {path}")

    def cp(self, src, dst):
        return self.exec(f"cp {src} {dst}")