from app.repositories.search_result_repository import SearchResultRepository
from app.models.search_result_model import SearchResult


def test_create(db_connection):
    db_connection.seed("tests/seeds/search_results_test_data.sql")

    search_result_repo = SearchResultRepository(db_connection)

    new_search_result = SearchResult(
        search_term='New Search Term',
        mean_sentiment=0.75,
        positive_article_count=5,
        negative_article_count=3,
        total_article_count=10,
        ratio_positive_vs_negative=1.67,
        main_headline='Main Headline for Search Result',
        top_3_articles=[
            {"title": "Article 1", "url": "https://example.com/1"},
            {"title": "Article 2", "url": "https://example.com/2"},
            {"title": "Article 3", "url": "https://example.com/3"}
        ],
        bottom_3_articles=[
            {"title": "Article 1", "url": "https://example.com/1"},
            {"title": "Article 2", "url": "https://example.com/2"},
            {"title": "Article 3", "url": "https://example.com/3"}
        ],
    )

    search_result_repo.create(new_search_result)

    found_search_result = search_result_repo.find(4)

    assert found_search_result.search_result_id == 4
    assert found_search_result.search_term == 'New Search Term'
    assert found_search_result.mean_sentiment == 0.75
    assert found_search_result.positive_article_count == 5
    assert found_search_result.negative_article_count == 3
    assert found_search_result.total_article_count == 10
    assert float(found_search_result.ratio_positive_vs_negative) == 1.67
    assert found_search_result.main_headline == 'Main Headline for Search Result'
    assert found_search_result.top_3_articles == [
        {"title": "Article 1", "url": "https://example.com/1"},
        {"title": "Article 2", "url": "https://example.com/2"},
        {"title": "Article 3", "url": "https://example.com/3"}
    ]
    assert found_search_result.bottom_3_articles == [
        {"title": "Article 1", "url": "https://example.com/1"},
        {"title": "Article 2", "url": "https://example.com/2"},
        {"title": "Article 3", "url": "https://example.com/3"}
    ]


def test_find(db_connection):

    db_connection.seed("tests/seeds/search_results_test_data.sql")

    search_result_repo = SearchResultRepository(db_connection)

    search_result = search_result_repo.find(1)

    assert search_result.search_result_id == 1
    assert search_result.search_term == 'test search term 1'
    assert float(search_result.mean_sentiment) == 0.7
    assert search_result.positive_article_count == 5
    assert search_result.negative_article_count == 3
    assert search_result.total_article_count == 10
    assert float(search_result.ratio_positive_vs_negative) == 1.67
    assert search_result.main_headline == 'Main Headline 1'
    assert search_result.top_3_articles == [
        {"title": "Top Article 1", "url": "https://example.com/1"},
        {"title": "Top Article 2", "url": "https://example.com/2"},
        {"title": "Top Article 3", "url": "https://example.com/3"}
    ]
    assert search_result.bottom_3_articles == [
        {"title": "Bottom Article 1", "url": "https://example.com/11"},
        {"title": "Bottom Article 2", "url": "https://example.com/12"},
        {"title": "Bottom Article 3", "url": "https://example.com/13"}
    ]


def test_query_result_returns_if_exists_for_that_day(db_connection):

    db_connection.seed("tests/seeds/search_results_test_data.sql")
    search_result_repo = SearchResultRepository(db_connection)
    assert search_result_repo.get_query_result_if_it_exists_today('test search term 1') is not None
    
def test_query_result_returns_none_if_does_not_exist_for_that_day(db_connection):
    db_connection.seed("tests/seeds/search_results_test_data.sql")
    search_result_repo = SearchResultRepository(db_connection)
    assert search_result_repo.get_query_result_if_it_exists_today('not searched') is None

def test_get_highest_sentiment_today(db_connection):
    db_connection.seed("tests/seeds/search_results_test_data.sql")
    search_result_repo = SearchResultRepository(db_connection)
    highest_sentiment_result = search_result_repo.get_highest_sentiment_today()

    assert highest_sentiment_result is not None
    assert float(highest_sentiment_result.mean_sentiment) == 0.90

def test_get_lowest_sentiment_today(db_connection):
    db_connection.seed("tests/seeds/search_results_test_data.sql")
    
    search_result_repo = SearchResultRepository(db_connection)
    lowest_sentiment_result = search_result_repo.get_lowest_sentiment_today()
    
    assert lowest_sentiment_result is not None
    assert float(lowest_sentiment_result.mean_sentiment) == -0.30