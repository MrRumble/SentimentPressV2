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

@sentiment_route.route('/api/get_sentiments', methods=['GET'])
def get_sentiments():
    # Define your list of news categories
    news_categories = [
        "World", "Politics", "Business", "Science", "Health", "Sports",
        "Entertainment", "Education", "Environment", "UK",
        "Finance", "Music", "Movies", "Television",
        'Technology', "Stock Market", "Cryptocurrency", "Weather", "Crime", "Starmer",
        "War", "Trump", "AI", "Rugby", 'Gaza', 'Israel', 'Russia', 'Ukraine'
    ]
    test_categoreies = ['rugby', 'gaza', 'israel']
    
    # Fetch search terms from the query parameters if necessary (optional)
    search_terms = request.args.get('search_terms', test_categoreies)

    # Initialize database connection and repository
    connection = get_flask_database_connection(current_app)
    search_result_repository = SearchResultRepository(connection)

    # Call the repository method to retrieve the data for the past 30 days
    try:
        # Fetch the data from the database
        results = search_result_repository.get_sentiment_over_time(search_terms)
        print(f"Results from DB: {results}")  # Add a print statement to inspect data

        # Organize the data in a way that can be used for plotting
        organized_data = defaultdict(lambda: defaultdict(list))

        # Iterate through the data and organize it by search_term, date, and summary
        for row in results:
            search_term = row['search_term']
            mean_sentiment = float(row['mean_sentiment'])  # Convert Decimal to float
            date = row['date'].strftime('%Y-%m-%d')
            summary = row['main_headline']
            organized_data[search_term][date].append({
                'sentiment': mean_sentiment, 
                'summary': summary
            })

        print(f"Organized Data: {organized_data}")  # Print organized data for inspection
        
        # Prepare the data for Chart.js in the required format
        final_data = {
            "datasets": []
        }

        for search_term, sentiment_by_date in organized_data.items():
            # Sort the dates
            sorted_dates = sorted(sentiment_by_date.keys())

            # Prepare the dataset
            final_data["datasets"].append({
                "label": search_term,  # Using search_term as the label for each dataset
                "data": [
                    {"x": date, "y": sentiment_by_date[date][0]['sentiment'], "summary": sentiment_by_date[date][0]['summary']}
                    for date in sorted_dates
                ],
                "borderColor": get_random_color(),  # Function for a random color for each line
                "fill": False  # Line graph without filling the area beneath
            })

        print(f"Final Data for Chart: {final_data}")  # Print final data for chart plotting
        return jsonify(final_data), 200

    except Exception as e:
        print(f"Error fetching or processing data: {e}")
        return jsonify({"error": "An error occurred while fetching sentiment data."}), 500

def get_random_color():
    # Helper function to generate a random color for each dataset
    return f"rgb({int(255 * random.random())}, {int(255 * random.random())}, {int(255 * random.random())})"
