import pytest

from ssh.SshConnect import SshConnect
from data.machines import MACHINES

def test_connect_to_node(nodes):
    exit_code, out, _ = nodes.command("tatlin-cli --version")
    assert exit_code == 0, f"Ошибка: команда tatlin-cli --version вернула код {exit_code}"
    assert out.strip() == "tatlin-cli version 4.1.0.v5346", f"Ошибка: команда tatlin-cli --version вернула неправильное значение {out.strip()}"

@pytest.mark.parametrize("machine", [MACHINES[1]])
def test_connect_to_node_with_wrong_password(machine):
    ssh = SshConnect(machine["host"], machine["username"], "WRONG_PASSWORD")
    with pytest.raises(ConnectionError) as exc_info:
        ssh.connect(max_attempts=1, delay=0)

    assert "Authentication failed."  in str(exc_info.value.__cause__), f"Ошибка: неправильное сообщение об ошибке {exc_info.value}"