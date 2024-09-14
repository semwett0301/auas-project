from datetime import datetime

import pandas as pd

SPECIFIED_COLUMNS = ["title", "international_box_office", "domestic_box_office", "worldwide_box_office", "release_date",
                     "year"]


def is_valid_date(date_str, date_format):
    try:
        datetime.strptime(date_str, date_format)
        return True
    except ValueError:
        return False


def prepare_movie(row):
    title = row["title"]
    year = row["year"]

    international_box_office = row["international_box_office"]
    domestic_box_office = row["domestic_box_office"]
    worldwide_box_office = row["worldwide_box_office"]

    prepared_release_date = row["release_date"].replace('st', '').replace('nd', '').replace('rd', '').replace('th',
                                                                                                              '').strip()

    day_and_month = datetime.strptime(prepared_release_date, '%B %d').strftime('%m-%d') if is_valid_date(
        prepared_release_date, '%B %d') else '01.01'

    print(f"movie: preparing row {title} - {year}-{day_and_month}")

    return [f"{title}-{year}-{day_and_month}", f"{year}-{day_and_month}", worldwide_box_office,
            international_box_office, domestic_box_office]


def prepare_movie_xlsx(sales_csv, result_csv):
    source_columns = pd.read_csv(sales_csv, usecols=SPECIFIED_COLUMNS, sep=';')

    results = source_columns.apply(prepare_movie, axis=1).tolist()
    movies_awards = pd.DataFrame(results,
                                 columns=["title", "release_date", "worldwide_box_office", "international_box_office",
                                          "domestic_box_office"])

    movies_awards.to_csv(result_csv)
