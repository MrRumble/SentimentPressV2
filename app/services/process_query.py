from datetime import datetime
from app.models.search_result_model import SearchResult
from app.services.sentiment_analyser import SentimentAnalyser
from app.services.news_processor import NewsProcessor
from app.services.article_summariser import ArticleSummariser
"""
ONLY CACHE IF SUCCESFUL RETURN FROM HUGGING FACE
"""

class QueryProcessor:
    def __init__(self):
        self.processor = NewsProcessor()
        self.analyser = SentimentAnalyser()
        self.summariser = ArticleSummariser()

    def process_query(self, query):
        query = query.lower().strip()

        df_sorted = self.processor.fetch_and_process_query(query, 100)
        if df_sorted is None or df_sorted.empty:
            return {"message": f"No articles to process for query: {query}"}, None

        mean_sentiment = self.analyser.calculate_average_sentiment(df_sorted)
        positive_count = self.analyser.calculate_positive_sentiment_count(df_sorted)
        negative_count = self.analyser.calculate_negative_sentiment_count(df_sorted)
        ratio = self.analyser.calculate_sentiment_ratio(positive_count, negative_count)

        df_summarised = self.summariser.summarise_headlines(df_sorted)

        top3 = self.processor.top_three_articles(df_sorted)
        bottom3 = self.processor.bottom_three_articles(df_sorted)
        total_articles = len(df_sorted)

        query_info_front_end = {
            "total_articles": total_articles,
            "positive_count": positive_count,
            "negative_count": negative_count,
            "mean_sentiment": mean_sentiment,
            'summary': df_summarised
        }

        response_data_front_end = {
            'query_info': query_info_front_end,
            'top3': top3,
            'bottom3': bottom3
        }

        search_result = SearchResult(
            search_term=query,
            mean_sentiment=mean_sentiment,
            positive_article_count=positive_count,
            negative_article_count=negative_count,
            total_article_count=total_articles,
            ratio_positive_vs_negative=ratio,
            main_headline=df_summarised,
            top_3_articles=top3,
            bottom_3_articles=bottom3,
        )

        return response_data_front_end, search_result
