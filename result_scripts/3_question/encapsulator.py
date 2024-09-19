# Semen Mokrov
from sqlalchemy import text

from common_module.db import engine
import pandas as pd


class Encapsulator:
    def __init__(self):
        # Constants
        self._WORLDWIDE_BOX_OFFICE_COLUMN = 'worldwide_box_office_avg'

        self._USER_REVIEW_VIEW_NAME = 'good_user_reviews_box_office_information'
        self._EXPERT_REVIEW_VIEW_NAME = 'good_user_reviews_box_office_information'

        # Queries
        self._CHECK_VIEW_QUERY = text("""
        SELECT EXISTS (
            SELECT 1
            FROM pg_catalog.pg_views
            WHERE schemaname = 'public' AND viewname = :view_name
        );
        """)

        self._USER_REVIEW_BOX_OFFICE_VIEW = text("""
        CREATE OR REPLACE VIEW :view_name AS
        SELECT m.title, AVG(s.worldwide_box_office) as worldwide_box_office_avg
        FROM movie m
                 JOIN sale s ON s.movie_title = m.title AND s.worldwide_box_office IS NOT NULL AND
                                m.title IN (SELECT title from avg_of_user_reviews WHERE idvscore >= 70)
        GROUP BY m.title
        LIMIT 1150;
        """)

        self._EXPERT_REVIEW_BOX_OFFICE_VIEW = text("""
        CREATE OR REPLACE VIEW :view_name AS
        SELECT m.title, AVG(s.worldwide_box_office) as worldwide_box_office_avg
        FROM movie m
                 JOIN sale s ON s.movie_title = m.title AND s.worldwide_box_office IS NOT NULL AND
                                m.title IN (SELECT title from avg_of_expert_reviews WHERE idvscore >= 70)
                 LEFT JOIN :relation_view_name gurboi on m.title = gurboi.title
        WHERE gurboi.title IS NULL
        GROUP BY m.title
        LIMIT 1150;
        """)

        self._EXPERT_BOX_OFFICE_QUERY = "SELECT * FROM good_expert_reviews_box_office_information"
        self._USER_BOX_OFFICE_QUERY = "SELECT * FROM good_user_reviews_box_office_information"

    def _check_view_existence(self, view_name):
        with engine.connect() as connection:
            result = connection.execute(self._CHECK_VIEW_QUERY, {"view_name": view_name})

            return result.scalar()

    def _create_view(self, view_query, view_name, relation_view_name=None):
        if not self._check_view_existence(view_name):
            with engine.connect() as connection:
                connection.execute(view_query, {'view_name': view_name, 'relation_view_name': relation_view_name})

    def _create_views(self):
        self._create_view(self._USER_REVIEW_BOX_OFFICE_VIEW, self._USER_REVIEW_VIEW_NAME)
        self._create_view(self._EXPERT_REVIEW_BOX_OFFICE_VIEW, self._EXPERT_REVIEW_VIEW_NAME,
                          self._USER_REVIEW_VIEW_NAME)

    def get_user_reviews_box_office_dataset(self):
        self._create_views()
        return pd.read_sql(self._USER_BOX_OFFICE_QUERY, engine)[self._WORLDWIDE_BOX_OFFICE_COLUMN].to_numpy()

    def get_expert_reviews_box_office_dataset(self):
        self._create_views()
        return pd.read_sql(self._EXPERT_BOX_OFFICE_QUERY, engine)[self._WORLDWIDE_BOX_OFFICE_COLUMN].to_numpy()
