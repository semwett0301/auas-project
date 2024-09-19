# Importing my libraries and defining them (WENDY)
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import psycopg2
import seaborn as sns
from scipy.stats import ttest_ind

#Conecting my SQL to my Python (WENDY)
conn = psycopg2.connect(
    host="localhost",
    database="DBM assignment 1",
    user="postgres",
    password="Wendy888",
    port="5432"
)

# creating my cursor and connectin it (WENDY)
cur = conn.cursor()

#Defining my sql query so that it can be a variable in python (WENDY)
review_query = """SELECT  movie_box_office."title",
    "worldwide_box_office",
    "international_box_office",
    "domestic_box_office",
    "average_score"
FROM (
    SELECT "title", "worldwide_box_office", 
	"international_box_office", "domestic_box_office" 
    FROM public."Movie"
) AS movie_box_office
INNER JOIN (
    SELECT "title", ROUND(AVG("idvscore"), 0) AS average_score
    FROM public."Review"
    WHERE "role" = 'expert'
    GROUP BY "title"
) AS expert_avg_scores
ON movie_box_office."title" = expert_avg_scores."title";
"""

#excecuting my query with the cursur and also fetching the data to display (WENDY)
cur.execute(review_query)
review_results = cur.fetchall()

#creating a dataframe with my wanted columns and displaying the head with first 5 rows (WENDY)
query_df = pd.DataFrame(review_results, columns=["title",
    "worldwide_box_office",
    "international_box_office",
    "domestic_box_office",
    "average_score"])
query_df.head()

#Showing what the lowest and higest scores are that trhe experts give (WENDY)
lowest_value = query_df["average_score"].min()
highest_value = query_df["average_score"].max()
print(lowest_value,highest_value)

# creating a correlation matrix for the 3 box offices (WENDY)
# here average score is the independant variable and the box offices are dependent (WENDY)
corr_matrix = query_df[["average_score", "worldwide_box_office" , "international_box_office", "domestic_box_office"]].corr()
print(corr_matrix)

# Creating a heat map with the correlation matrix (WENDY)
plt.figure(figsize=(8,6))
sns.heatmap(corr_matrix, annot=True, cmap = "coolwarm", vmin=-1, vmax=1)
plt.title("Correlation matrix")


# Categorizing movies into two groups based on the average score (70 and above, below 70) (WENDY)
query_df['score_category'] = np.where(query_df['average_score'] >= 70, '70 and Above', 'Below 70')

# Performing the t-test for worldwide box office as an example (WENDY)
t_statistic, p_value = ttest_ind(
    query_df[query_df['score_category'] == '70 and Above']['worldwide_box_office'], 
    query_df[query_df['score_category'] == 'Below 70']['worldwide_box_office'],
    nan_policy='omit')
print(f'T-Test for Worldwide Box Office: t-statistic = {t_statistic}, p-value = {p_value}')

# Visualizing the data with a simple box plot (WENDY)
plt.figure(figsize=(8, 6))
sns.boxplot(x='score_category', y='worldwide_box_office', data = query_df)
plt.title('Worldwide Box Office by Review Score Category')
plt.xlabel('Review Score Category')
plt.ylabel('Worldwide Box Office')
plt.show()
