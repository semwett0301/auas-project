from datetime import datetime

import pandas as pd

AWARD_COLUMN = "awards"
MOVIE_AWARDS_COLUMNS = ["title", "RelDate", "awards"]


def split_cell(cell):
    print(f"award: preparing award {cell}")
    return cell.split(',')


def prepare_award(row):
    current_awards = split_cell(row[AWARD_COLUMN]) if row[AWARD_COLUMN] != "" else []
    current_title = f"{row[MOVIE_AWARDS_COLUMNS[0]]}-{datetime.strptime(row[MOVIE_AWARDS_COLUMNS[1]], '%d.%m.%Y').strftime('%Y-%m-%d')}"

    for current_award in current_awards:
        print(f"awards_movies: preparing award {current_title} - {current_award}")
        return [current_title, current_award]


def prepare_award_xlsx(movie_awards_csv, awards_csv, awards_movie_csx):
    award_csv = pd.read_csv(movie_awards_csv, usecols=MOVIE_AWARDS_COLUMNS, sep=';').dropna(subset=[AWARD_COLUMN])

    awards = award_csv[AWARD_COLUMN].apply(split_cell).explode()
    awards = awards.drop_duplicates().tolist()

    result_awards = pd.DataFrame(awards, columns=["name"])

    result_awards.to_csv(awards_csv)

    movies_awards = award_csv.apply(prepare_award, axis=1).tolist()

    movies_awards = pd.DataFrame(movies_awards, columns=["title", "awards"])
    movies_awards.to_csv(awards_movie_csx)
