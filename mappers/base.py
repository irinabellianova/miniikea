import time 
import logging 

log = logging.getLogger(__name__)

class LinuxBase:
    def __init__(self, ssh):
        self.ssh = ssh

    def exec(self, command, timeout=30):
        log.info("Команда: %s", command)
        start = time.monotonic()
        exit_code, out, err = self.ssh.exec(command, timeout=timeout)
        elapsed = time.monotonic() - start
        log.info("exit_code=%s, время=%.2f сек\nSTDOUT:\n%s\nSTDERR:\n%s", exit_code, elapsed, out.strip(), err.strip())
        return exit_code, out, err