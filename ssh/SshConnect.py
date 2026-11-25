import time
import paramiko
import logging
import os

log = logging.getLogger(__name__)

class SshConnect:

    def __init__(self, host, username, password=None, port=22, timeout=15, key_filename=None):
        self.host = host
        self.username = username
        self.password = password
        self.port = port
        self.timeout = timeout
        self.key_filename = key_filename
        self.client = paramiko.SSHClient()

    def connect(self, max_attempts=3, delay=2):
        log.debug("Попытка подключиться к %s", self.host)
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        attempt = 1
        while True:
            try:
                kwargs = {
                    "hostname": self.host,
                    "port": self.port,
                    "username": self.username,
                    "timeout": self.timeout,
                    "banner_timeout": self.timeout,
                    "auth_timeout": self.timeout,
                }
                if self.key_filename:
                    kwargs["key_filename"] = os.path.expanduser(self.key_filename)
                elif self.password:
                    kwargs["password"] = self.password
                else:
                    kwargs["look_for_keys"] = True
                    kwargs["allow_agent"] = True

                self.client.connect(**kwargs)
                log.info("Подключение к %s установлено", self.host)
                return self
            except (paramiko.AuthenticationException, paramiko.SSHException, OSError) as exc:
                if attempt >= max_attempts:
                    raise ConnectionError(f"Не удалось подключиться к {self.host}: {exc}") from exc
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
        log.info("Выполняю: %s", command)
        _, stdout, _ = self.client.exec_command(command, timeout=timeout)
        return stdout.channel

    def reconnect(self, attempts=30, delay=10, command="whoami"):
        log.info("Переподключение к %s:", self.host)
        for i in range(1, attempts + 1):
            try:
                self.close()
                self.connect(max_attempts=1, delay=0)
                exit_code, _, _ = self.exec(command, timeout=5)
                if exit_code == 0:
                    log.info("Нода %s поднялась после перезагрузки", self.host)
                    return self
            except (ConnectionError, OSError, paramiko.SSHException) as exc:
                log.info("...ждём ноду (%s/%s): %s", i, attempts, exc)
            time.sleep(delay)
        raise ConnectionError(f"Нода {self.host} не поднялась за {attempts * delay} секунд")

    def __enter__(self):
        return self.connect()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        return False