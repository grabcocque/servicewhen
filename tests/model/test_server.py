import pytest

from model.server import Server


@pytest.fixture(autouse=True)
def clear_database(neomodel_db):
    """Fixture to clear the database before each test."""
    neomodel_db.cypher_query("MATCH (n) DETACH DELETE n")
    yield


def test_create_server():
    """Test creating a Server node."""
    server = Server(
        name="Server1",
        ip_address="192.168.1.1",
        operating_system="Linux",
        cpu_cores=4,
        memory_gb=16,
    ).save()

    assert server.uid is not None, "Server UID should not be None."
    assert server.name == "Server1", "Server name does not match."
    assert server.ip_address == "192.168.1.1", "Server IP address does not match."
    assert server.operating_system == "Linux", "Server operating system does not match."
    assert server.cpu_cores == 4, "Server CPU cores do not match."
    assert server.memory_gb == 16, "Server memory does not match."


def test_unique_constraints(neomodel_db):
    """Test unique constraints on name and ip_address."""
    from neomodel import install_labels

    install_labels(Server)
    Server(name="Server1", ip_address="192.168.1.1").save()

    with pytest.raises(ValueError):
        Server(name="Server1", ip_address="192.168.1.2").save()

    with pytest.raises(ValueError):
        Server(name="Server2", ip_address="192.168.1.1").save()


def test_optional_properties():
    """Test creating a Server node with optional properties."""
    server = Server(name="Server2", ip_address="192.168.1.2").save()

    assert server.operating_system is None, "Operating system should be None."
    assert server.cpu_cores is None, "CPU cores should be None."
    assert server.memory_gb is None, "Memory should be None."
