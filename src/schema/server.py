from neomodel import IntegerProperty, StringProperty, StructuredNode, UniqueIdProperty


class Server(StructuredNode):
    """A class to represent a server in the database."""

    uid = UniqueIdProperty()
    name = StringProperty(unique_index=True, required=True)
    ip_address = StringProperty(unique_index=True, required=True)
    operating_system = StringProperty()
    cpu_cores = IntegerProperty()
    memory_gb = IntegerProperty()


# Example usage:
# server = Server(name="Server1", ip_address="192.168.1.1", operating_system="Linux", cpu_cores=4, memory_gb=16).save()
