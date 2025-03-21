import torch
import pandas as pd
from transformers import pipeline
from concurrent.futures import ThreadPoolExecutor
import os

class ArticleSummariser:
    def __init__(self, model_dir="./models/distilbart-cnn-12-6"):
        self.device = -1
        
        self.model_path = os.path.abspath(model_dir)
        
        if not os.path.exists(self.model_path):
            raise FileNotFoundError(f"Model directory {self.model_path} does not exist.")
        
        self.summarizer = pipeline("summarization", model=self.model_path, device=self.device)

    def summarise_text(self, text: str, max_length: int = 150, min_length: int = 50) -> str:
        """ Summarizes a given text using the loaded Hugging Face model. """
        summary = self.summarizer(text, max_length=max_length, min_length=min_length, do_sample=False)
        return summary[0]['summary_text']

    def summarise_headlines(self, df: pd.DataFrame) -> str:
        """ Summarizes a large number of headlines by processing them in chunks. """
        max_chunk_size = 1024
        
        headlines = df['Title'].apply(lambda x: x.strip())
        chunks = [headlines[i:i + 10] for i in range(0, len(headlines), 10)]
        summaries = []

        with ThreadPoolExecutor() as executor:
            results = executor.map(self.summarise_text_batch, chunks)
            for result in results:
                summaries.append(result)

        combined_summary = ' '.join(summaries)
        if combined_summary:
            try:
                final_summary = self.summarise_text(combined_summary, max_length=150, min_length=50)
                return final_summary
            except Exception as e:
                return f"Error: Final summarization failed: {e}"
        else:
            return "Error: Unable to summarize due to processing failure."

    def summarise_text_batch(self, batch: pd.Series) -> str:
        """Summarizes a batch of text (headlines)."""
        batch_text = '. '.join(batch)
        return self.summarise_text(batch_text, max_length=100, min_length=30)
