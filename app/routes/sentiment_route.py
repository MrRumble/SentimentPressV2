from flask import jsonify, request, current_app
from app.repositories.search_result_repository import SearchResultRepository
from app.utils.database import get_flask_database_connection
from flask import Blueprint
from flask_cors import CORS
from collections import defaultdict
from decimal import Decimal
import random

sentiment_route = Blueprint('sentiment_route', __name__)
CORS(sentiment_route)


def get_random_color():
    # Helper function to generate a random color for each dataset
    return f"rgb({int(255 * random.random())}, {int(255 * random.random())}, {int(255 * random.random())})"


@sentiment_route.route('/api/get_sentiment', methods=['GET'])
def get_sentiment():
    # Fetch a single search term from query parameters
    search_term = request.args.get('search_term')
    if not search_term:
        return jsonify({"error": "search_term is required"}), 400

    # Initialize database connection and repository
    connection = get_flask_database_connection(current_app)
    search_result_repository = SearchResultRepository(connection)

    # Call the repository method to retrieve the data for the past 30 days
    try:
        # Fetch the data from the database for the given search term
        results = search_result_repository.get_sentiment_over_time(search_term)
        print(f"Results from DB: {results}")  # Add a print statement to inspect data

        # Organize the data in a way that can be used for plotting
        organized_data = defaultdict(list)

        # Iterate through the data and organize it by date and summary
        for row in results:
            mean_sentiment = float(row['mean_sentiment'])  # Convert Decimal to float
            date = row['date'].strftime('%Y-%m-%d')
            summary = row['main_headline']
            organized_data[date].append({
                'sentiment': mean_sentiment, 
                'summary': summary
            })

        print(f"Organized Data: {organized_data}")  # Print organized data for inspection
        
        # Prepare the data for Chart.js in the required format
        final_data = {
            "datasets": [
                {
                    "label": search_term,  # Using search_term as the label for the dataset
                    "data": [
                        {"x": date, "y": organized_data[date][0]['sentiment'], "summary": organized_data[date][0]['summary']}
                        for date in sorted(organized_data.keys())
                    ],
                    "borderColor": get_random_color(),  # Function for a random color for the line
                    "fill": False  # Line graph without filling the area beneath
                }
            ]
        }

        print(f"Final Data for Chart: {final_data}")  # Print final data for chart plotting
        return jsonify(final_data), 200

    except Exception as e:
        print(f"Error fetching or processing data: {e}")
        return jsonify({"error": "An error occurred while fetching sentiment data."}), 500
