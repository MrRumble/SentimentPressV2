import os
import torch
import pandas as pd
from transformers import pipeline

class ArticleSummariser:
    def __init__(self, model_name="facebook/bart-large-cnn"):
        # Load summarization model locally
        self.device = 0 if torch.cuda.is_available() else -1  # Use GPU if available
        self.summarizer = pipeline("summarization", model=model_name, device=self.device)

    def summarise_text(self, text: str, max_length: int = 150, min_length: int = 50) -> str:
        """ Summarizes a given text using the loaded Hugging Face model. """
        summary = self.summarizer(text, max_length=max_length, min_length=min_length, do_sample=False)
        return summary[0]['summary_text']

    def summarise_headlines(self, df: pd.DataFrame) -> str:
        """ Summarizes a large number of headlines by processing them in chunks. """
        combined_text = '. '.join(df['Title']) + '.'  # Combine titles into one string
        max_chunk_size = 1024  # Hugging Face models have a token limit (approx. 700 words)
        
        # Split into manageable chunks
        chunks = [combined_text[i:i + max_chunk_size] for i in range(0, len(combined_text), max_chunk_size)]
        summaries = []

        # Summarize each chunk separately
        for chunk in chunks:
            try:
                summary = self.summarise_text(chunk, max_length=100, min_length=30)
                summaries.append(summary)
            except Exception as e:
                print(f"Error summarizing chunk: {e}")

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

