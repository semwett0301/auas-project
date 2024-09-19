# Sven

import pandas as pd

# Excel file in map
bestand_naam = 'sales.xlsx'

# Load excel file
sales = pd.read_excel(bestand_naam)

sales.head()

filtered_sales.head()

import pandas as pd
import re


# Function to clean and combine year and release_date
def clean_and_combine_date(row):
    try:
        # Clean the release_date by keeping only month and day
        clean_release_date = re.sub(r'[^a-zA-Z0-9\s]', '', row['release_date']).split()[0:2]
        if len(clean_release_date) == 2:  # Make sure both month and day exist
            clean_release_date = ' '.join(clean_release_date)
        else:
            return None  # Return None if release_date is not in the expected format

        # Combine year and cleaned release_date
        combined_date_str = f"{clean_release_date} {row['year']}"
        return combined_date_str
    except:
        return None  # Return None if any error occurs


# Apply the function to create a 'combined_date' column
filtered_sales['combined_date'] = filtered_sales.apply(clean_and_combine_date, axis=1)

# Now attempt to parse 'combined_date' into a datetime object
filtered_sales['full_release_date'] = pd.to_datetime(filtered_sales['combined_date'], errors='coerce',
                                                     format='%B %d %Y')

# Check the new column
print(filtered_sales[['year', 'release_date', 'combined_date', 'full_release_date']].head())

# Select the specific columns you want to keep
filtered_sales = filtered_sales[
    ['title', 'international_box_office', 'domestic_box_office', 'worldwide_box_office', 'combined_date']]

# Show the first few rows of the filtered dataset
print(filtered_sales.head())

filtered_sales.head()

# Save the filtered dataset as a CSV file
filtered_sales.to_csv('filtered_sales.csv', index=False)
