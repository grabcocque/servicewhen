import pandas as pd
import pytest

from db.neo4j_connection import insert_sample_data


@pytest.fixture(autouse=True)
def sample_data(neo4j_connection):
    """Fixture for inserting sample data into the database."""
    insert_sample_data(neo4j_connection)
    yield


def test_insert_sample_data(neo4j_connection):
    """
    Test the insert_sample_data function.
    """
    # Query to verify the inserted data
    result = neo4j_connection.query("MATCH (n:Person) RETURN n")
    # Convert the result to a pandas DataFrame
    df = pd.DataFrame([dict(record["n"]) for record in result])

    # Assert that the DataFrame is not empty
    assert not df.empty, "The DataFrame is empty, no data returned from Neo4j."

    # Assert that the DataFrame has the expected columns
    expected_columns = ["name", "age"]
    for column in expected_columns:
        assert column in df.columns, f"Missing expected column: {column}"

    # Assert that the DataFrame has the expected number of rows
    expected_row_count = 3
    assert (
        len(df) == expected_row_count
    ), f"Expected {expected_row_count} rows, but got {len(df)}."

    # Assert that the 'age' column contains only integers
    assert (
        df["age"].apply(lambda x: isinstance(x, int)).all()
    ), "The 'age' column contains non-integer values."

    # Assert that the 'name' column contains only non-empty strings
    assert (
        df["name"].apply(lambda x: isinstance(x, str) and x).all()
    ), "The 'name' column contains empty or non-string values."

    # Assert that the relationships are correctly created
    result = neo4j_connection.query("MATCH (a)-[r:FRIEND]->(b) RETURN a, b")
    assert len(result) == 3, f"Expected 3 relationships, but got {len(result)}."
