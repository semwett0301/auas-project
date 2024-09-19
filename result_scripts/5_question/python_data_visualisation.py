# Haider

import matplotlib.pyplot as plt
import pandas as pd
from sqlalchemy import create_engine

# Database connection details
db_config = {
    'dbname': 'AUAS Data',
    'user': 'postgres',
    'password': 'data12',
    'host': 'localhost',  # server's address
    'port': '5432',       # default PostgreSQL port
}

# Establish a connection to PostgreSQL using psycopg2
conn_string = f"postgresql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['dbname']}"
engine = create_engine(conn_string)

# SQL query to classify movies into Peak and Off-Peak Seasons
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

# Fetch the data into a pandas DataFrame
df = pd.read_sql(query, engine)

# Group by season and calculate total and average box office sales
season_group = df.groupby('season').agg({
    'worldwide_box_office': ['sum', 'mean'],
    'domestic_box_office': ['sum', 'mean'],
    'international_box_office': ['sum', 'mean']
}).reset_index()

# Flatten multi-level columns
season_group.columns = ['season', 'total_worldwide', 'avg_worldwide', 'total_domestic', 'avg_domestic', 'total_international', 'avg_international']

# Plotting the data
fig, ax = plt.subplots(1, 3, figsize=(18, 6))

# Plot 1: Worldwide Box Office
ax[0].bar(season_group['season'], season_group['total_worldwide'], color=['#ff9999','#66b3ff'])
ax[0].set_title('Total Worldwide Box Office by Season')
ax[0].set_ylabel('Total Worldwide Box Office ($)')

# Plot 2: Domestic Box Office
ax[1].bar(season_group['season'], season_group['total_domestic'], color=['#ff9999','#66b3ff'])
ax[1].set_title('Total Domestic Box Office by Season')
ax[1].set_ylabel('Total Domestic Box Office ($)')

# Plot 3: International Box Office
ax[2].bar(season_group['season'], season_group['total_international'], color=['#ff9999','#66b3ff'])
ax[2].set_title('Total International Box Office by Season')
ax[2].set_ylabel('Total International Box Office ($)')

plt.tight_layout()
plt.show()
