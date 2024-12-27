import pandas as pd
import pytest
import requests
import strawberry
import uvicorn
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter

from db.utils import insert_sample_data


@pytest.fixture(autouse=True)
def sample_data(neomodel_db):
    """Fixture for inserting sample data into the database."""
    insert_sample_data(neomodel_db)
    yield


@pytest.fixture(scope="module")
def schema(neomodel_db):
    """Fixture for creating a Person strawberry schema."""

    @strawberry.type
    class Person:
        name: str
        age: int

    @strawberry.type
    class Query:
        @strawberry.field
        def people(self, info: strawberry.types.Info) -> list[Person]:
            result = neomodel_db.cypher_query("MATCH (n:Person) RETURN n")
            people = [
                Person(name=record[0]["name"], age=record[0]["age"])
                for record in result[0]
            ]
            return people

    yield strawberry.Schema(query=Query)


@pytest.fixture(scope="module")
def app(schema):
    """Fixture for creating a FastAPI app with a GraphQL endpoint."""

    def create_app():
        app = FastAPI()
        graphql_app = GraphQLRouter(schema)
        app.include_router(
            graphql_app,
            prefix="/graphql",
        )
        return app

    yield create_app()


@pytest.fixture(scope="module")
def test_app(app):
    """Fixture for running the FastAPI app with Uvicorn."""
    config = uvicorn.Config(app, host="127.0.0.1", port=8000, log_level="info", ws="websockets")
    server = uvicorn.Server(config)
    yield server
    server.should_exit = True


def test_insert_sample_data(neomodel_db):
    """
    Test the insert_sample_data function.
    """
    # Query to verify the inserted data
    result = neomodel_db.cypher_query("MATCH (n:Person) RETURN n")
    # Convert the result to a pandas DataFrame
    df = pd.DataFrame([dict(record[0]) for record in result[0]])

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
    result = neomodel_db.cypher_query("MATCH (a)-[r:FRIEND]->(b) RETURN a, b")
    assert len(result[0]) == 3, f"Expected 3 relationships, but got {len(result[0])}."


def test_graphql_endpoint(test_app):
    """
    Test the GraphQL endpoint for fetching people data.
    """

    query = """
    query {
        people {
            name
            age
        }
    }
    """

    # Start the server
    import threading

    server_thread = threading.Thread(target=test_app.run, daemon=True)
    server_thread.start()

    import time

    # Give the server some time to start
    time.sleep(2)

    # Send a request to the GraphQL endpoint
    response = requests.post(
        "http://127.0.0.1:8000/graphql", json={"query": query}, timeout=10
    )

    # Assert that the response status code is 200
    assert (
        response.status_code == 200
    ), f"Expected status code 200, but got {response.status_code}"

    # Parse the JSON response
    data = response.json()

    # Assert that the 'data' key is present in the response
    assert "data" in data, "The 'data' key is missing in the response."

    # Assert that the 'people' key is present in the response data
    assert "people" in data["data"], "The 'people' key is missing in the response data."

    # Assert that the 'people' list is not empty
    people = data["data"]["people"]
    assert len(people) > 0, "The 'people' list is empty."

    # Assert that each person has 'name' and 'age' fields
    for person in people:
        assert "name" in person, "Missing 'name' field in person data."
        assert "age" in person, "Missing 'age' field in person data."
        assert (
            isinstance(person["name"], str) and person["name"]
        ), "Invalid 'name' value."
        assert isinstance(person["age"], int), "Invalid 'age' value."
