-- CS 121 Winter 2022 Final Project
-- Part I: Procedural SQL

-- A UDF that will get the average rating for any book the database.
-- The UDF can take any book isbn_10 identifier as the input and find the 
-- average of all ratings of that book via the ratings table. This can be used
-- to identify which books have high or low ratings.
DROP FUNCTION IF EXISTS get_average_rating;

DELIMITER !
CREATE FUNCTION get_average_rating(input_isbn_10 CHAR(10)) 
RETURNS NUMERIC(5, 2) DETERMINISTIC
BEGIN
    DECLARE avg_rating INT;

    SELECT AVG(rating) 
        FROM ratings
        WHERE isbn_10 = input_isbn_10
    INTO avg_rating;

    RETURN avg_rating;
END !
DELIMITER ;

-- This procedure takes a user_id and an author name, and adds the highest
-- (average) rated book by that author to the user's to_read collection by 
-- adding (user_id, isbn_10) to to_read, where the isbn_10 is the identifier of 
-- the book.
DROP PROCEDURE IF EXISTS add_highest_rated_book;

DELIMITER !
CREATE PROCEDURE add_highest_rated_book(
    in_user_id INT, 
    input_author VARCHAR(50)
)
BEGIN
    -- The isbn_10 identifier of the highest rated book by the specified author
    DECLARE highest_rated_isbn_10_by_author CHAR(10);

    -- author_book_ratings is a table of all books and ratings by the specified
    -- author
    WITH 
    (
        SELECT isbn_10, rating 
            FROM ratings
            where author = input_author;
    )
    AS author_book_ratings
        -- We select the book(s) which have the highest rating 
        SELECT isbn_10
            FROM author_book_ratings 
            WHERE rating = (SELECT MAX(rating) from author_book_ratings)
            -- If there are multiple books which have the highest rating, we 
            -- select the first book from our query
            LIMIT 1
        INTO highest_rated_isbn_10_by_author

    INSERT INTO to_read(user_id, isbn_10)
        VALUES (in_user_id, highest_rated_isbn_10_by_author)
        
END !
DELIMITER ;

-- We write the table definition for the materialized results mv_book_stats,
-- which contains stats about a book's ratings.
CREATE TABLE mv_book_stats 
(
    isbn_10     CHAR(10) PRIMARY KEY
    num_ratings INT NOT NULL,
    total_stars INT NOT NULL
);

-- The initial SQL DML statement to populate the materialized view table 
-- mv_book_stats.
INSERT INTO mv_book_stats(
    SELECT isbn_10,
        COUNT(*),
        SUM(ratings)
    FROM ratings GROUP BY isbn_10
);

-- Write the view definition for book_stats.
CREATE VIEW book_stats AS
    SELECT isbn_10,
        num_ratings,
        total_stars,
        total_stars / num_ratings AS avg_rating
    FROM mv_book_stats;

-- A procedure to execute when inserting a new isbn_10 and rating
-- to the book stats materialized view (mv_book_stats).
-- If an isbn_10 is already in view, the associated information is updated.
CREATE PROCEDURE sp_book_stats_new_rating(
    new_isbn_10 CHAR(10),
    new_rating INT
)
BEGIN 
    INSERT INTO mv_book_stats 
        -- isbn_10 not already in view; add row
        VALUES (new_isbn_10, 1, new_rating)
    ON DUPLICATE KEY UPDATE 
        -- isbn_10 already in view; update existing row
        num_ratings = num_ratings + 1,
        total_stars = total_stars + new_rating;
END !

-- Handles new rows added to ratings table, updates stats accordingly
CREATE TRIGGER trg_ratings_insert AFTER INSERT
       ON ratings FOR EACH ROW
BEGIN
    CALL sp_book_stats_new_rating(NEW.isbn_10, NEW.rating);
END !
DELIMITER ;


-- Trigger (and related procedures) to handle deletes.
DELIMITER !

CREATE PROCEDURE sp_book_stats_del_rating(
    old_isbn_10 VARCHAR(15),
    old_rating NUMERIC(12, 2)
)
BEGIN
    -- If the number of ratings is only 1, remove the isbn_10 from the 
    -- summary table
    DELETE FROM mv_book_stats 
        WHERE isbn_10 = old_isbn_10 AND num_ratings = 1;

    -- If the isbn_10 is still in the summary table (meaning there was already
    -- at least one rating)
    IF old_isbn_10 IN (SELECT isbn_10 FROM mv_book_stats)
        THEN UPDATE mv_book_stats
            SET num_ratings = num_ratings - 1,
                total_stars = total_stars - old_rating
            WHERE  isbn_10 = old_isbn_10;
    END IF;

END !

-- Handles when rows are deleted from ratings table, updates stats accordingly
CREATE TRIGGER trg_ratings_delete AFTER DELETE
       ON ratings FOR EACH ROW
BEGIN
    CALL sp_book_stats_del_rating(OLD.isbn_10, OLD.rating);
END !
DELIMITER ;


-- Trigger (and related procedures) to handle updates.
DELIMITER !

-- Handles when updates are made to the ratings table, updates stats accordingly
CREATE TRIGGER trg_ratings_update AFTER UPDATE
       ON ratings FOR EACH ROW
BEGIN
    IF OLD.isbn_10 = NEW.isbn_10
        THEN UPDATE mv_book_stats 
            SET total_stars = total_stars + NEW.rating - OLD.rating
            WHERE isbn_10 = NEW.isbn_10;
    ELSE
        CALL sp_book_stats_new_rating(NEW.isbn_10, NEW.rating);
        CALL sp_book_stats_del_rating(OLD.isbn_10, OLD.rating);
    END IF;
END !
DELIMITER ;