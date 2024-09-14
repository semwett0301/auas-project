from pathlib import Path

from src.prep.award import prepare_award_xlsx
from src.prep.movie import prepare_movie_xlsx
from src.prep.reviews import prepare_reviews_xlsx

# Constants
USER_CSV = f"{Path(__file__).resolve().parent}/data/init/UserReviewsClean43LIWC.csv"
EXPERT_CSV = f"{Path(__file__).resolve().parent}/data/init/ExpertReviewsClean43LIWC.csv"
META_CSV = f"{Path(__file__).resolve().parent}/data/init/metaClean43Brightspace.csv"
SALES_CSV = f"{Path(__file__).resolve().parent}/data/init/sales.csv"

MOVIE_RESULTS = f"{Path(__file__).resolve().parent}/data/result/movie.csv"
AWARDS_RESULTS = f"{Path(__file__).resolve().parent}/data/result/award.csv"
AWARDS_MOVIE_RESULTS = f"{Path(__file__).resolve().parent}/data/result/award_movie.csv"
REVIEW_RESULTS = f"{Path(__file__).resolve().parent}/data/result/review.csv"


# Business code
# prepare_movie_xlsx(SALES_CSV, MOVIE_RESULTS)

# prepare_award_xlsx(META_CSV, AWARDS_RESULTS, AWARDS_MOVIE_RESULTS)

prepare_reviews_xlsx(EXPERT_CSV, USER_CSV, META_CSV, REVIEW_RESULTS)
