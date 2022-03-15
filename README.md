# CS-121-Final-Project
CS 121 Winter 2022 Final Project.

## Data Origin and Description
Our data set comes from the [goodbooks-10k dataset](https://github.com/malcolmosh/goodbooks-10k-extended/blob/master/README.md), an extended version of 
the [original goodbooks dataset](https://github.com/zygmuntz/goodbooks-10k) 
which was scraped from the Goodreads API in September 2017. The dataset contains 
information on the 10,000 most popular books on goodreads when it was collected. 
We selected columns that were most relevant to our application and renamed 
certain columns for more clarity. We have also limited our focus to the first
3k books in the original books_enriched.csv file for the purposes of this project 
(which are the 3k most popular books in the dataset according to the original data 
description).

We have created 5 .csv files using the .csv files from the original goodbooks
dataset, each described below:
- books.csv
    - ```isbn_10```: Unique identifier for each book, stands for International 
    Standard Book Number. An ISBN is assigned to each separate edition and 
    variation of a publication.
    - ```orig_title```: Original title of publication.
    - ```orig_publication_yr```: Original year of publication.
    - ```language_code```: A short language code which identifies the language 
    in which the book was published.

- book_details.csv
    - ```isbn_10```: See books.csv.
    - ```book_description```: A brief description of the book's contents. 
    Serves as a kind of summary or synopsis. Not every book may have this, so we 
    allow it to be null.
    - ```num_pages```: A brief description of the book's contents. Serves as a 
    kind of summary or synopsis. 
    - ```num_comments```: The number of comments the book has received on 
    goodreads.
    - ```num_editions```: The number of editions of the book which have been 
    released.

- authors.csv
    - ```isbn_10```: See books.csv.
    - ```author```: Author associated with the book. Note that there may be 
    multiple authors associated with one book.

- genres.csv
    - ```isbn_10```: See books.csv.
    - ```genre```: Genre associated with the book. Note that there may be 
    multiple genres associated with one book.

- ratings.csv
    - ```user_id```: A unique user_id used to identify users within goodreads.
    - ```isbn_10```: See books.csv.
    - ```rating```: Rating given to a book by a user, out of 5 stars. A rating 
    must be at minimum one star.

- to_read.csv
    - ```user_id```: See ratings.csv.
    - ```isbn_10```: See books.csv.

## Instructions for loading our data from the command-line in MySQL
After cloning this repository using ```git clone``` or downloading this 
repository, 
1. Start mysql. Then within mysql:
2. Setup the database and tables using ```source setup.sql```
3. Load the data using ```source load-data.sql```
4. Create database password management using ```source setup-passwords.sql```
5. Create database routines using ```source setup-routines.sql``` 
6. Create client permissions by using ```source grant-permissions.sql```
7. Quit mysql using ```quit```
8. In the main command line, use ```python3 app.py``` to begin the app (see 
below for specific instructions on running our Python program).

## Instructions for running our Python program
