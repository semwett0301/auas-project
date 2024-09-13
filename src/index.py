from pathlib import Path

from src.prep.award import prepare_award_xlsx
from src.prep.movie import prepare_movie_xlsx

prepare_movie_xlsx(f"{Path(__file__).resolve().parent}/data/init/sales.xlsx", "numbers253",
                   f"{Path(__file__).resolve().parent}/data/result/movie.csv")

prepare_award_xlsx(f"{Path(__file__).resolve().parent}/data/init/metaClean43Brightspace.xlsx", "Sheet1",
                   f"{Path(__file__).resolve().parent}/data/result/award.csv", f"{Path(__file__).resolve().parent}/data/result/award_movie.csv")
