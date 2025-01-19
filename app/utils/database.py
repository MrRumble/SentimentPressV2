import os
import psycopg
from flask import g
from psycopg.rows import dict_row

class DatabaseConnection:
    DEV_DATABASE_NAME = "sentiment_press_db_dev"
    TEST_DATABASE_NAME = "sentiment_press_db_test"
    PROD_DATABASE_NAME = "sentiment_press_db_prod"  # AWS RDS connection will be set dynamically


    def __init__(self, test_mode=False, prod_mode=False):
        self.test_mode = test_mode
        self.prod_mode = prod_mode

    # Connect to the correct PostgreSQL database.
    def connect(self):
        try:
            self.connection = psycopg.connect(
                f"postgresql://localhost/{self._database_name()}", 
                row_factory=dict_row
            )
        except psycopg.OperationalError:
            raise Exception(f"Couldn't connect to the database {self._database_name()}! " \
                             f"Did you create it using `createdb {self._database_name()}`?")
    
    def seed(self, sql_filename):
        self._check_connection()
        if not os.path.exists(sql_filename):
            raise Exception(f"File {sql_filename} does not exist")
        with self.connection.cursor() as cursor:
            cursor.execute(open(sql_filename, "r").read())
            self.connection.commit()

    def execute(self, query, params=[]):
        self._check_connection()
        with self.connection.cursor() as cursor:
            cursor.execute(query, params)
            if cursor.description is not None:
                result = cursor.fetchall()
            else:
                result = None
            self.connection.commit()
            return result

    CONNECTION_MESSAGE = '' \
        'DatabaseConnection.exec_params: Cannot run a SQL query as ' \
        'the connection to the database was never opened. Did you ' \
        'make sure to call first the method DatabaseConnection.connect` ' \
        'in your app.py file (or in your tests)?'

    def _check_connection(self):
        if self.connection is None:
            raise Exception(self.CONNECTION_MESSAGE)

    # Determine which database to connect to (based on environment mode).
    def _database_name(self):
        if self.prod_mode:
            return self.PROD_DATABASE_NAME
        elif self.test_mode:
            return self.TEST_DATABASE_NAME
        else:
            return self.DEV_DATABASE_NAME

# Flask Integration (for running in the Flask environment)
def get_flask_database_connection(app):
    if not hasattr(g, 'flask_database_connection'):
        # Determine whether app is in test mode or production mode using environment variables or configuration
        is_prod = os.getenv('APP_ENV') == 'production'
        is_test = os.getenv('APP_ENV') == 'test' or app.config['TESTING']

        g.flask_database_connection = DatabaseConnection(test_mode=is_test, prod_mode=is_prod)
        g.flask_database_connection.connect()
    return g.flask_database_connection
