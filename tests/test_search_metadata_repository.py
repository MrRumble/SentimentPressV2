import pytest
from datetime import datetime
from app.models.search_metadata_model import SearchMetadata
from app.repositories.search_metadata_repository import SearchMetadataRepository

def test_create(db_connection):
    db_connection.seed("tests/seeds/search_metadata_test_data.sql")

    search_metadata_repo = SearchMetadataRepository(db_connection)

    new_search_metadata = SearchMetadata(
        user_id=4,
        search_term='new search term'
    )

    search_metadata_repo.create(new_search_metadata)

    found_search_metadata = db_connection.execute("SELECT * FROM search_metadata WHERE search_term = 'new search term'")[0]
    
    assert found_search_metadata['user_id'] == 4
    assert found_search_metadata['search_term'] == 'new search term'

def test_get_todays_top_search_term(db_connection):
    # Seed db
    db_connection.seed("tests/seeds/search_metadata_test_data.sql")

    search_metadata_repo = SearchMetadataRepository(db_connection)

    db_connection.execute("""
        INSERT INTO search_metadata (user_id, search_term, searched_at) VALUES
        (1, 'popular term', NOW()),
        (2, 'popular term', NOW()),
        (3, 'popular term', NOW()),
        (4, 'less popular term', NOW());
    """)

    top_term, count = search_metadata_repo.get_todays_top_search_term()

    assert top_term == 'popular term'
    assert count == 3
