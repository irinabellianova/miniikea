import pytest
from ssh.SshConnect import SshConnect
from data.machines import MACHINES


@pytest.fixture(params=MACHINES)
def node(request):
    host = request.param["host"]
    username = request.param["username"]
    password = request.param["password"]

    ssh = SshConnect(host, username, password)
    ssh.connect()
    yield ssh
    ssh.close()