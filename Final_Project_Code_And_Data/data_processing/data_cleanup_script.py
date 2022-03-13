# CS 121 Winter 2022 Final Project

import csv

# Data cleaning script
def remove_list_values(old_filename, new_filename):
    with open(old_filename, 'r', encoding="utf-8") as f_in, \
        open(new_filename, 'w', newline='', encoding="utf-8") as f_out:
        csv_out = csv.writer(f_out)
        for row in csv.reader(f_in):
            items_list = row[-1].strip('][').split(', ')
            clean_list = []
            for item in items_list:
                clean_list.append(item.replace('\'', ''))
            for i in clean_list:
                csv_out.writerow(row[:-1] + [i])


# Map every instance of book_id to its corresponding isbn_13 number in ratings
# and to_read
def convert_ids(input_filename, output_filename, book_id_to_isbn_13):
    with open(input_filename, 'r', encoding="utf-8") as f_in, \
        open(output_filename, 'w', newline='', encoding="utf-8") as f_out:
        csv_out = csv.writer(f_out)
        for row in csv.reader(f_in):
            for i in row[-1].split():
                isbn_13 = book_id_to_isbn_13[row[1]]
                csv_out.writerow(row[:1] + [isbn_13] + row[2:])
                
if __name__ == "__main__":
    # Modify genres.csv and authors.csv to have one book and one author per 
    # row
    remove_list_values('genres.csv', 'new_genres.csv')
    remove_list_values('authors.csv', 'new_authors.csv')

    # From books.csv, creating a dictionary from book_id to isbn_13
    book_id_to_isbn_13 = {}
    filename = 'books_enriched_copy.csv'

    with open(filename, 'r') as csvfile:
        datareader = csv.reader(csvfile)
        for row in datareader:
            books_row = list(row)
            book_id = books_row[0]
            isbn_13 = books_row[1]
            book_id_to_isbn_13[book_id] = isbn_13

    # Modify ratings and to_read to use isbn_13 instead of book_id
    convert_ids('ratings.csv', 'new_ratings.csv', book_id_to_isbn_13)
    convert_ids('to_read.csv', 'new_to_read.csv', book_id_to_isbn_13)