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
CREATE PROCEDURE add_highest_rated_book(user_id INT, input_author VARCHAR(50))
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
        INTO highest_rated_isbn_10_by_author;

    -- Insert the new to read info to to_read
    INSERT INTO to_read(user_id, isbn_10)
        
END !
DELIMITER ;

-- This trigger will  