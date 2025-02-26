import requests
from dotenv import load_dotenv
import os

class ArticleSummariser:
    def __init__(self):
        load_dotenv()
        self.api_url = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
        self.api_key = os.getenv("HUGGINGFACE_API_KEY")

    def send_to_huggingface(self, combined_text: str, max_length: int = 150, min_length: int = 50) -> str:
        headers = {"Authorization": f"Bearer {self.api_key}"}
        payload = {
            "inputs": combined_text,
            "parameters": {
                "max_length": max_length,
                "min_length": min_length
            }
        }
        response = requests.post(self.api_url, headers=headers, json=payload)

        if response.status_code == 200:
            summary = response.json()
            return summary[0]['summary_text']
        else:
            return f"Error: {response.status_code}, {response.text}"

    def summarise_headlines(self, df) -> str:
        combined_text = '. '.join(df['Title']) + '.'
        max_length = 1024  # Adjust based on the model's token limit
        chunks = [combined_text[i:i + max_length] for i in range(0, len(combined_text), max_length)]

        # Summarize each chunk with reduced length
        summaries = [self.send_to_huggingface(chunk, max_length=100, min_length=30) for chunk in chunks]

        # Combine the individual summaries
        combined_summary = ' '.join(summaries)

        # Further condense the final summary
        final_summary = self.send_to_huggingface(combined_summary, max_length=150, min_length=30)

        return final_summary

