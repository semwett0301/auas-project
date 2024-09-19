#Importing the pandas and numpy libraries (WENDY)
import pandas as pd

#Importing the excel file to python (WENDY)
file_name_expert = 'ExpertReviewsClean43LIWC.xlsx'
df_expert_review = pd.read_excel(file_name_expert)

#Presenting the dataframe with the first 5 rows (WENDY)
df_expert_review.head()

#Selecting only the url and idvscore columns as they will be needed (WENDY)
filterd_url_idvscore = df_expert_review[['url' , 'idvscore']]
filterd_url_idvscore

#Removing the duplicates from the columns (WENDY)
df_expert_def = filterd_url_idvscore.drop_duplicates()
df_expert_def

#Saving the dataframe to csv on my local laptop
df_expert_def.to_csv("/Users/wendyessilfie/Library/Mobile Documents/com~apple~CloudDocs/School map/Cleaned_idv_Wendy", index= False)