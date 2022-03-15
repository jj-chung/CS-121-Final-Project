"""
Brief overview of application:
Our application allows user to navigate the books database. Users are able
to search books using specific search criteria, including genre, publication 
year, author, ratings, and more. 

Users are also able to perform other actions, such as add a rating of a book
to the database, or add a book to their "to-read" shelf by adding an entry
to the to-read table.

Users can also view information pertaining to popular series in the database,
such as the Harry Potter series, the Twilight Series, and more. 

Users can also be recommended a book by entering a book they liked. Then,
a similar book will be recommended by extracting information about the book they
liked, given that it is in the database.

Meanwhile, admin users can target specific readers and recommend them books
by accessing their top-rated or to-read books. They may also view top-rated
books within a specific timeframe to analyze the market for books.

Names: Amelia Whitworth, Jennie Chung
Emails: awhirwor@caltech.edu, jjchung@caltech.edu 
"""
from ssl import _PasswordType
import sys  # to print error messages to sys.stderr
import mysql.connector
# To get error codes from the connector, useful for user-friendly
# error-handling
import mysql.connector.errorcode as errorcode

# Debugging flag to print errors when debugging that shouldn't be visible
# to an actual client. Set to False when done testing.
DEBUG = True

# ----------------------------------------------------------------------
# SQL Utility Functions
# ----------------------------------------------------------------------
def get_conn():
    """"
    Returns a connected MySQL connector instance, if connection is successful.
    If unsuccessful, exits.
    """
    try:
        conn = mysql.connector.connect(
          host='localhost',
          user='appadmin',
          # Find port in MAMP or MySQL Workbench GUI or with
          # SHOW VARIABLES WHERE variable_name LIKE 'port';
          port='3306',
          password='adminpw',
          database='booksdb'
        )
        print('Successfully connected.')
        return conn
    except mysql.connector.Error as err:
        # Remember that this is specific to _database_ users, not
        # application users. So is probably irrelevant to a client in your
        # simulated program. Their user information would be in a users table
        # specific to your database.
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR and DEBUG:
            sys.stderr('Incorrect username or password when connecting to DB.')
        elif err.errno == errorcode.ER_BAD_DB_ERROR and DEBUG:
            sys.stderr('Database does not exist.')
        elif DEBUG:
            sys.stderr(err)
        else:
            sys.stderr('An error occurred, please contact the administrator.')
        sys.exit(1)

# ----------------------------------------------------------------------
# Functions for Command-Line Options/Query Execution
# ----------------------------------------------------------------------
def search_for_books():
    '''
    A function to prompt users for genre, language, and year specifications in 
    searching the database for books. Then, using these specifications, the
    books will be displayed in order of descending publication year.
    '''
    # Ask the user whether they'd like to search the database using these
    # criteria 
    ans = input('Would you want to search books by genre, language, and year?')
    chosen_genre = None
    chosen_lang = None
    chosen_yr = None

    # If yes, prompt the user for each of the search criteria
    if ans and ans.lower()[0] == 'y':
        chosen_genre = input('What genre are you looking for?')
        chosen_lang = input("""What language are you looking for? 
            (Options: eng, ara, )""")
        chosen_yr = input('After which year should the books be published?')

    # If the user has entered search criteria, create the SQL query
    if chosen_genre and chosen_lang and chosen_yr:
        sql = """
            SELECT orig_title, orig_publication_yr
            FROM books NATURAL JOIN genres
            WHERE genre = '%s' AND language_code = '%s'
            AND orig_publication_yr > %s
            ORDER BY orig_publication_yr DESC;""" % (chosen_genre, chosen_lang, 
                chosen_yr)
    
    # Attempt to retrieve the books
    try:
        cursor = conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
    except mysql.connector.Error as err:
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            sys.stderr('An error occurred, could not retrieve specified books.')
    
    # If there are no books, let the user know. Otherwise, display
    # the results.
    if not rows:
        print("""Could not find any books under genre %s, in %s, published after
            %d""".format(chosen_genre, chosen_lang, chosen_yr))
    else:
        print("""The following are books under genre %s, in %s, published after
            %d""".format(chosen_genre, chosen_lang, chosen_yr))
        for row in rows:
            (orig_title, orig_publication_yr) = (row) 
            print('    ', f'{orig_title}', f'{orig_publication_yr}')


