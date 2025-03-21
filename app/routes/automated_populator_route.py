from flask import jsonify, current_app, request
from app.services.process_query import QueryProcessor
from flask_cors import CORS
from flask import Blueprint
import time
from dotenv import load_dotenv
import os
import requests

populate_route = Blueprint('populate_route', __name__)
CORS(populate_route)

news_categories = [
    "Politics", "Business", "Science", "Sports",
    "Entertainment", "Education", "Environment", "UK", 
    "Finance", "Music", "Movies",
    'technology', "stock market", "Weather", "Crime", "Starmer",
    "war", "Trump", "AI", "Rugby", 'Gaza', 'Israel', 'Russia', 'Ukraine'
]

@populate_route.route('/populate_database', methods=['POST'])
def populate_database():
    load_dotenv()
    processor = QueryProcessor()
    
    BASE_URL = os.getenv('BASE_URL', 'http://18.169.54.136:5002')

    api_key = request.headers.get('X-API-KEY')
    if api_key != os.getenv('POPULATE_KEY'):
        return jsonify({"error": "Unauthorized"}), 401

    try:
        start_time = time.time() 
        print("Populating the database with predefined news categories...")

        for category in news_categories:
            print(f"Populating: {category}...")
            response_data_front_end, search_result = processor.process_query(category)

            if search_result is None or "Error:" in response_data_front_end.get("query_info", {}).get("summary", ""):
                print(f"Skipping '{category}' due to summarization failure.")
                continue

            data = {
                "search_term": category.lower(),
                "mean_sentiment": search_result.mean_sentiment,
                "positive_article_count": search_result.positive_article_count,
                "negative_article_count": search_result.negative_article_count,
                "total_article_count": search_result.total_article_count,
                "ratio_positive_vs_negative": search_result.ratio_positive_vs_negative,
                "main_headline": search_result.main_headline,
                "top_3_articles": search_result.top_3_articles,
                "bottom_3_articles": search_result.bottom_3_articles
            }

            response = requests.post(f'{BASE_URL}/insert_data', json=data)

            if response.status_code != 200:
                print(f"Failed to insert data for category '{category}'. Response: {response.text}")
                continue

            print(f"Data for category '{category}' inserted successfully.")

        end_time = time.time()
        duration = end_time - start_time
        return jsonify({"message": f"Database population completed successfully in {duration} seconds"}), 200

    except Exception as e:
        print(f"Error during population: {str(e)}")
        return jsonify({"error": str(e)}), 500
