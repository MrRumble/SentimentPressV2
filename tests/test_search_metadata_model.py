from datetime import datetime
from app.models.search_metadata_model import SearchMetadata  # Adjust import based on actual path

def test_initialisation():
    # Test initialization with no arguments
    search_metadata = SearchMetadata()
    assert search_metadata.search_term is None
    assert search_metadata.user_id is None
    assert isinstance(search_metadata.searched_at, str)
    print("test_initialisation passed")

def test_initialisation_with_values():
    # Test initialization with arguments
    searched_at = "2025-01-14 10:30:45"
    search_metadata = SearchMetadata(
        search_term="blockchain",
        user_id="user_123",
        searched_at=searched_at
    )

    assert search_metadata.search_term == "blockchain"
    assert search_metadata.user_id == "user_123"
    assert search_metadata.searched_at == searched_at
    print("test_initialisation_with_values passed")

def test_equality():
    # Test equality comparison
    searched_at = "2025-01-14 10:30:45"
    metadata1 = SearchMetadata(search_term="AI", user_id="user_001", searched_at=searched_at)
    metadata2 = SearchMetadata(search_term="AI", user_id="user_001", searched_at=searched_at)
    metadata3 = SearchMetadata(search_term="VR", user_id="user_002", searched_at="2025-01-14 11:00:00")

    assert metadata1 == metadata2
    assert metadata1 != metadata3
    print("test_equality passed")

def test_representation():
    # Test string representation
    searched_at = "2025-01-14 10:30:45"
    search_metadata = SearchMetadata(search_term="blockchain", user_id="user_123", searched_at=searched_at)
    
    expected_repr = (
        f"SearchMetadata(search_metadata_id=None, user_id=user_123, search_term=blockchain, searched_at={searched_at})"
    )
    
    assert repr(search_metadata) == expected_repr
    print("test_representation passed")

def test_to_dict():
    # Test dictionary conversion
    searched_at = "2025-01-14 10:30:45"
    search_metadata = SearchMetadata(search_term="blockchain", user_id="user_123", searched_at=searched_at)
    
    expected_dict = {
        "search_metadata_id": None,
        "search_term": "blockchain",
        "user_id": "user_123",
        "searched_at": searched_at
    }
    
    assert search_metadata.to_dict() == expected_dict
    print("test_to_dict passed")
