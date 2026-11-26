import os
import pytest
from ssh.SshConnect import SshConnect
from data.machines import MACHINES
from mappers.LinuxMapper import LinuxMapper

def pytest_addoption(parser):
    parser.addoption(
        "--disk",
        action="store_true",
        default=False,
        help="Флаг: выполнять диск-шаги",
    )

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

@pytest.fixture
def node_1():
    m = MACHINES[1]
    ssh = _make_node(m)
    yield LinuxMapper(ssh)
    ssh.close()

@pytest.fixture
def initiator():
    m = MACHINES[2]
    ssh = _make_node(m)
    yield LinuxMapper(ssh)
    ssh.close()

@pytest.fixture
def disk(request):
    cli_disk = request.config.getoption("--disk")
    env_disk = os.environ.get("MINIIKEA_DISK")
    return bool(cli_disk or env_disk)