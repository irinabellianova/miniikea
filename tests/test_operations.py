import pytest

from ssh.SshConnect import SshConnect

def test_pwd(node):
    exit_code, out, err = node.files.pwd()
    assert exit_code == 0, f"Ошибка: pwd вернул код {exit_code}: {err}"
    assert out.strip().startswith("/"), f"Ошибка: неожиданный путь {out.strip()}"

def test_create_file(node):
    exit_code, out, err = node.files.touch("test_file1")
    exit_code, out, err = node.command("ls -la")
    assert exit_code == 0, f"Ошибка: pwd вернул код {exit_code}: {err}"
    exit_code, out, err = node.files.cat("test_file")
    assert exit_code == 0, f"Ошибка: pwd вернул код {exit_code}: {err}"
    assert out.strip() == "", f"Ошибка: файл не пустой, получено: {out!r}"