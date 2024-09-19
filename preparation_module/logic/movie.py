from datetime import datetime

import pandas as pd
from sqlalchemy.dialects.mssql.information_schema import columns

from preparation_module.utils.movie_check import check_movie_existence
from preparation_module.utils.numbers import convert_to_int
from preparation_module.utils.save_data import save_data

SPECIFIED_COLUMNS = ["title", "international_box_office", "domestic_box_office", "worldwide_box_office", "release_date",
                     "year"]


def is_valid_date(date_str, date_format):
    try:
        datetime.strptime(date_str, date_format)
        return True
    except ValueError:
        return False


def get_correct_release_date(row):
    release_date = row["release_date"]
    year = row["year"]

    prepared_release_date = release_date.replace('st', '').replace('nd', '').replace('rd', '').replace('th', '').strip()

    day_and_month = datetime.strptime(prepared_release_date, '%B %d').strftime('%m-%d') if is_valid_date(
        prepared_release_date, '%B %d') else '01-01'

    return f"{year}-{day_and_month}"


def get_movie_title(row):
    title = row["title"]
    correct_date = get_correct_release_date(row)

    return f"{title}-{correct_date}"


def prepare_sales(row, movies):
    international_box_office = convert_to_int(row["international_box_office"])
    domestic_box_office = convert_to_int(row["domestic_box_office"])
    worldwide_box_office = None

    if international_box_office is not None and domestic_box_office is not None:
        worldwide_box_office = international_box_office + domestic_box_office
    elif international_box_office is not None:
        worldwide_box_office = international_box_office
    elif domestic_box_office is not None:
        worldwide_box_office = domestic_box_office

    movie_title = get_movie_title(row)

    if check_movie_existence(movies, movie_title):
        print(
            f"sale: preparing row {movie_title} - {worldwide_box_office} - {domestic_box_office} - {international_box_office}")

        return [movie_title, worldwide_box_office, international_box_office, domestic_box_office]

    return None


def prepare_movie(row):
    movie_title = get_movie_title(row)
    correct_release_date = get_correct_release_date(row)

    print(f"movie: preparing row {movie_title}")

    return [movie_title, correct_release_date]


def prepare_movie_csv(sales_csv, result_csv):
    source_columns = pd.read_csv(sales_csv, usecols=SPECIFIED_COLUMNS, sep=';')

    results = source_columns.apply(prepare_movie, axis=1).tolist()
    movies = (pd.DataFrame(results, columns=["title", "release_date"])
              .drop_duplicates(subset=['title']))

    save_data(movies, result_csv, "movie")

    movies.set_index("title", inplace=True)

    return movies


def prepare_sale_csv(sales_csv, result_csv, movies):
    source_columns = pd.read_csv(sales_csv, usecols=SPECIFIED_COLUMNS, sep=';')

    results = source_columns.apply(prepare_sales, axis=1, movies=movies).dropna().tolist()
    sales = pd.DataFrame(results, columns=["movie_title", "worldwide_box_office", "international_box_office",
                                           "domestic_box_office"])

    save_data(sales, result_csv, "sale")
