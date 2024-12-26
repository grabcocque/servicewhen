import pandas as pd


def test_neo4j_connection(neo4j_connection):
    """
    Test the Neo4j connection.
    """
    # Query to verify the inserted data
    result = neo4j_connection.query("MATCH (n) RETURN n LIMIT 5")
    # Convert the result to a pandas DataFrame
    df = pd.DataFrame([dict(record["n"]) for record in result])

    # Assert that the DataFrame is not empty
    assert not df.empty, "The DataFrame is empty, no data returned from Neo4j."

    # Assert that the DataFrame has the expected columns
    expected_columns = ["name", "age"]  # Example columns
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
