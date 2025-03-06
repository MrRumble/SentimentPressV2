
import torch
import pandas as pd
from transformers import pipeline
from concurrent.futures import ThreadPoolExecutor

class ArticleSummariser:
    def __init__(self, model_name="sshleifer/distilbart-cnn-12-6"):
        self.device = 0 if torch.cuda.is_available() else -1  # Use GPU if available
        self.summarizer = pipeline("summarization", model=model_name, device=self.device)

    def summarise_text(self, text: str, max_length: int = 150, min_length: int = 50) -> str:
        """ Summarizes a given text using the loaded Hugging Face model. """
        summary = self.summarizer(text, max_length=max_length, min_length=min_length, do_sample=False)
        return summary[0]['summary_text']

    def summarise_headlines(self, df: pd.DataFrame) -> str:
        """ Summarizes a large number of headlines by processing them in chunks. """
        max_chunk_size = 1024  # Hugging Face models have a token limit (approx. 700 words)
        
        # Split headlines into manageable chunks
        headlines = df['Title'].apply(lambda x: x.strip())  # Preprocessing headlines
        chunks = [headlines[i:i + 10] for i in range(0, len(headlines), 10)]  # Batch chunking
        summaries = []

        # Use ThreadPoolExecutor to process chunks concurrently
        with ThreadPoolExecutor() as executor:
            results = executor.map(self.summarise_text_batch, chunks)
            for result in results:
                summaries.append(result)

        # Combine chunk summaries and generate a final summary
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
