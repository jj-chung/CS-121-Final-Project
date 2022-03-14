-- CS 121 Winter 2022 Final Project
-- Part H: SQL Queries

-- Get all the books made in a particular year, genre, and language
SELECT orig_title 
    FROM books NATURAL JOIN genres
    WHERE genre = chosen_genre AND language = chosen_language
    AND orig_publication_yr = chosen_year;

-- Get the number of ratings for each author, sorted by most to least rated
SELECT COUNT(*) as num_ratings  
    FROM books NATURAL JOIN ratings NATUIRAL JOIN authors
    GROUP BY author
    ORDER BY num_ratings;

-- Get the highest-rated book titles in each genre and year, sort from oldest 
-- to newest
WITH 
(
    SELECT genre, orig_publication_yr, MAX(get_avg_rating(isbn_13)) as max_rating
        FROM books NATURAL JOIN ratings NATURAL JOIN genres
        GROUP BY genre, orig_publication_yr
        ORDER BY orig_publication_yr;
)
AS max_ratings
SELECT orig_title
    FROM max_ratings JOIN books ON (max_ratings.genre = book_details.genre AND
        max_ratings.year = books.orig_publication_yr AND
        max_rating = ratings.rating);
