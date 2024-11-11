import mysql.connector
from mysql.connector import Error

class DatabaseManager:
    def __init__(self, host, user, password, database, port =3306, ssl = None):
        """
        Initializes the DatabaseManager with connection details.
        :param host: Database host (e.g., 'localhost' or an IP address).
        :param user: Username for database authentication.
        :param password: Password for database authentication.
        :param database: Name of the database to connect to.
        """
        
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.port = port
        self.ssl = ssl
        self.connection = None
        

    def connect(self):
        """
        Establishes a connection to the MySQL database.
        """
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                port=self.port,
                ssl_disabled=not self.ssl  # Adjusts SSL based on ssl parameter
            )
            if self.connection.is_connected():
                print("Database connection established.")
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            self.connection = None

    def close(self):
        """
        Closes the connection to the MySQL database.
        """
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("Database connection closed.")

    def execute_query(self, query, params=None):
        cursor = self.connection.cursor()
        try:
            cursor.execute(query, params)
            result = cursor.fetchall()  # Read all rows to avoid "unread result" error
            cursor.close()
            return result
        except mysql.connector.Error as e:
            print(f"Error executing query: {e}")
            cursor.close()
            return None


    def execute_update(self, query, params=None):
        """
        Executes an INSERT, UPDATE, or DELETE query.
        :param query: SQL query to execute.
        :param params: Optional parameters to pass to the query.
        :return: True if the query was successful, False otherwise.
        """
        cursor = self.connection.cursor()
        try:
            cursor.execute(query, params)
            self.connection.commit()
            cursor.close()
        except mysql.connector.Error as e:
            print(f"Error executing update: {e}")
            cursor.close()


    def __enter__(self):
        """
        Enables the use of the 'with' statement for database connections.
        """
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Ensures the connection is closed when leaving the 'with' block.
        """
        self.close()
