SELECT title,
       release_date,
       worldwide_box_office,
       international_box_office,
       domestic_box_office,
       CASE 
           WHEN EXTRACT(MONTH FROM release_date) IN (6, 7, 8, 11, 12) THEN 'Peak Season'
           ELSE 'Off-Peak Season'
       END AS season
FROM "Movie";
SELECT season,
       SUM(worldwide_box_office) AS total_worldwide_box_office,
       AVG(worldwide_box_office) AS avg_worldwide_box_office
FROM (
       SELECT title,
              release_date,
              worldwide_box_office,
              international_box_office,
              domestic_box_office,
              CASE 
                  WHEN EXTRACT(MONTH FROM release_date) IN (6, 7, 8, 11, 12) THEN 'Peak Season'
                  ELSE 'Off-Peak Season'
              END AS season
       FROM "Movie"
     ) AS season_data
GROUP BY season;

SELECT season,
       SUM(domestic_box_office) AS total_domestic_box_office,
       AVG(domestic_box_office) AS avg_domestic_box_office
FROM (
       SELECT title,
              release_date,
              worldwide_box_office,
              international_box_office,
              domestic_box_office,
              CASE 
                  WHEN EXTRACT(MONTH FROM release_date) IN (6, 7, 8, 11, 12) THEN 'Peak Season'
                  ELSE 'Off-Peak Season'
              END AS season
       FROM "Movie"
     ) AS season_data
GROUP BY season;
SELECT season,
       SUM(international_box_office) AS total_international_box_office,
       AVG(international_box_office) AS avg_international_box_office
FROM (
       SELECT title,
              release_date,
              worldwide_box_office,
              international_box_office,
              domestic_box_office,
              CASE 
                  WHEN EXTRACT(MONTH FROM release_date) IN (6, 7, 8, 11, 12) THEN 'Peak Season'
                  ELSE 'Off-Peak Season'
              END AS season
       FROM "Movie"
     ) AS season_data
GROUP BY season;
