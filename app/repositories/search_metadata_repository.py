import json
from app.models.search_metadata_model import SearchMetadata  # Adjust path as needed

class SearchMetadataRepository:
    def __init__(self, connection):
        self._connection = connection

    def create(self, search_metadata):
        query = """
            INSERT INTO search_metadata (user_id, search_term, searched_at)
            VALUES (%s, %s, %s)
            RETURNING search_metadata_id
        """
        params = (
            search_metadata.user_id,
            search_metadata.search_term,
            search_metadata.searched_at
        )
        result = self._connection.execute(query, params)
        search_metadata.search_metadata_id = result[0]['search_metadata_id']
        return search_metadata
