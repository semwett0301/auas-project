# Sven

import pandas as pd

filtered_idv_score_expert = pd.read_csv('filterd_url_idvscore.csv')

print(filtered_idv_score_expert)

# split the column based on semicolons (;)

# First, split the combined column into separate components
filtered_idv_score_expert[['index', 'url', 'idvscore']] = filtered_idv_score_expert[';url;idvscore'].str.split(';',
                                                                                                               expand=True)

# Remove the 'index' column as it duplicates the index
filtered_idv_score_expert.drop(columns=['index'], inplace=True)

# Convert the 'idvscore' column to numeric type in case you want to use it later
filtered_idv_score_expert['idvscore'] = pd.to_numeric(filtered_idv_score_expert['idvscore'])

# Check the result
filtered_idv_score_expert.head()

filtered_idv_score_expert = filtered_idv_score[['url', 'idvscore']]

print(filtered_idv_score_expert)

# Rename the 'idvscore' column to 'idv_score_expert'
filtered_idv_score_expert.rename(columns={'idvscore': 'idv_score_expert'}, inplace=True)

# Check the updated dataframe
filtered_idv_score_expert.head()

# Extract the movie name from the URL by splitting on '/' and taking the last part
# filtered_idv_score['movie'] = filtered_idv_score['url'].str.split('/').str[-1]

# Display the updated dataframe to check the new 'movie' column
# filtered_idv_score.head()


# Excel file in map
bestand_naam = 'UserReviewsClean43LIWC.xlsx'

# Load excel file
filtered_idv_score_user = pd.read_excel(bestand_naam)

filtered_idv_score_user.head()

filtered_idv_score_user = filtered_idv_score_user[['url', 'idvscore']]

print(filtered_idv_score_user)

# Rename the 'idvscore' column to 'idv_score_expert'
filtered_idv_score_user.rename(columns={'idvscore': 'idv_score_user'}, inplace=True)

# Check the updated dataframe
filtered_idv_score_user.head()

# Merge the two dataframes on the 'url' column
merged_df = pd.merge(filtered_idv_score_expert, filtered_idv_score_user, on='url', how='inner')

# Display the first few rows to check the result
merged_df.head()

merged_df.head()

# Save the filtered dataset as a CSV file
merged_df.to_csv('merged_df.csv', index=False)

merged_df = pd.read_csv('merged_df.csv')

merged_df.head()

# Check the column names to confirm the exact names in the dataframe
print(merged_df.columns)

# Extract the movie name from the URL by splitting on '/' and taking the last part
merged_df['movie'] = merged_df['url'].str.split('/').str[-1]

# Rearrange columns to show 'movie', 'idv_score_expert', and 'idv_score_user'
merged_df = merged_df[['movie', 'idv_score_expert', 'idv_score_user']]

merged_df.head()

# Convert 'idv_score_expert' and 'idv_score_user' to numeric, invalid parsing will be set as NaN
merged_df['idv_score_expert'] = pd.to_numeric(merged_df['idv_score_expert'], errors='coerce')
merged_df['idv_score_user'] = pd.to_numeric(merged_df['idv_score_user'], errors='coerce')

# Drop rows where either 'idv_score_expert' or 'idv_score_user' is NaN
merged_df.dropna(subset=['idv_score_expert', 'idv_score_user'], inplace=True)

# Check the cleaned dataframe
merged_df.head()

# Convert 'idv_score_expert' and 'idv_score_user' to numeric, invalid parsing will be set as NaN
merged_df['idv_score_expert'] = pd.to_numeric(merged_df['idv_score_expert'], errors='coerce')
merged_df['idv_score_user'] = pd.to_numeric(merged_df['idv_score_user'], errors='coerce')

# Replace NaN values with 0 (or any other default value)
merged_df['idv_score_expert'].fillna(0, inplace=True)
merged_df['idv_score_user'].fillna(0, inplace=True)

# Check the updated dataframe
merged_df.head()

# Multiply the 'idv_score_user' column by 10
merged_df['idv_score_user'] = merged_df['idv_score_user'] / 10

# Check the updated dataframe
merged_df.head()

merged_df.head()

# Save the filtered dataset as a CSV file
merged_df.to_csv('merged_user_and_expert_final_df.csv', index=False)
