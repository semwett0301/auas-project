import pandas as pd

AWARD_COLUMN = "awards"
MOVIE_AWARDS_COLUMNS = ["title", "RelDate", "awards"]


def split_cell(cell):
    return cell.split(',')


def prepare_award_xlsx(movie_awards_xlsx, sheet_name, awards_csv, awards_movie_csx):
    award_sheet = pd.read_excel(movie_awards_xlsx, sheet_name=sheet_name, keep_default_na=False)

    awards = award_sheet[AWARD_COLUMN].apply(split_cell).explode()
    awards = awards[awards != ""]
    awards = awards.drop_duplicates().tolist()

    result_awards = pd.DataFrame(awards, columns=["name"])

    result_awards.to_csv(awards_csv)

    movies_awards_columns = award_sheet[MOVIE_AWARDS_COLUMNS]
    movies_awards = []

    for index, row in movies_awards_columns.iterrows():
        current_awards = split_cell(row[AWARD_COLUMN]) if row[AWARD_COLUMN] != "" else []
        current_title = f"{row[MOVIE_AWARDS_COLUMNS[0]]}-{row[MOVIE_AWARDS_COLUMNS[1]].strftime('%Y-%m-%d')}"

        for current_award in current_awards:
            movies_awards.append([current_title, current_award])

    movies_awards = pd.DataFrame(movies_awards, columns=["title", "awards"])
    movies_awards.to_csv(awards_movie_csx)
