-- CS 121 Winter 2022 Final Project
-- Part B: DDL

DROP DATABASE IF EXISTS booksdb;
CREATE DATABASE booksdb;
USE booksdb;

-- Maintain referential integrity when dropping tables, keeping in mind foreign
-- key constraints.  
-- DROP TABLE IF EXISTS books;
-- DROP TABLE IF EXISTS authors, genres, book_details, ratings, to_read;

-- This table holds information with the most essential information about each
-- book, including isbn (which serves as a unique book id), original title, etc. 
CREATE TABLE books (
    -- Unique identifier for each book, stands for International Standard Book
    -- Number. An ISBN is assigned to each separate edition and variation of a 
    -- publication.
    isbn_10                 CHAR(10)    NOT NULL,
    -- Original title of publication.
    orig_title              VARCHAR(200) NOT NULL,
    -- Original year of publication.
    -- Using SMALLINT since YEAR has a limited range (after 1900 only)
    orig_publication_yr     SMALLINT,
    -- A short language code which identifies the language in which the 
    -- book was published.
    language_code           VARCHAR(5) NOT NULL,
    PRIMARY KEY (isbn_10),
    CHECK (orig_publication_yr >= 0)
);

-- This table holds isbn_10's and authors for different books.
-- In the ER model, corresponds to a multi-valued attribute.
CREATE TABLE authors (
    -- Unique identifier for each book.
    isbn_10     CHAR(10)    NOT NULL,
    -- Author associated with the book. Note that there may be multiple authors
    -- associated with one book.
    author      VARCHAR(50) NOT NULL,
    PRIMARY KEY (isbn_10, author),
    FOREIGN KEY (isbn_10) REFERENCES books(isbn_10)
        ON UPDATE CASCADE ON DELETE CASCADE
);

-- This table holds isbn_10's and genres for different books.
-- In the ER model, corresponds to a multi-valued attribute.
CREATE TABLE genres (
    -- Unique identifier for each book.
    isbn_10     CHAR(10)    NOT NULL,
    -- Genre associated with the book. Note that there may be multiple genres
    -- associated with one book.
    genre       VARCHAR(50) NOT NULL,
    PRIMARY KEY (isbn_10, genre),
    FOREIGN KEY (isbn_10) REFERENCES books(isbn_10)
        ON UPDATE CASCADE ON DELETE CASCADE
);

-- This table holds additional information about each book which may not be
-- as critical, such as story descriptions, pages, and genres.
CREATE TABLE book_details (
    -- Unique identifier for each book.
    isbn_10             CHAR(10)        NOT NULL,
    -- A brief description of the book's contents. Serves as a kind of summary 
    -- or synopsis. Not every book may have this, so we allow it to be null.
    book_description    VARCHAR(6000),
    -- The number of pages each book has.
    num_pages           INT,
    -- The number of comments the book has received on goodreads
    num_comments        INT,
    -- The number of editions of the book which have been released
    num_editions        INT,
    PRIMARY KEY (isbn_10),
    FOREIGN KEY (isbn_10) REFERENCES books(isbn_10)
        ON UPDATE CASCADE ON DELETE CASCADE
);

-- This table holds information about the ratings which users give to books.
CREATE TABLE ratings (
    -- A unique user_id used to identify users within goodreads.
    user_id     INT         NOT NULL,
    -- Unique identifier for each book.
    isbn_10     CHAR(10)    NOT NULL,
    -- Rating given to a book by a user, out of 5 stars.
    rating      TINYINT     NOT NULL,
    PRIMARY KEY (user_id, isbn_10),
    FOREIGN KEY (isbn_10) REFERENCES books(isbn_10)
        ON UPDATE CASCADE ON DELETE CASCADE,
    CHECK (1 <= rating <= 5)
);

-- This table holds information about the books that users have on their 
-- 'to read' list, which is to say books that they plan on reading.
-- Both customers and bookstore managers have the potential to use this data
-- for different purposes. 
CREATE TABLE to_read (
    -- A unique user_id used to identify users within goodreads.
    user_id     INT         NOT NULL,
    -- Unique identifier for each book.
    isbn_10     CHAR(10)    NOT NULL,
    PRIMARY KEY (user_id, isbn_10),
    FOREIGN KEY (isbn_10) REFERENCES books(isbn_10)
        ON UPDATE CASCADE ON DELETE CASCADE
);

-- An index on orig_publication_yr, since we expect searches and queries
-- related to the publication year.
CREATE INDEX idx_year ON books(orig_publication_yr);