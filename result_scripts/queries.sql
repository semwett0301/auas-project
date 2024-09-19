-- Gwen

select * FROM public."Award";
select * FROM public."Award_movie";
select * FROM public."movie ;
select * FROM public."Review";

-- GWEN filter out only the relevant colomns of the movie table and leave out release date
SELECT "title",
"worldwide_box_office",
"international_box_office",
"domestic_box_office" FROM public."movie" AS "movie_box_office";

-- GWEN filter reviews by users
SELECT "title",
"idvscore" FROM public."Review"
WHERE "role" = 'user';

-- GWEN Aggregate review scores per movie
SELECT "title", ROUND (AVG("idvscore"),0) AS average_score
FROM public."Review"
WHERE 
    "role" = 'user'
GROUP BY 
    "title"
	
-- GWEN innerjoin movie table with review table and the review scores with box office data
SELECT 
    movie_box_office."title",
    movie_box_office."worldwide_box_office",
    movie_box_office."international_box_office",
    movie_box_office."domestic_box_office",
    user_avg_scores.average_score
FROM (
    SELECT 
        "title",
        "worldwide_box_office",
        "international_box_office",
        "domestic_box_office"
    FROM public."movie"
) AS movie_box_office
INNER JOIN (
    SELECT 
        "title", 
        ROUND(AVG("idvscore"), 0) AS average_score
    FROM public."Review"
    WHERE 
        "role" = 'user'
    GROUP BY 
        "title"
) AS user_avg_scores
ON movie_box_office."title" = user_avg_scores."title";

-- GWEN correlation between high and low review scores to measure the relation between box office sales.
WITH movie_data AS (
    SELECT 
        movie_box_office."title",
        movie_box_office."worldwide_box_office",
        movie_box_office."international_box_office",
        movie_box_office."domestic_box_office",
        CASE 
            WHEN user_avg_scores.average_score >= 70 THEN 'high'
            ELSE 'low'
        END AS score_category,
        user_avg_scores.average_score
    FROM (
        SELECT 
            "title",
            "worldwide_box_office",
            "international_box_office",
            "domestic_box_office"
        FROM public."movie"
    ) AS movie_box_office
    INNER JOIN (
        SELECT 
            "title", 
            ROUND(AVG("idvscore"), 0) AS average_score
        FROM public."Review"
        WHERE 
            "role" = 'user'
        GROUP BY 
            "title"
    ) AS user_avg_scores
    ON movie_box_office."title" = user_avg_scores."title"
)
SELECT 
    score_category,
    corr(movie_data.average_score, movie_data.worldwide_box_office) AS correlation_worldwide,
    corr(movie_data.average_score, movie_data.international_box_office) AS correlation_international,
    corr(movie_data.average_score, movie_data.domestic_box_office) AS correlation_domestic
FROM movie_data
GROUP BY score_category;

--GWEN to measure the direct correlation between the variables average user review score and box office
WITH movie_data AS (
    SELECT 
        movie_box_office."title",
        movie_box_office."worldwide_box_office",
        user_avg_scores.average_score
    FROM (
        SELECT 
            "title",
            "worldwide_box_office"
        FROM public."movie"
    ) AS movie_box_office
    INNER JOIN (
        SELECT 
            "title", 
            ROUND(AVG("idvscore"), 0) AS average_score
        FROM public."Review"
        WHERE 
            "role" = 'user'
        GROUP BY 
            "title"
    ) AS user_avg_scores
    ON movie_box_office."title" = user_avg_scores."title"
)
SELECT 
    corr(movie_data.average_score, movie_data.worldwide_box_office) AS general_correlation_worldwide
FROM movie_data;





