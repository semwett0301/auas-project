# Gwen
import pandas as pd

# Gwen
bestand_naam = "UserReviewsClean43LIWC (1).xlsx"
df = pd.read_excel(bestand_naam)

# Gwen show table
df.head()

# Gwen
User_review = df

# Gwen select from data frame
url_idv_user = User_review[["url","idvscore"]]
print = url_idv_user

# Gwen show new data frame
url_idv_user.head()

# Gwen idvs score times ten
user_fil_def = url_idv_user[["url"]].copy()
user_fil_def["idvscore_x10"] = url_idv_user["idvscore"]*10
user_fil_def

# Gwen remove duplicates
user_fil_duplicates = user_fil_def.drop_duplicates()
user_fil_duplicates

# Gwen save file
user_fil_def.to_excel("C:\\Users\\gwenr\\OneDrive\\Documenten\\DDB master 24\\user_fil_def2.xlsx")

# Gwen remove empty cells
emptycells = user_fil_def["idvscore_x10"].isna()
emptycells

# Gwen save new file
user_fil_duplicates.to_csv("C:\\Users\\gwenr\\OneDrive\\Documenten\\DDB master 24\\user_fil_duplicates", index=False)

# %%



