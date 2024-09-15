from datetime import datetime

import pandas as pd

from preparation_module.utils.movie_check import check_movie_existence
from preparation_module.utils.save_data import save_data

AWARD_COLUMN = "awards"
MOVIE_AWARDS_COLUMNS = ["title", "RelDate", "awards"]


def split_cell(cell):
    print(f"award: preparing award {cell}")
    return cell.split(',')


def prepare_award(row, movies):
    result_list = []

    current_awards = split_cell(row[AWARD_COLUMN]) if row[AWARD_COLUMN] != "" else []
    current_title = f"{row[MOVIE_AWARDS_COLUMNS[0]]}-{datetime.strptime(row[MOVIE_AWARDS_COLUMNS[1]], '%d.%m.%Y').strftime('%Y-%m-%d')}"

    if check_movie_existence(movies, current_title):
        for current_award in current_awards:
            print(f"awards_movies: preparing award {current_title} - {current_award}")
            result_list.append([current_title, current_award])

        return result_list

    return None


def prepare_award_xlsx(movie_awards_csv, awards_csv, awards_movie_csv, movies):
    award_csv = pd.read_csv(movie_awards_csv, usecols=MOVIE_AWARDS_COLUMNS, sep=';').dropna(subset=[AWARD_COLUMN])

    awards = award_csv[AWARD_COLUMN].apply(split_cell).explode()
    awards = awards.drop_duplicates().tolist()

    result_awards = pd.DataFrame(awards, columns=["name"])

    save_data(result_awards, awards_csv, "award")

    movies_awards = award_csv.apply(prepare_award, axis=1, movies=movies).dropna().explode().tolist()
    movies_awards = pd.DataFrame(movies_awards, columns=["movie_title", "award_name"])

    save_data(movies_awards, awards_movie_csv, 'award_movie')
