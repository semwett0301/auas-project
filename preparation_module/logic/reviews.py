from datetime import datetime

import pandas as pd

from preparation_module.utils.movie_check import check_movie_existence
from preparation_module.utils.save_data import save_data

REVIEW_COLUMNS = ["url", "idvscore"]
META_CLEAN_COLUMNS = ["url", "title", "RelDate"]


def find_row_by_url(meta_clean_columns, url):
    return meta_clean_columns.loc[meta_clean_columns['url'] == url].iloc[0]


def safe_cast_to_int(value):
    try:
        return int(value)
    except ValueError:
        return None


def map_columns(row, meta_columns, role, movies, idvscore_map_func=None):
    current_url = row["url"]
    current_idv = safe_cast_to_int(row["idvscore"])

    if current_idv is not None:
        if idvscore_map_func is not None:
            current_idv = idvscore_map_func(int(current_idv))

        current_meta_row = find_row_by_url(meta_columns, current_url)

        if current_meta_row is not None:
            current_date = datetime.strptime(current_meta_row["RelDate"], "%d.%m.%Y").strftime("%Y-%m-%d")
            current_title = current_meta_row["title"]
            result_title = f"{current_title}-{current_date}"

            if check_movie_existence(movies, result_title):
                print(f"reviews: processing review {result_title} - {current_idv} - {role}")

                return [result_title, current_idv, role]
        else:
            print(f"reviews: no meta data found for URL {current_url}")

    return None


def prepare_reviews_xlsx(expert_csv, user_csv, meta_clean_csv, result_csv, movies):
    print("Opening expert reviews csv file...")
    expert_columns = pd.read_csv(expert_csv, usecols=REVIEW_COLUMNS, sep=';')

    print("Opening user reviews csv file...")
    user_columns = pd.read_csv(user_csv, usecols=REVIEW_COLUMNS, sep=';')

    print("Opening meta clean csv file...")
    meta_columns = pd.read_csv(meta_clean_csv, usecols=META_CLEAN_COLUMNS, sep=';')

    print("Files opened!")

    result_dataset = pd.DataFrame(columns=["movie_title", "idvscore", "role"])

    expert_results = expert_columns.apply(func=map_columns, role="expert", meta_columns=meta_columns, axis=1,
                                          movies=movies).dropna()
    expert_results_df = pd.DataFrame(expert_results.tolist(), columns=["movie_title", "idvscore", "role"])

    user_results = user_columns.apply(func=map_columns, role="user", meta_columns=meta_columns, axis=1,
                                      idvscore_map_func=lambda x: x * 10, movies=movies).dropna()
    user_results_df = pd.DataFrame(user_results.tolist(), columns=["movie_title", "idvscore", "role"])

    result_dataset = pd.concat([result_dataset, expert_results_df, user_results_df], ignore_index=True)

    save_data(result_dataset, result_csv, "review")
