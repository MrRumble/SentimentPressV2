from transformers import pipeline

import os
from dotenv import load_dotenv


class ArticleSummariser:
    def __init__(self):
        load_dotenv()
        self.text_generation_pipeline = pipeline('summarization', model="sshleifer/distilbart-cnn-12-6") # Investigate models
        self.api_key = os.getenv("OPEN_AI_KEY")

    def summarise_top_bottom_articles(self, df, top_n=3, bottom_n=3, max_summary_sentences=6) -> str:
        top_articles = df.nlargest(top_n, 'Sentiment Score')
        bottom_articles = df.nsmallest(bottom_n, 'Sentiment Score')
        combined_text = '. '.join(top_articles['Title'] + '. ' + top_articles['Description']) + '. ' + \
                        '. '.join(bottom_articles['Title'] + '. ' + bottom_articles['Description'])
        summary = self.text_generation_pipeline(combined_text, max_length=200, min_length=30, num_return_sequences=1,
                                                early_stopping=True)
        summarized_text = summary[0]['summary_text']
        summarized_sentences = summarized_text.split('. ')
        if len(summarized_sentences) > max_summary_sentences:
            summarized_text = '. '.join(summarized_sentences[:max_summary_sentences]) + '.'
        return summarized_text