def add_rating():
    """
    Users are also able to perform other actions, such as add a rating of a 
    book to the database.
    """
    # Ask the user whether they'd like to rate a book
    ans = input('Would you like to rate a book?')
    user_id = None
    isbn_10 = None
    rating = None

    # If yes, prompt the user for rating info
    if ans and ans.lower()[0] == 'y':
        user_id = input('What is your user_id?')
        isbn_10 = input('What is the isbn_10 identifier of the book?')
        rating = input('What do you rate this book (1 to 5 stars?')

    # If the user has entered valid rating info, create the SQL command
    if user_id and isbn_10 and rating:
        sql = """
            INSERT INTO ratings(user_id, isbn_10, rating) 
            VALUES (%s, %s, %s);""" % (user_id, isbn_10, rating)
    
    # Attempt to add this book to the ratings table
    try:
        cursor = conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
    except mysql.connector.Error as err:
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            sys.stderr('An error occurred, could not add rating to database.')



def add_to_read_item():
    """
    User can also add a book to their "to-read" shelf by adding an 
    entry to the to-read table.
    """
    # Ask the user whether they'd like to add a book to their to-read shelf
    ans = input('Would you like to add a book to your to-read shelf?')
    user_id = None
    isbn_10 = None

    # If yes, prompt the user for rating info
    if ans and ans.lower()[0] == 'y':
        user_id = input('What is your user_id?')
        isbn_10 = input('What is the isbn_10 identifier of the book?')

    # If the user has entered valid to-read book info, create the SQL command
    if user_id and isbn_10:
        sql = """
            INSERT INTO to_read(user_id, isbn_10) 
            VALUES (%s, %s);""" % (user_id, isbn_10)
    
    # Attempt to add this book to the to_read table
    try:
        cursor = conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
    except mysql.connector.Error as err:
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            sys.stderr("""An error occurred, could not add book to to_read 
                table.""")


def view_popular_series_info():
    """
    Users can also view information pertaining to popular series in the 
    database, such as the Harry Potter series, the Twilight Series, and more. 
    """
    # Ask the user whether they'd like to see popular series information
    ans = input('Would you like to see information on popular series?')
    chosen_series = None
    option = None

    # If yes, prompt the user for which popular series they'd like
    # information on 
    if ans and ans.lower()[0] == 'y':
        print('Which series would you like information on?')
        print('  (h) - Harry Potter')
        print('  (t) - twilight')
        print('  (t) - add a book to your to-read shelf')
        print('  (p) - view information on popular series')
        print('  (b) - get a book recommendation')
        print('  (q) - quit')
        print()

        option = input('Enter an option: ').lower()
        
        if option == ''
        chosen_series = 
        
    # If the user has entered search criteria, create the SQL query
    if chosen_genre and chosen_lang and chosen_yr:
        sql = """
            SELECT orig_title, orig_publication_yr
            FROM books NATURAL JOIN genres
            WHERE genre = '%s' AND language_code = '%s'
            AND orig_publication_yr > %s
            ORDER BY orig_publication_yr DESC;""" % (chosen_genre, chosen_lang, 
                chosen_yr)
    
    # Attempt to retrieve the books
    try:
        cursor = conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
    except mysql.connector.Error as err:
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            sys.stderr('An error occurred, could not retrieve specified books.')
    
    # If there are no books, let the user know. Otherwise, display
    # the results.
    if not rows:
        print("""Could not find any books under genre %s, in %s, published after
            %d""".format(chosen_genre, chosen_lang, chosen_yr))
    else:
        print("""The following are books under genre %s, in %s, published after
            %d""".format(chosen_genre, chosen_lang, chosen_yr))
        for row in rows:
            (orig_title, orig_publication_yr) = (row) 
            print('    ', f'{orig_title}', f'{orig_publication_yr}')
    

