import os

import pytest
from dotenv import load_dotenv

from db.neo4j_connection import Neo4jConnection, insert_sample_data


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


@pytest.fixture
def sampled_data(neo4j_connection):
    """Fixture for inserting sample data into the database."""
    insert_sample_data(neo4j_connection)
    yield
