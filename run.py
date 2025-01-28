from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from app.routes.query_route import query_route
from app.routes.automated_populator_route import populate_route
from app.routes.sentiment_route import sentiment_route
import os

load_dotenv()

# Create a new Flask app
app = Flask(__name__)
CORS(app)

app.register_blueprint(query_route)
app.register_blueprint(populate_route)
app.register_blueprint(sentiment_route)

if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get('PORT', 5002)))
