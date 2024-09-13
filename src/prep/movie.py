import pandas as pd
from datetime import datetime

from src.utils.db import engine

SPECIFIED_COLUMNS = ["title", "international_box_office", "domestic_box_office", "worldwide_box_office", "release_date",
                     "year"]


def is_valid_date(date_str, date_format):
    try:
        datetime.strptime(date_str, date_format)
        return True
    except ValueError:
        return False


def prepare_movie_xlsx(sales_xlsx, sheet_name, result_csv):
    movie_sheet = pd.read_excel(sales_xlsx, sheet_name=sheet_name)

    result_columns = movie_sheet[SPECIFIED_COLUMNS]

    for index, row in result_columns.iterrows():
        title = row["title"]
        year = row["year"]
        prepared_release_date = row["release_date"].replace('st', '').replace('nd', '').replace('rd', '').replace('th',
                                                                                                                  '').strip()

        day_and_month = datetime.strptime(prepared_release_date, '%B %d').strftime('%m-%d') if is_valid_date(
            prepared_release_date, '%B %d') else '01.01'

        result_columns.loc[index, "title"] = f"{title}-{year}-{day_and_month}"
        result_columns.loc[index, "release_date"] = f"{year}-{day_and_month}"

    result_columns = result_columns.drop(columns=["year"])
    # result_columns.to_sql('movie', engine, if_exists='replace', index=False)
    result_columns.to_csv(result_csv)
