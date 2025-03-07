import os
from transformers import pipeline

"""
This class processes individual articles, 
extracting specified information and analyzing sentiment scores using a Transformer pipeline 
on combined titles and descriptions. 
Note: sentiment analysis is slow; consider a faster model based on our needs. 
With full access to a newsAPI key, particularly access to article content, sentiment scoring accuracy could improve. 
Articles are validated to prevent null results from deleted publications. 
Finally, articles are transformed into a delicious dictionary format, ready for use elsewhere.
"""

# TESTED
class ArticleProcessor:
    _model = None  # Class variable to store the model

    def __init__(self, model_dir="./models/distilbert-base-uncased-finetuned-sst-2-english"):
        self.model_path = os.path.abspath(model_dir)  # Convert to absolute path

        # Check if model directory exists
        if not os.path.exists(self.model_path):
            raise FileNotFoundError(f"Model directory {self.model_path} does not exist.")

        # Load sentiment analysis model once for efficiency
        if ArticleProcessor._model is None:
            ArticleProcessor._model = pipeline(
                "sentiment-analysis", 
                model=self.model_path
            )
        self.sentiment_pipeline = ArticleProcessor._model

    def extract_article_info(self, article):
        """Extracts relevant article information."""
        title = article.get('title')
        description = article.get('description')
        published_at = article.get('publishedAt')
        source = article.get('source', {}).get('name')
        return title, description, published_at, source

    def combine_text(self, title, description):
        """Combines title and description for sentiment analysis."""
        return f"{title}. {description}" if title and description else title or description

    def analyse_sentiment(self, text):
        """Analyzes sentiment of the given text using the loaded model."""
        if text:
            sentiment = self.sentiment_pipeline(text)
            return sentiment[0]['score'] if sentiment[0]['label'] == 'POSITIVE' else -sentiment[0]['score']
        return None

    def validate_article(self, title, description, sentiment_score):
        if sentiment_score != 0 and title is not None and description is not None:
            return '[Removed]' not in title and '[Removed]' not in description
        return False

    def process_article(self, article):
        """Processes an article and returns structured data if valid."""
        title, description, published_at, source = self.extract_article_info(article)
        text = self.combine_text(title, description)
        sentiment_score = self.analyse_sentiment(text)
        if self.validate_article(title, description, sentiment_score):
            return {
                'Published Date': published_at,
                'Title': title,
                'Description': description,
                'Source': source,
                'Sentiment Score': sentiment_score
            }
        return None
