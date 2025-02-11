from flask import Blueprint, jsonify, current_app
from flask_cors import CORS
from app.utils.database import get_flask_database_connection
from app.repositories.search_result_repository import SearchResultRepository

landing_route = Blueprint('landing_routes', __name__)
CORS(landing_route)

@landing_route.route('/api/get-headlines', methods=['GET'])
def get_random_headlines():
    """
    API endpoint to fetch random search terms and their main headlines for the current day.
    """
    connection = get_flask_database_connection(current_app)
    repository = SearchResultRepository(connection)

    try:
        headlines = repository.get_queries_and_headlines()
        return jsonify({"headlines": headlines}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
