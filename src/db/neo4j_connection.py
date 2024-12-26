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


def insert_sample_data(conn):
    """Insert sample data into the Neo4j database."""
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
