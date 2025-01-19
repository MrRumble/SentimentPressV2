from datetime import datetime
from app.models.search_result_model import SearchResult  # Adjust import based on the actual path


def test_initialisation():
    # Test initialization with no arguments
    search_result = SearchResult()
    assert search_result.search_term is None
    assert search_result.mean_sentiment is None
    assert search_result.positive_article_count is None
    assert search_result.negative_article_count is None
    assert search_result.total_article_count is None
    assert search_result.ratio_positive_vs_negative is None
    assert search_result.main_headline is None
    assert search_result.top_3_articles == []
    assert search_result.bottom_3_articles == []
    assert isinstance(search_result.created_at, str)
    print("test_initialisation passed")


def test_initialisation_with_values():
    # Test initialization with arguments
    created_at = "2025-01-14 10:30:45"
    search_result = SearchResult(
        search_term="climate change",
        mean_sentiment=0.45,
        positive_article_count=5,
        negative_article_count=3,
        total_article_count=8,
        ratio_positive_vs_negative=1.67,
        main_headline="Impact of climate change on polar bears",
        top_3_articles=[{"title": "Article 1"}, {"title": "Article 2"}, {"title": "Article 3"}],
        bottom_3_articles=[{"title": "Article A"}, {"title": "Article B"}, {"title": "Article C"}],
        created_at=created_at
    )

    assert search_result.search_term == "climate change"
    assert search_result.mean_sentiment == 0.45
    assert search_result.positive_article_count == 5
    assert search_result.negative_article_count == 3
    assert search_result.total_article_count == 8
    assert search_result.ratio_positive_vs_negative == 1.67
    assert search_result.main_headline == "Impact of climate change on polar bears"
    assert search_result.top_3_articles == [{"title": "Article 1"}, {"title": "Article 2"}, {"title": "Article 3"}]
    assert search_result.bottom_3_articles == [{"title": "Article A"}, {"title": "Article B"}, {"title": "Article C"}]
    assert search_result.created_at == created_at
    print("test_initialisation_with_values passed")


def test_equality():
    # Test equality comparison
    created_at = "2025-01-14 10:30:45"
    result1 = SearchResult(
        search_term="climate change",
        mean_sentiment=0.45,
        positive_article_count=5,
        negative_article_count=3,
        total_article_count=8,
        ratio_positive_vs_negative=1.67,
        main_headline="Impact of climate change on polar bears",
        top_3_articles=[{"title": "Article 1"}, {"title": "Article 2"}, {"title": "Article 3"}],
        bottom_3_articles=[{"title": "Article A"}, {"title": "Article B"}, {"title": "Article C"}],
        created_at=created_at
    )
    result2 = SearchResult(
        search_term="climate change",
        mean_sentiment=0.45,
        positive_article_count=5,
        negative_article_count=3,
        total_article_count=8,
        ratio_positive_vs_negative=1.67,
        main_headline="Impact of climate change on polar bears",
        top_3_articles=[{"title": "Article 1"}, {"title": "Article 2"}, {"title": "Article 3"}],
        bottom_3_articles=[{"title": "Article A"}, {"title": "Article B"}, {"title": "Article C"}],
        created_at=created_at
    )
    result3 = SearchResult(
        search_term="carbon emissions",
        mean_sentiment=0.30,
        positive_article_count=3,
        negative_article_count=5,
        total_article_count=8,
        ratio_positive_vs_negative=0.6,
        main_headline="Carbon emissions impact",
        top_3_articles=[{"title": "Article X"}, {"title": "Article Y"}, {"title": "Article Z"}],
        bottom_3_articles=[{"title": "Article M"}, {"title": "Article N"}, {"title": "Article O"}],
        created_at="2025-01-14 11:00:00"
    )

    assert result1 == result2
    assert result1 != result3
    print("test_equality passed")


def test_representation():
    # Test string representation
    created_at = "2025-01-14 10:30:45"
    search_result = SearchResult(
        search_term="climate change",
        mean_sentiment=0.45,
        positive_article_count=5,
        negative_article_count=3,
        total_article_count=8,
        ratio_positive_vs_negative=1.67,
        main_headline="Impact of climate change on polar bears",
        top_3_articles=[{"title": "Article 1"}, {"title": "Article 2"}, {"title": "Article 3"}],
        bottom_3_articles=[{"title": "Article A"}, {"title": "Article B"}, {"title": "Article C"}],
        created_at=created_at
    )

    expected_repr = (
        "SearchResult(search_result_id=None, search_term=climate change, mean_sentiment=0.45, "
        "positive_article_count=5, negative_article_count=3, total_article_count=8, "
        "ratio_positive_vs_negative=1.67, main_headline=Impact of climate change on polar bears, "
        "top_3_articles=[{'title': 'Article 1'}, {'title': 'Article 2'}, {'title': 'Article 3'}], "
        "bottom_3_articles=[{'title': 'Article A'}, {'title': 'Article B'}, {'title': 'Article C'}], "
        f"created_at={created_at})"
    )

    assert repr(search_result) == expected_repr
    print("test_representation passed")


def test_to_dict():
    # Test dictionary conversion
    created_at = "2025-01-14 10:30:45"
    search_result = SearchResult(
        search_term="climate change",
        mean_sentiment=0.45,
        positive_article_count=5,
        negative_article_count=3,
        total_article_count=8,
        ratio_positive_vs_negative=1.67,
        main_headline="Impact of climate change on polar bears",
        top_3_articles=[{"title": "Article 1"}, {"title": "Article 2"}, {"title": "Article 3"}],
        bottom_3_articles=[{"title": "Article A"}, {"title": "Article B"}, {"title": "Article C"}],
        created_at=created_at
    )

    expected_dict = {
        "search_result_id": None,
        "search_term": "climate change",
        "mean_sentiment": 0.45,
        "positive_article_count": 5,
        "negative_article_count": 3,
        "total_article_count": 8,
        "ratio_positive_vs_negative": 1.67,
        "main_headline": "Impact of climate change on polar bears",
        "top_3_articles": [{"title": "Article 1"}, {"title": "Article 2"}, {"title": "Article 3"}],
        "bottom_3_articles": [{"title": "Article A"}, {"title": "Article B"}, {"title": "Article C"}],
        "created_at": created_at
    }

    assert search_result.to_dict() == expected_dict
    print("test_to_dict passed")
