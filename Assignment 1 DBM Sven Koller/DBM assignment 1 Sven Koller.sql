SELECT 
    filtered_awards."award_name", 
    filtered_movies."title", 
    filtered_movies."worldwide_box_office", 
    filtered_movies."international_box_office", 
    filtered_movies."domestic_box_office"
FROM 
    (SELECT "award_name", "movie_title" 
     FROM public."Award_movie") AS filtered_awards
full JOIN 
    (SELECT "title", "worldwide_box_office", "international_box_office", "domestic_box_office" 
     FROM public."Movie") AS filtered_movies
ON 
    filtered_awards."movie_title" = filtered_movies."title";

-- Avarage office sales with award
SELECT 
    'With Award' AS category, 
    AVG(filtered_movies."worldwide_box_office") AS avg_worldwide_box_office, 
    AVG(filtered_movies."domestic_box_office") AS avg_domestic_box_office, 
    AVG(filtered_movies."international_box_office") AS avg_international_box_office
FROM 
    (SELECT "award_name", "movie_title" 
     FROM public."Award_movie") AS filtered_awards
JOIN 
    (SELECT "title", "worldwide_box_office", "international_box_office", "domestic_box_office" 
     FROM public."Movie") AS filtered_movies
ON 
    filtered_awards."movie_title" = filtered_movies."title"
WHERE 
    filtered_awards."award_name" IS NOT NULL

UNION ALL

-- Average for movies with no awards
SELECT 
    'Without Award' AS category, 
    AVG(filtered_movies."worldwide_box_office") AS avg_worldwide_box_office, 
    AVG(filtered_movies."domestic_box_office") AS avg_domestic_box_office, 
    AVG(filtered_movies."international_box_office") AS avg_international_box_office
FROM 
    (SELECT "title", "worldwide_box_office", "international_box_office", "domestic_box_office" 
     FROM public."Movie") AS filtered_movies
LEFT JOIN 
    (SELECT "movie_title" 
     FROM public."Award_movie") AS filtered_awards
ON 
    filtered_movies."title" = filtered_awards."movie_title"
WHERE 
    filtered_awards."movie_title" IS NULL;




