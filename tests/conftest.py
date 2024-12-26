import os

import pytest
from dotenv import load_dotenv

from db.neo4j_connection import Neo4jConnection


@pytest.fixture
def neo4j_connection():
    """Fixture for creating a Neo4j connection."""
    assert load_dotenv()
    uri = os.getenv("NEO4J_URI")
    user = os.getenv("NEO4J_USER")
    password = os.getenv("NEO4J_PASSWORD")

    conn = Neo4jConnection(uri, user, password)
    yield conn
    conn.close()
