import os

import pytest
from dotenv import load_dotenv

from main import Neo4jConnection


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
    neo4j_connection.query("MATCH (n) DETACH DELETE n")
    neo4j_connection.query("""
    CREATE (a:Person {name: 'Alice', age: 30})
    CREATE (b:Person {name: 'Bob', age: 24})
    CREATE (c:Person {name: 'Carol', age: 29})
    CREATE (a)-[:FRIEND]->(b)
    CREATE (b)-[:FRIEND]->(c)
    CREATE (c)-[:FRIEND]->(a)
    """)
    yield

    neo4j_connection.query("MATCH (n) DETACH DELETE n")
