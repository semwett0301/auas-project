from pathlib import Path

from logic.award import prepare_award_xlsx
from logic.movie import prepare_movie_csv
from logic.reviews import prepare_reviews_xlsx
from preparation_module.logic.movie import prepare_sale_csv

# TODO create preparation for init csv files to get relevant data
# TODO remove check for existence from award and review preparation
# TODO Add transaction for all data insertion

# Constants
USER_CSV = f"{Path(__file__).resolve().parent}/data/init/UserReviewsClean43LIWC.csv"
EXPERT_CSV = f"{Path(__file__).resolve().parent}/data/init/ExpertReviewsClean43LIWC.csv"
META_CSV = f"{Path(__file__).resolve().parent}/data/init/metaClean43Brightspace.csv"
SALES_CSV = f"{Path(__file__).resolve().parent}/data/init/sales.csv"

MOVIE_RESULTS = f"{Path(__file__).resolve().parent}/data/result/movie.csv"
SALE_RESULTS = f"{Path(__file__).resolve().parent}/data/result/sale.csv"
AWARDS_RESULTS = f"{Path(__file__).resolve().parent}/data/result/award.csv"
AWARDS_MOVIE_RESULTS = f"{Path(__file__).resolve().parent}/data/result/award_movie.csv"
REVIEW_RESULTS = f"{Path(__file__).resolve().parent}/data/result/review.csv"

# Business code
movies = prepare_movie_csv(SALES_CSV, MOVIE_RESULTS)

prepare_sale_csv(SALES_CSV, SALE_RESULTS, movies)

prepare_award_xlsx(META_CSV, AWARDS_RESULTS, AWARDS_MOVIE_RESULTS, movies)

prepare_reviews_xlsx(EXPERT_CSV, USER_CSV, META_CSV, REVIEW_RESULTS, movies)