def get_book_recommendation():
    """
    Users can also be recommended a book by entering a book they liked. Then,
    a similar book will be recommended by extracting information about the book 
    they liked, given that it is in the database.
    """
    pass

def get_users_top_rated():
    """
    Meanwhile, admin users can target specific readers and recommend them books
    by accessing their top-rated or to-read books.
    """
    pass


def get_top_rated_in_timeframe():
    """
    Admin users may also view top-rated books within a specific timeframe to 
    analyze the market for books.
    """
    pass


# ----------------------------------------------------------------------
# Functions for Logging Users In
# ----------------------------------------------------------------------
def sign_up():
    """
    If a user doesn't have an account yet, allow them to create an account.
    """
    username = input('Please enter your new username (<= 20 characters):')
    password = input('Please enter your new password (<= 20 characters):')

    # If the user has entered a username and password, add them 
    if username and password:
        sql = """
            CALL sp_add_user(%s, %s);
            """ % (username, password)
    
    # Attempt to execute the SQL procedure
    try:
        cursor = conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
    except mysql.connector.Error as err:
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            sys.stderr('An error occurred, could not add user to database.')


def authenticate_login():
    """
    Ask for a user's login information, and verify whether their login
    information is valid.
    """
    has_acct = input('Do you already have an account?')
    username = None
    password = None

    # If they don't have an account, prompt them to sign up first. Otherwise,
    # check if their login information is valid.
    # If yes, prompt the user for each of the search criteria
    if has_acct and has_acct.lower()[0] == 'y':
        username = input('Please enter your username:')
        password = input('Please enter your password:')

    # If the user has entered login info, create the SQL command
    if username and password:
        sql = """
            authenticate(%s, %s)""" % (username, password)
    
    # Attempt to authenticate this user
    try:
        cursor = conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
    except mysql.connector.Error as err:
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            sys.stderr('An error occurred, could not login.')

# ----------------------------------------------------------------------
# Command-Line Functionality
# ----------------------------------------------------------------------
def show_options():
    """
    Displays options users can choose in the application, such as
    viewing <x>, filtering results with a flag (e.g. -s to sort),
    sending a request to do <x>, etc.
    """
    print('What would you like to do? ')
    print('  (s) - search for books by genre, language, and year')
    print('  (r) - add a rating for a book')
    print('  (t) - add a book to your to-read shelf')
    print('  (p) - view information on popular series')
    print('  (b) - get a book recommendation')
    print('  (q) - quit')
    print()

    ans = input('Enter an option: ').lower()
    if ans == 'q':
        quit_ui()
    elif ans == 's':
        search_for_books()
    elif ans == 'r':
        add_rating()
    elif ans == 't':
        add_to_read_item()
    elif ans  == 'p':
        view_popular_series_info()
    elif ans == 'b':
        get_book_recommendation()


# You may choose to support admin vs. client features in the same program, or
# separate the two as different client and admin Python programs using the same
# database.
def show_admin_options():
    """
    Displays options specific for admins, such as adding new data <x>,
    modifying <x> based on a given id, removing <x>, etc.
    """
    print('What would you like to do? ')
    print('  (x) - something nifty for admins to do')
    print('  (x) - another nifty thing')
    print('  (x) - yet another nifty thing')
    print('  (x) - more nifty things!')
    print('  (q) - quit')
    print()
    ans = input('Enter an option: ').lower()
    if ans == 'q':
        quit_ui()
    elif ans == '':
        pass


def quit_ui():
    """
    Quits the program, printing a good bye message to the user.
    """
    print('Good bye!')
    exit()


def main():
    """
    Main function for starting things up.
    """
    show_options()


if __name__ == '__main__':
    # This conn is a global object that other functinos can access.
    # You'll need to use cursor = conn.cursor() each time you are
    # about to execute a query with cursor.execute(<sqlquery>)
    conn = get_conn()
    main()
