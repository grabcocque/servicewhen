import os

import pytest
from dotenv import load_dotenv
from neomodel import config, db


@pytest.fixture
def neomodel_db():
    """Fixture for creating a Neo4j connection."""
    assert load_dotenv()
    uri = os.getenv("NEO4J_URI")
    user = os.getenv("NEO4J_USER")
    password = os.getenv("NEO4J_PASSWORD")

    config.DATABASE_URL = f"bolt://{user}:{password}@{uri}"

    yield db

    db.close_connection()
