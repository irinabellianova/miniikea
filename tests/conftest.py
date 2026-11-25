import pytest
from ssh.SshConnect import SshConnect
from data.machines import MACHINES
from mappers.LinuxMapper import LinuxMapper

def _make_node(m):
    ssh = SshConnect(
        m["host"], m["username"], m.get("password"),
        key_filename=m.get("key_filename"),
    )
    ssh.connect()
    return ssh


@pytest.fixture(params=MACHINES)
def nodes(request):
    ssh = _make_node(request.param)
    yield LinuxMapper(ssh)
    ssh.close()


@pytest.fixture
def node_0():
    m = MACHINES[0]
    ssh = _make_node(m)
    yield LinuxMapper(ssh)
    ssh.close()