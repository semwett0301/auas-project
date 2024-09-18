CREATE TABLE IF NOT EXISTS movie
(
    title                    varchar(512) PRIMARY KEY,
    release_date             date NOT NULL
);

CREATE TABLE IF NOT EXISTS sale (
    id SERIAL PRIMARY KEY,
    movie_title varchar(512) REFERENCES movie NOT NULL,
    worldwide_box_office     bigint,
    domestic_box_office      bigint,
    international_box_office bigint
);

CREATE TABLE IF NOT EXISTS award
(
    name varchar(256) PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS award_movie
(
    id          SERIAL PRIMARY KEY,
    movie_title varchar(512) REFERENCES movie NOT NULL,
    award_name  varchar(256) REFERENCES award NOT NULL
);

CREATE TYPE REVIEW_ROLE AS ENUM ('user', 'expert');

CREATE TABLE IF NOT EXISTS review
(
    id          SERIAL PRIMARY KEY,
    movie_title varchar(512) REFERENCES movie NOT NULL,
    idvscore    int                           NOT NULL CHECK ( idvscore >= 0 ),
    role        REVIEW_ROLE                   NOT NULL
);



