# Sven

import pandas as pd

# Excel file in map
bestand_naam = 'movie.xlsx'

# Load excel file
Movie = pd.read_excel(bestand_naam)

Movie.head()

# Excel file in map
bestand_naam2 = 'metaclean43Brightspace.xlsx'

# Load excel file
Metaclean = pd.read_excel(bestand_naam2)

Metaclean.head()

# Select the specific columns you want to keep
columns = ['title', 'metascore', 'RelDate']
filtered_metaclean = Metaclean[columns]

filtered_metaclean.head()

# Convert 'RelDate' column to string (if not already datetime, first convert it)
filtered_metaclean['RelDate'] = pd.to_datetime(filtered_metaclean['RelDate'], errors='coerce')

# Combine the 'title' and 'RelDate' columns
filtered_metaclean['title_with_date'] = filtered_metaclean['title'] + ' (' + filtered_metaclean['RelDate'].dt.strftime(
    '%Y-%m-%d') + ')'

# Display the first few rows to check the new column
print(filtered_metaclean[['title', 'RelDate', 'title_with_date']].head())

filtered_metaclean.head()
