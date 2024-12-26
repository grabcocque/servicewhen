def insert_sample_data(db):
    """Insert sample data into the Neo4j database."""
    # Delete all nodes and relationships in the database
    db.cypher_query("MATCH (n) DETACH DELETE n")
    # Insert sample nodes and relationships
    db.cypher_query("""
            CREATE (a:Person {name: 'Alice', age: 30})
            CREATE (b:Person {name: 'Bob', age: 24})
            CREATE (c:Person {name: 'Carol', age: 29})
            CREATE (a)-[:FRIEND]->(b)
            CREATE (b)-[:FRIEND]->(c)
            CREATE (c)-[:FRIEND]->(a)
            """)
