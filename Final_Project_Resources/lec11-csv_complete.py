'''
CSV Examples, extended from Wednesday's lecture.
See bottom of file for some practice exercises.
Some example data can be found in lec11-data.zip
'''
import csv

with open('csv_example.csv') as csvfile:
  reader = csv.DictReader(csvfile)
  for row in reader:
    print(row) # first row printed is header

# An improved version with some nice formatting. Sometimes
# we want to format datasets nicely in processing programs
# for users.
with open('csv_example.csv') as csvfile:
  reader = csv.reader(csvfile)
  line_number = 0
  for row in reader:
    print(' | '.join(row)) # format each element in row nicely
    # ' | '.join(['A', 'B', C'] -> 'A | B | C'
    if line_number == 0: # format header nicely
      print('-' * 25)
    line_number += 1

# Example of writing a new CSV file with csv.writer (usually
# csv.DictWriter is preferred, but this works too)
with open('data/new_csv.csv', 'w') as csvfile:
  usernames = {('El', 'Hovik') : 'hovik', 
               ('Gavin', 'McCabe') : 'gmccabe'}
  columns = ['first', 'last', 'email']
  writer = csv.writer(csvfile)
  writer.writerow(columns) # first row should be written as column names
  # The code below is just like the solution from the dictionary part of lecture
  # only saving the results to a CSV file instead of printing, which
  # is more representative of an actual Python utility program.
  for key in usernames:
    first, last = key # tuple-unpacking!
    username = usernames[key]
    writer.writerow([first, last, username])
  
# Example using csv.DictReader with staff data downloaded 
# as .csv file from Google Sheets!
# We have multiple columns in the CSV file, but only work
# with what we need here using the dictionary keys as column
# names in the first (header) row seen in data/cs1staff.csv
with open('data/cs1staff.csv', 'r') as csvfile:
  reader = csv.DictReader(csvfile)
  email_file = open('data/cs1staff_emails.csv', 'w')
  writer = csv.DictWriter(email_file, fieldnames = ['email'])
  writer.writeheader() # uses fieldnames
  for row in reader:
    # DictWriter's writerow() method expects a key/value dictionary where
    # keys match the column names specified by fieldnames above.
    writer.writerow({'email' : row['Username'] + '@caltech.edu'})
  # Don't forget to close the file since
  # we opened this one without `with`!
  email_file.close() 

# Example motivated by our first problem posed in lecture
# to take a dataset with staff info (including usernames) and 
# use each username based on the Username column to 
# write a new CSV file (with a single 'email' column)
# with each row having a staff member's email based on <username>@caltech.edu
# This is a very simple csv file we're writing, but there's a lot
# more we could do!
with open('cs1staff.csv', 'r') as csvfile:
  reader = csv.DictReader(csvfile)
  email_file = open('cs1staff_emails.csv', 'w')
  writer = csv.DictWriter(email_file, fieldnames = ['email'])
  writer.writeheader() # uses fieldnames
  for row in reader:
    writer.writerow({'email' : row['Username'] + '@caltech.edu'})
  email_file.close()

# Exercises
# cs1staff.csv
# 1. Print all emails using <username>, one per line
# 2. Print full names as <First> <Last> (<Role>)
# 3. Use 1. to write all emails to a new file, cs1staff_emails.csv with a column called 'email'
# 4. Write a function to return the full name of the TA as a string who has the most quarters TAd (must have role TA or Head TA)
# 5. Write a function to return a list of all TA names who have a given house name.

# nobel_prizes.csv
# 1. Write a function to print the name and motivation for all winners of a specific category
# 2. Write a function to return a list of all names of winners of a specific year

# dictionary.csv
# 1. Write a function to return the definitions of a given word, ignoring letter-casing
# Can you think of others?