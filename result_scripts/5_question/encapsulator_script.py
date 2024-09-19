# Haider

import pandas as pd  #importing pandas here
import psycopg2


class MovieDataEncapsulator:
    def __init__(self, host, dbname, user, password):
        # Store database connection parameters
        self.host = host
        self.dbname = dbname
        self.user = user
        self.password = password
    
    def _connect(self):
        #  connection to the database
        try:
            connection = psycopg2.connect(
                host=self.host,
                dbname=self.dbname,
                user=self.user,
                password=self.password
            )
            return connection
        except Exception as e:
            print(f"Error connecting to the database: {e}")
            return None

    def fetch_movie_data(self):
        # Query to fetch movie data and season classification
        query = """
        SELECT title,
               release_date,
               worldwide_box_office,
               international_box_office,
               domestic_box_office,
               CASE 
                   WHEN EXTRACT(MONTH FROM release_date) IN (6, 7, 8, 11, 12) THEN 'Peak Season'
                   ELSE 'Off-Peak Season'
               END AS season
        FROM "Movie";
        """

        # Establish connection and execute query
        connection = self._connect()
        if connection is None:
            return None
        
        try:
            # I am using pandas to execute the query and load results into a DataFrame
            df = pd.read_sql_query(query, connection)
            return df
        except Exception as e:
            print(f"Error fetching data: {e}")
            return None
        finally:
            # Close the connection after the query
            connection.close()

# Usage
# Initialize the encapsulator with database connection details
encapsulator = MovieDataEncapsulator(
    host="localhost", 
    dbname="AUAS Data", 
    user="postgres", 
    password="data12"
)

# Fetch the data
movie_data_df = encapsulator.fetch_movie_data()

# Display the resulting DataFrame
if movie_data_df is not None:
    print(movie_data_df.head())  # Show the first few rows for verification
else:
    print("Failed to fetch data.")
