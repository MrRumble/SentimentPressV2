from app.services.process_query import QueryProcessor
from flask import Blueprint
from flask_cors import CORS
from flask import Blueprint, jsonify, request, current_app
from app.repositories.search_result_repository import SearchResultRepository    
from app.utils.database import get_flask_database_connection
from app.models import SearchResult

query_route = Blueprint('query_route', __name__)
CORS(query_route)

@query_route.route("/query", methods=["POST"])
def query():
    connection = get_flask_database_connection(current_app)
    processor = QueryProcessor()
    search_result_repository = SearchResultRepository(connection)
    data = request.get_json()
    query_text = data.get('query', '').lower().strip()

    if not query_text:
            return jsonify({"error": "Query text cannot be empty"}), 400

    # Check if a result for the query exists today
    existing_result = search_result_repository.get_query_result_if_it_exists_today(query_text)      
    if existing_result:
        # Transform the existing result into a frontend-friendly format
        response_data_front_end = {
            'query_info': {
                'total_articles': existing_result.total_article_count,
                'positive_count': existing_result.positive_article_count,
                'negative_count': existing_result.negative_article_count,
                'mean_sentiment': existing_result.mean_sentiment,
                'summary': existing_result.main_headline
            },
            'top3': existing_result.top_3_articles,
            'bottom3': existing_result.bottom_3_articles
        }
        print("Existing result found for query:", query_text)
        return jsonify(response_data_front_end), 200

    # If no result exists for today, process the query and save the result
    response_data_front_end, search_result = processor.process_query(query_text)
    search_result_repository.create(search_result)

    return jsonify(response_data_front_end), 201
