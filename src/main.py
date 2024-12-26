import argparse
import os
import sys

import pandas as pd
from dotenv import load_dotenv
from IPython.display import display

from db.neo4j_connection import Neo4jConnection, insert_sample_data


def parse_arguments() -> argparse.Namespace:
    """Set up argument parser"""
    parser = argparse.ArgumentParser(description="Neo4j database connection parameters")
    parser.add_argument(
        "--uri",
        type=str,
        help="URI for the Neo4j database",
        default=os.getenv("NEO4J_URI"),
    )
    parser.add_argument(
        "--user",
        type=str,
        help="Username for the Neo4j database",
        default=os.getenv("NEO4J_USER"),
    )
    parser.add_argument(
        "--password",
        type=str,
        help="Password for the Neo4j database",
        default=os.getenv("NEO4J_PASSWORD"),
    )

    # Parse arguments
    args = parser.parse_args()
    if not all([args.uri, args.user, args.password]):
        parser.error("Missing required arguments")
        sys.exit(parser.print_usage())
    return args


if __name__ == "__main__":
    load_dotenv()
    if not hasattr(__builtins__, "__IPYTHON__"):
        args = parse_arguments()
    else:
        args = argparse.Namespace(
            uri=os.getenv("NEO4J_URI"),
            user=os.getenv("NEO4J_USER"),
            password=os.getenv("NEO4J_PASSWORD"),
        )

    conn = Neo4jConnection(**vars(args))

    try:
        # Insert sample data
        insert_sample_data(conn)

        # Query to verify the inserted data
        result = conn.query("MATCH (n) RETURN n LIMIT 5")
        # Convert the result to a pandas DataFrame
        df = pd.DataFrame([dict(record["n"]) for record in result])
        display(df)

    finally:
        if not hasattr(__builtins__, "__IPYTHON__"):
            conn.close()
