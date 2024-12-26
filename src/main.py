import os

import pandas as pd
from IPython.display import display
from neo4j import GraphDatabase


class Neo4jConnection:
    """A simple class to manage connections to a Neo4j database."""

    def __init__(self, uri, user, password):
        self._driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        """Close the connection to the database."""
        self._driver.close()

    def query(self, query, parameters=None):
        """Execute a Cypher query and return the result."""
        with self._driver.session() as session:
            result = session.run(query, parameters)
            return list(result)


if __name__ == "__main__":
    uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    user = os.getenv("NEO4J_USER", "neo4j")
    password = os.getenv("NEO4J_PASSWORD", "password")

    conn = Neo4jConnection(uri, user, password)

    try:
        # Delete all nodes and relationships in the database
        conn.query("MATCH (n) DETACH DELETE n")
        # Insert sample nodes and relationships
        conn.query("""
        CREATE (a:Person {name: 'Alice', age: 30})
        CREATE (b:Person {name: 'Bob', age: 24})
        CREATE (c:Person {name: 'Carol', age: 29})
        CREATE (a)-[:FRIEND]->(b)
        CREATE (b)-[:FRIEND]->(c)
        CREATE (c)-[:FRIEND]->(a)
        """)

        # Query to verify the inserted data
        result = conn.query("MATCH (n) RETURN n LIMIT 5")
        # Convert the result to a pandas DataFrame
        df = pd.DataFrame([dict(record["n"]) for record in result])
        display(df)

    finally:
        conn.close()
