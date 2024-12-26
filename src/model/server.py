from neomodel import (
    IntegerProperty,
    StringProperty,
    StructuredNode,
    UniqueIdProperty,
)


class Server(StructuredNode):
    """A class to represent a server in the database."""

    uid = UniqueIdProperty()
    name = StringProperty(unique_index=True, required=True)
    ip_address = StringProperty(unique_index=True, required=True)
    operating_system = StringProperty()
    cpu_cores = IntegerProperty()
    memory_gb = IntegerProperty()
