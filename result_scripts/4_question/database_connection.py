# Sven

import pandas as pd


import psycopg2

# Maak verbinding met de PostgreSQL-database
conn = psycopg2.connect(
    host="localhost",  # Je werkt lokaal, dus localhost
    database="DBM assignment 1",  # Vul hier de naam van je database in
    user="postgres",  # Dit is je gebruikersnaam
    password="xxxxxxxxxxxx",  # Vul hier het wachtwoord van de gebruiker 'postgres' in
    port="5432"  # Dit is de standaardpoort voor PostgreSQL
)

# Maak een cursor om SQL-opdrachten uit te voeren
cur = conn.cursor()

# Controleer of de verbinding werkt
print("Verbonden met de database")

# Sluit de verbinding (na je opdrachten)
#cur.close()
#conn.close()



query = '''
SELECT *
FROM public."Movie" M
LEFT JOIN public."Award_movie" AM
ON M.title = AM.movie_title;
'''
cur.execute(query)
rows = cur.fetchall()

# Results to DF
df = pd.DataFrame(rows, columns=[desc[0] for desc in cur.description])

# Show DF
print(df)



df.head()


# Print the movie title with the highest worldwide box office
print(df.loc[df['worldwide_box_office'].idxmax()]['movie_title'])



df = df[['movie_title', 'award_name','worldwide_box_office', 'international_box_office', 'domestic_box_office']]



import plotly.graph_objects as go

# Make new df for plot 
box_office_df = df[['worldwide_box_office', 'domestic_box_office', 'international_box_office']]

fig = go.Figure()

# Box for WWBO
fig.add_trace(go.Box(y=box_office_df['worldwide_box_office'], name='Worldwide Box Office'))

# Box for DBO
fig.add_trace(go.Box(y=box_office_df['domestic_box_office'], name='Domestic Box Office'))

# Box for IBO
fig.add_trace(go.Box(y=box_office_df['international_box_office'], name='International Box Office'))

# Layout
fig.update_layout(
    title="Box Office Distribution",
    yaxis_title="Box Office Sales",
    xaxis_title="Box Office Type",
    showlegend=False
)

#Show plot
fig.show()


# In[10]:


df.head()


# In[15]:


import re
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import plotly.express as px

# Step 1: Ensure the 'award_name' column is a string and handle missing values
df['award_name'] = df['award_name'].fillna('')

# Step 2: Extract the ranking (number) from the 'award_name' using regex
df['award_rank'] = df['award_name'].apply(lambda x: int(re.findall(r'\d+', str(x))[0]) if re.findall(r'\d+', str(x)) else 0)

# Step 3: Define the independent variable (award_rank) and dependent variable (worldwide_box_office)
X = df[['award_rank']]  # Award rank as independent variable
y = df['worldwide_box_office']  # Worldwide box office as the target variable

# Step 4: Split the data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Step 5: Train the linear regression model
model = LinearRegression()
model.fit(X_train, y_train)

# Step 6: Predict box office sales based on the test set
y_pred = model.predict(X_test)

# Step 7: Evaluate the model using Mean Squared Error
mse = mean_squared_error(y_test, y_pred)
print(f"Mean Squared Error: {mse}")

# Step 8: Check the coefficient (impact of award ranking on box office)
coef = model.coef_[0]
print(f"Coefficient (impact of award rank on box office): {coef}")

# Step 9: Scatter plot of award ranking vs worldwide box office
fig = px.scatter(df, x='award_rank', y='worldwide_box_office', trendline='ols', title='Impact of Award Rank on Worldwide Box Office')
fig.show()

