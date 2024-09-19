# Haider

import pandas as pd # Importing the pandas

file_path = r'C:\Users\haide\Desktop\Master\Data analytics\ExpertReviewsClean43LIWC.xlsx'  # The location of the data file

data = pd.read_excel(file_path)  

print (data)    #excessing the data form the file




print(data.info()) # Show basic information about the dataset (data types, non-null counts, etc.)


print(data.describe()) # Show summary statistics


print(data.isnull().sum())  # Show missing values


data.drop_duplicates(inplace=True) # Remove duplicate rows


data_filtered = data[['url', 'idvscore']] #Access coloumns and create new dataframe

data_filtered.head()  #Shows the first 5 rows of the data


if 'url' in data_filtered.columns:
    data_filtered.loc[:, 'movie_name'] = data_filtered['url'].str.split('/').str[-1] #Extracting the movie names from data file and creating new column.
else:
    print("Column 'url' not found in the DataFrame")



print(data_filtered)


release_dates = pd.read_excel(r'C:\Users\haide\Downloads\metaClean43Brightspace.xlsx', usecols=['release_dates'])

print(release_dates)


data_filtered = pd.read_excel(r'C:\Users\haide\Desktop\updated_file.xlsx')


print(data_filtered.columns)


print(release_dates.columns)




