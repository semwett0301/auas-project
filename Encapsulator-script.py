import pandas as pd
from sqlalchemy import create_engine
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import psycopg2
import numpy as np

class BoxOfficeDataEncapsulator:
    def __init__(self, db_config):
        """
        Initializes the BoxOfficeDataEncapsulator object with a database configuration.
        :param db_config: Dictionary containing database connection parameters.
        """
        self.db_config = db_config
        self.engine = self._create_engine()
        self.data = None

    def _create_engine(self):
        """
        Creates a database connection engine using SQLAlchemy.
        :return: SQLAlchemy engine object.
        """
        try:
            conn_string = f"postgresql://{self.db_config['user']}:{self.db_config['password']}@{self.db_config['host']}:{self.db_config['port']}/{self.db_config['dbname']}"
            return create_engine(conn_string)
        except Exception as e:
            print(f"Error creating engine: {e}")
            raise

    def fetch_box_office_data(self):
        """
        Fetches the box office data from the Movie table in the database,
        classifying movies into Peak and Off-Peak seasons.
        Stores the result in the instance's `data` attribute.
        """
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
        try:
            # Execute the query and store the result as a DataFrame
            self.data = pd.read_sql(query, self.engine)
            return self.data
        except Exception as e:
            print(f"Error fetching data: {e}")
            return None

    def preprocess_data(self):
        """
        Preprocesses the data for statistical analysis and machine learning.
        Handles missing values, feature engineering, and data scaling.
        :return: Preprocessed pandas DataFrame.
        """
        if self.data is None:
            raise ValueError("Data has not been fetched. Call fetch_box_office_data first.")

        # Handle missing values (can be customized)
        self.data.fillna(0, inplace=True)

        # Convert categorical variables (like 'season') to numerical if needed for ML
        self.data['season'] = self.data['season'].apply(lambda x: 1 if x == 'Peak Season' else 0)

        # Scaling the numeric columns
        scaler = StandardScaler()
        numeric_cols = ['worldwide_box_office', 'international_box_office', 'domestic_box_office']
        self.data[numeric_cols] = scaler.fit_transform(self.data[numeric_cols])

        return self.data

    def split_data_for_ml(self, target_column='worldwide_box_office'):
        """
        Splits the dataset into training and testing sets for machine learning.
        :param target_column: The column to predict (default: 'worldwide_box_office').
        :return: X_train, X_test, y_train, y_test.
        """
        if self.data is None:
            raise ValueError("Data has not been fetched or preprocessed. Call fetch_box_office_data and preprocess_data first.")

        # Defining features (X) and target (y)
        X = self.data.drop(columns=[target_column, 'title', 'release_date'])
        y = self.data[target_column]

        # Splitting into training and test sets (80% train, 20% test)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        return X_train, X_test, y_train, y_test

    def get_summary_statistics(self):
        """
        Returns summary statistics of the dataset for statistical analysis.
        :return: Summary statistics as a pandas DataFrame.
        """
        if self.data is None:
            raise ValueError("Data has not been fetched. Call fetch_box_office_data first.")

        return self.data.describe()

    def calculate_correlations(self):
        """
        Calculates correlations between numeric features in the dataset.
        :return: Correlation matrix as a pandas DataFrame.
        """
        if self.data is None:
            raise ValueError("Data has not been fetched. Call fetch_box_office_data first.")

        # Drop non-numeric columns (like 'title', 'release_date')
        numeric_data = self.data.drop(columns=['title', 'release_date'])
        return numeric_data.corr()

    def close_connection(self):
        """
        Closes the database connection if necessary.
        """
        self.engine.dispose()


# Example usage:

# Database connection details
db_config = {
    'dbname': 'AUAS Data',
    'user': 'postgres',
    'password': 'data12',
    'host': 'localhost',  # server's address
    'port': '5432',       # default PostgreSQL port
}

# Initialize the BoxOfficeDataEncapsulator object
box_office_encapsulator = BoxOfficeDataEncapsulator(db_config)

# Fetch the box office data
df = box_office_encapsulator.fetch_box_office_data()

# Preprocess the data for ML/statistical analysis
preprocessed_data = box_office_encapsulator.preprocess_data()

# Split the data for machine learning
X_train, X_test, y_train, y_test = box_office_encapsulator.split_data_for_ml()

# Get summary statistics
summary_stats = box_office_encapsulator.get_summary_statistics()

# Calculate correlations
correlations = box_office_encapsulator.calculate_correlations()

# Close the database connection
box_office_encapsulator.close_connection()

# Output examples
print(summary_stats)
print(correlations)
