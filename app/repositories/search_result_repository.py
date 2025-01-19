from app.models.search_result_model import SearchResult
import json
from datetime import date

class SearchResultRepository:
    def __init__(self, connection):
        self._connection = connection

    def create(self, search_result):
        query = """
            INSERT INTO search_results (search_term, mean_sentiment, positive_article_count, 
                                       negative_article_count, total_article_count, 
                                       ratio_positive_vs_negative, main_headline, 
                                       top_3_articles, bottom_3_articles, created_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING search_result_id
        """
        params = (
            search_result.search_term,
            search_result.mean_sentiment,
            search_result.positive_article_count,
            search_result.negative_article_count,
            search_result.total_article_count,
            search_result.ratio_positive_vs_negative,
            search_result.main_headline,
            json.dumps(search_result.top_3_articles),
            json.dumps(search_result.bottom_3_articles),
            search_result.created_at
        )
        result = self._connection.execute(query, params)
        search_result.search_result_id = result[0]['search_result_id']
        return search_result

    def find(self, search_result_id):
        query = 'SELECT * FROM search_results WHERE search_result_id = %s'
        rows = self._connection.execute(query, [search_result_id])
        if not rows:
            raise ValueError("SearchResult not found")
        row = rows[0]
        return SearchResult(
            search_result_id=row['search_result_id'],
            search_term=row['search_term'],
            mean_sentiment=row['mean_sentiment'],
            positive_article_count=row['positive_article_count'],
            negative_article_count=row['negative_article_count'],
            total_article_count=row['total_article_count'],
            ratio_positive_vs_negative=row['ratio_positive_vs_negative'],
            main_headline=row['main_headline'],
            top_3_articles=row['top_3_articles'],
            bottom_3_articles=row['bottom_3_articles'],
            created_at=row['created_at']
        )

    def get_query_result_if_it_exists_today(self, query):
        today = date.today().strftime('%Y-%m-%d')

        query_str = """
                SELECT *
                FROM search_results
                WHERE search_term = %s AND created_at::date = %s
            """
            
        rows = self._connection.execute(query_str, [query.lower().strip(), today])
        if rows:
            row = rows[0]
            return SearchResult(
                search_result_id=row['search_result_id'],
                search_term=row['search_term'],
                mean_sentiment=row['mean_sentiment'],
                positive_article_count=row['positive_article_count'],
                negative_article_count=row['negative_article_count'],
                total_article_count=row['total_article_count'],
                ratio_positive_vs_negative=row['ratio_positive_vs_negative'],
                main_headline=row['main_headline'],
                top_3_articles=row['top_3_articles'],
                bottom_3_articles=row['bottom_3_articles'],
                created_at=row['created_at']
            )
        else:
            return None

