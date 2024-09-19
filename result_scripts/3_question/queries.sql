-- Semen Mokrov

-- This is an auxiliary file for viewing VIEWS created in the encapsulator
-- Only some useful queries implemnented in init.sql file
-- The logic of the queries being processed is explained here

-- I create a limit of 1150 rows because in the results of each query there is no more than 2300 rows
-- It's possible to mention that the both views contains data about different films
-- Therefore, in order to get two equal records and independent datasets, I set a limit just above half of the final result
CREATE OR REPLACE VIEW good_user_reviews_box_office_information AS
SELECT m.title, AVG(s.worldwide_box_office) as worldwide_box_office_avg
FROM movie m
         JOIN sale s ON s.movie_title = m.title AND s.worldwide_box_office IS NOT NULL AND
                        m.title IN (SELECT title from avg_of_user_reviews WHERE idvscore >= 70)
GROUP BY m.title
LIMIT 1150;

CREATE OR REPLACE VIEW good_expert_reviews_box_office_information AS
SELECT m.title, AVG(s.worldwide_box_office) as worldwide_box_office_avg
FROM movie m
         JOIN sale s ON s.movie_title = m.title AND s.worldwide_box_office IS NOT NULL AND
                        m.title IN (SELECT title from avg_of_expert_reviews WHERE idvscore >= 70)
         LEFT JOIN good_user_reviews_box_office_information gurboi on m.title = gurboi.title
WHERE gurboi.title IS NULL
GROUP BY m.title
LIMIT 1150;

-- This code can be used to obtain average values for calculating the increment
-- However, during the analysis this is done at the level of the programming language
SELECT AVG(worldwide_box_office_avg)
FROM good_expert_reviews_box_office_information;

SELECT AVG(worldwide_box_office_avg)
FROM good_user_reviews_box_office_information;

SELECT *
FROM good_user_reviews_box_office_information;

SELECT *
FROM good_expert_reviews_box_office_information
