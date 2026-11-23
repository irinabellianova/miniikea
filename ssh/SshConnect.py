import time
import paramiko
import logging

log = logging.getLogger(__name__)

class SshConnect:

    def __init__(self, host, username, password, port=22, timeout=15):
        self.host = host
        self.username = username
        self.password = password
        self.port = port 
        self.timeout = timeout
        self.client = paramiko.SSHClient()

    def connect(self,max_attempts=3, delay=2):
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        attempt = 1
        while True:
            try:
                log.debug("Попытка %s подключиться к %s", attempt, self.host)
                self.client.connect(
                    hostname=self.host,
                    port=self.port,
                    username=self.username,
                    password=self.password,
                    timeout=self.timeout,
                    banner_timeout=self.timeout,
                    auth_timeout=self.timeout
                )
                log.info("Подключение к %s установлено", self.host)
                return self
            except(paramiko.AuthenticationException, paramiko.SSHException, OSError) as exc:
                if attempt >= max_attempts:
                    raise ConnectionError (f"Не удалось подключиться к {self.host}: {exc}") from exc
                log.warning("Ошибка подключения %s, попытка %s/%s: %s", self.host, attempt, max_attempts, exc)
                attempt += 1
                time.sleep(delay)

    def close(self):
        if self.client:
            try:
                self.client.close()
                log.info("Соединение с %s закрыто", self.host)
            except Exception as exc:
                log.warning("Ошибка при закрытии соединения: %s", exc)

    def exec(self, command, timeout=30):
        log.debug("Выполняю: %s", command)
        _, stdout, stderr = self.client.exec_command(command, timeout=timeout)
        out = stdout.read().decode("utf-8", errors="replace")
        err = stderr.read().decode("utf-8", errors="replace")
        exit_code = stdout.channel.recv_exit_status()
        log.info("Команда '%s' -> exit code: %s\nSTDOUT:\n%s\nSTDERR:\n%s",
                 command, exit_code, out.strip(), err.strip())
        return exit_code, out, err
   
    def background_exec(self, command, timeout=30):
        log.debug("Выполняю: %s", command)
        _, stdout, _ = self.client.exec_command(command, timeout=timeout)
        return stdout.channel

    def __enter__(self):
        return self.connect()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        return False