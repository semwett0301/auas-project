-- Displaying only the columns that I need
-- Naming it AS movie_box_office (WENDY)
SELECT "title" , "worldwide_box_office" ,
"international_box_office" , "domestic_box_office" 
FROM public."Movie" AS movie_box_office ;

-- Displaying only the culumns that I need (WENDY)
SELECT "title" , "idvscore"  FROM public."Review"
WHERE "role" = 'expert' ;

-- Making the score an average,
-- leaving me with an average score of every movie (WENDY)
SELECT *
FROM (
    SELECT "title", ROUND(AVG("idvscore"), 0) AS average_score
    FROM public."Review"
    WHERE "role" = 'expert'
    GROUP BY "title"
) AS expert_avg_scores;

-- INNER joining the filterd Movie table unto the filtered Review table (WENDY)
SELECT  movie_box_office."title",
    "worldwide_box_office",
    "international_box_office",
    "domestic_box_office",
    "average_score"
FROM (
    SELECT "title", "worldwide_box_office", 
	"international_box_office", "domestic_box_office" 
    FROM public."Movie"
) AS movie_box_office
INNER JOIN (
    SELECT "title", ROUND(AVG("idvscore"), 0) AS average_score
    FROM public."Review"
    WHERE "role" = 'expert'
    GROUP BY "title"
) AS expert_avg_scores
ON movie_box_office."title" = expert_avg_scores."title";


