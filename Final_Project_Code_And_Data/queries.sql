-- CS 121 Winter 2022 Final Project
-- Part H: SQL Queries

-- [Query 1]
-- Users can fetch books that are most suited to them
-- Retrieve all fantasy books written in english after 2010

SELECT orig_title 
    FROM books NATURAL JOIN genres
    WHERE genre = "fantasy" AND language_code = "eng"
    AND orig_publication_yr > 2010;

-- [Query 2]
-- Users can get descriptions for books of interest
-- Retrieve descriptions of all books related to the Harry Potter series
SELECT orig_title, book_description
    FROM books NATURAL JOIN book_details 
    WHERE orig_title LIKE "%Harry Potter%";


-- [Query 3]
-- For genres with foreign language books,
-- get the percentage of books not written in English, from highest to lowest

SELECT genre, (foreign_books_count/genre_count) as foreign_books_percent FROM 
    (SELECT genre, COUNT(*) as foreign_books_count
    FROM books NATURAL JOIN genres
    WHERE language_code != "eng"
    GROUP BY genre) as foreign_books
NATURAL JOIN 
    (SELECT genre, COUNT(*) as genre_count
    FROM books NATURAL JOIN genres
    GROUP BY genre) as all_books
ORDER BY foreign_books_percent DESC;

-- [Query 4]
-- Get the longest book by every author, in alphabetical order by author
-- This query requires the additional info in the book_details table

SELECT author, orig_title FROM
(
    SELECT author, MAX(num_pages) AS max_page_amount
    FROM books NATURAL JOIN book_details NATURAL JOIN authors
    GROUP BY author) AS max_pages
NATURAL JOIN
(
    SELECT orig_title, author, num_pages
    FROM authors NATURAL JOIN books NATURAL JOIN book_details) AS book_lengths
    WHERE num_pages = max_page_amount
    ORDER BY author;

-- [Query 5]
-- Get all authors who have published in the 20th century and the most recent 
-- year they published
-- ALSO IN RELATIONAL ALGEBRA

SELECT author, MAX(orig_publication_yr) AS last_publish
    FROM authors NATURAL JOIN books
    GROUP BY author
    HAVING last_publish > 2000
    ORDER BY last_publish DESC;

-- [Query 6]
-- Get the top 10 most critically acclaimed authors by finding those with the 
-- highest average rating 

SELECT author, AVG(rating) average_rating
    FROM books NATURAL JOIN ratings NATURAL JOIN authors
    GROUP BY author
    ORDER BY average_rating DESC
    LIMIT 10;

-- [Query 7]
-- Get the number of ratings for each author, sorted by most to least rated, 
-- to find the authors who the most people have read
-- ALSO IN RELATIONAL ALGEBRA

SELECT author, COUNT(*) AS num_ratings  
    FROM books NATURAL JOIN ratings NATURAL JOIN authors
    GROUP BY author
    ORDER BY num_ratings DESC;

-- [Query 8]
-- To find new releases to read, search the books written in the last 7 years
-- that are most common on people's too read list

SELECT isbn_10, orig_title, COUNT(*) AS read_list_count
    FROM to_read
    NATURAL JOIN books
    WHERE orig_publication_yr > 2015
    GROUP BY isbn_10
    ORDER BY read_list_count DESC;

-- [Query 9]
-- Find the most commonly rated book in each genre
WITH total_ratings AS
(
    SELECT isbn_10, COUNT(*) AS num_ratings
        FROM ratings 
        GROUP BY isbn_10
)
SELECT genre, orig_title FROM
    (SELECT genre, MAX(num_ratings) AS num_ratings 
        FROM total_ratings NATURAL JOIN genres 
        GROUP BY genre) AS max_book_ratings
    NATURAL JOIN
    (SELECT genre, isbn_10, num_ratings, orig_title 
        FROM total_ratings NATURAL JOIN genres 
        NATURAL JOIN books) AS all_book_ratings;

-- [Query 10]
-- Find the highest rated book in each genre
WITH avg_ratings AS
(
    SELECT isbn_10, avg(rating) AS avg_rating
        FROM ratings 
        GROUP by isbn_10
)
SELECT genre, orig_title FROM
    (SELECT genre, MAX(avg_rating) AS avg_rating 
        FROM avg_ratings NATURAL JOIN genres 
        GROUP BY genre) AS max_book_ratings
    NATURAL JOIN
    (SELECT genre, isbn_10, avg_rating, orig_title 
        FROM avg_ratings NATURAL JOIN genres 
        NATURAL JOIN books) AS all_book_ratings;

-- [Query 11]
-- Get the highest-rated book titles in each genre and year, 
-- sort from oldest to newest
-- this query makes use of our UDF
WITH max_ratings AS
(
    SELECT genre, orig_publication_yr, 
        MAX(get_avg_rating(isbn_10)) AS max_rating
        FROM books NATURAL JOIN ratings NATURAL JOIN genres
        GROUP BY genre, orig_publication_yr
        ORDER BY orig_publication_yr;
)
SELECT orig_title
    FROM max_ratings JOIN books ON (max_ratings.genre = book_details.genre AND
        max_ratings.year = books.orig_publication_yr AND
        max_rating = ratings.rating);
