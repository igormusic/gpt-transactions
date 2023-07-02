import os
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Date, ForeignKey, Numeric, URL


class Database:
    engine = None

    def __init__(self):
        # Fetch the environment variables
        username = os.environ.get('GPT_SQL_USERNAME')
        password = os.environ.get('GPT_SQL_PASSWORD')
        server_name = os.environ.get('GPT_SQL_SERVER_NAME')
        database_name = os.environ.get('GPT_SQL_DATABASE_NAME')

        # Construct the connection string
        self.connection_string = URL.create(
            "mssql+pyodbc",
            username=username,
            password=password,
            host=server_name,
            port=1433,
            database=database_name,
            query={
                "driver": "ODBC Driver 18 for SQL Server",
                "TrustServerCertificate": "yes"
            },
        )
        self.engine = create_engine(self.connection_string)

    def __enter__(self):
        self.connection = self.engine.connect()
        return self.connection

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()
