import csv
import os
from io import StringIO

from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Date, ForeignKey, Numeric, URL, text
from sqlalchemy.orm import sessionmaker


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

    def query(self, query):
        session_factory = sessionmaker(self.engine)

        with session_factory() as session:
            try:
                result = session.execute(text(query))
            except Exception as e:
                print(e)
                raise ValueError("Invalid query")

            columns = result.keys()

            # Create a string buffer
            csv_buffer = StringIO()
            csv_writer = csv.writer(csv_buffer)

            # Write the column headers
            csv_writer.writerow(columns)

            # Write the rows
            for row in result:
                csv_writer.writerow(row)

            # Get the CSV content from the buffer
            return csv_buffer.getvalue()

    def query_schema(self, tables):
        table_list = ", ".join(tables)
        sql = f"SELECT CONCAT(TABLE_SCHEMA, '.', TABLE_NAME, ', ', COLUMN_NAME, ', ', DATA_TYPE) " \
              f"AS 'Table, Column, DataType' " \
              f"FROM INFORMATION_SCHEMA.COLUMNS " \
              f"WHERE TABLE_NAME IN ({table_list})"

        return self.query(sql)
