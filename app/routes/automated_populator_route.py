from flask import jsonify, current_app, request
from app.services.process_query import QueryProcessor
from app.repositories.search_result_repository import SearchResultRepository
from app.utils.database import get_flask_database_connection
from flask_cors import CORS
from flask import Blueprint
import time

populate_route = Blueprint('populate_route', __name__)
CORS(populate_route)

news_categories = [
    "World", "Politics", "Business", "Science", "Health", "Sports",
    "Entertainment", "Lifestyle", "Education", "Environment", "Travel", "Culture", "UK", "Finance",
    "Automotive", "Music", "Movies", "Television", "Social Media",
    "Gaming", "Cryptocurrency", "Weather", "Crime", "Starmer"
    "Military", "Fashion", "Celebrity", "Technology", "Startup", "Trump", "AI"
]

@populate_route.route('/populate_database', methods=['POST'])
def populate_database():

    processor = QueryProcessor()
    connection = get_flask_database_connection(current_app)
    search_result_repository = SearchResultRepository(connection)

    # Ensure only authorised users/services can access this endpoint
    api_key = request.headers.get('X-API-KEY')  # Replace with your auth mechanism
    if api_key != 'admin':
        return jsonify({"error": "Unauthorized"}), 401

    # Run the population logic
    try:
        start_time = time.time()  # Record start time
        print("Populating the database with predefined news categories...")
        for category in news_categories:
            print(f"Populating: {category}...")
            _, search_result = processor.process_query(category)
            search_result_repository.create(search_result)
        end_time = time.time()  # Record end time
        duration = end_time - start_time
        print(f"Database population completed in {duration:.2f} seconds.")
        return jsonify({"message": "Database population completed successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500