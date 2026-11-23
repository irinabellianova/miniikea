import pytest

from ssh.SshConnect import SshConnect
from data.machines import MACHINES

def test_connect_to_node(node):
    exit_code, out, _ = node.exec("whoami")
    assert exit_code == 0, f"Ошибка: команда whoami вернула код {exit_code}"
    assert out.strip() == "autotest", f"Ошибка: команда whoami вернула неправильное username {out.strip()}"

@pytest.mark.parametrize("machine", MACHINES)
def test_connect_to_node_with_wrong_password(machine):
    ssh = SshConnect(machine["host"], machine["username"], "WRONG_PASSWORD")
    with pytest.raises(ConnectionError) as exc_info:
        ssh.connect(max_attempts=1, delay=0)

    assert "Authentication failed."  in str(exc_info.value.__cause__), f"Ошибка: неправильное сообщение об ошибке {exc_info.value}"