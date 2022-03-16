"""
Brief overview of application:
Our application allows user to navigate the books database. Users are able
to search books using specific search criteria, including genre, publication 
year, author, ratings, and more. 

Users are also able to perform other actions, such as:
- add a rating of a book to the database
- add a book to their "to-read" shelf by adding an entry to the to-read table
- view information pertaining to books by authors of popular series 
in the database, such as the Harry Potter series, the Twilight Series, and more
- can be recommended a book by entering a book they liked. Then,
a similar book will be recommended by extracting information about the book they
liked, given that it is in the database.

Meanwhile, admin users can target specific readers and recommend them books
by accessing their top-rated or to-read books. They may also view top-rated
books within a specific timeframe to analyze the market for books. 

Names: Amelia Whitworth, Jennie Chung
Emails: awhirwor@caltech.edu, jjchung@caltech.edu 
"""

from re import S
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
          user='bookretailer',
          # Find port in MAMP or MySQL Workbench GUI or with
          # SHOW VARIABLES WHERE variable_name LIKE 'port';
          port='3306',
          password='8sXjJK',
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
def execute_sql_query(sql, error_message):
    """
    Try-except for executing sql queries.
    """
    try:
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
        rows = cursor.fetchall()
    except mysql.connector.Error as err:
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            sys.stderr(error_message)

    return rows

def execute_sql_command(sql, error_message):
    """
    Try-except for executing sql commands where query result is not needed.
    """
    try:
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
    except mysql.connector.Error as err:
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            sys.stderr(error_message)


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
    rows = execute_sql_query(sql, """An error occurred, could not retrieve 
        specified books.""")
    
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
            print('    ', orig_title, orig_publication_yr)


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
    execute_sql_command('An error occurred, could not add rating to database.')


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
    execute_sql_command('An error occurred, could not add book to to_read.')


def view_popular_series_info():
    """
    Users can also view information pertaining to popular authors in the 
    database, such as the authors of Harry Potter series, the Twilight Series, 
    and more. 
    """
    # Ask the user whether they'd like to see popular series information
    ans = input("""Would you like to see information on books by 
        authors of popular series?""")
    chosen_author = None
    option = None

    # If yes, prompt the user for which popular series they'd like
    # information on 
    if ans and ans.lower()[0] == 'y':
        print('Which series author would you like book information for?')
        print('  (h) - Harry Potter')
        print('  (t) - Twilight')
        print('  (g) - The Hunger Games')
        print('  (n) - The Chronicles of Narnia')
        print('  (got) - Games of Thrones')
        print()

        option = input('Enter an option: ').lower()
        
        if option == 'h':
            chosen_author = 'J.K. Rowling'
        elif option == 't':
            chosen_author = 'Stephanie Meyer'
        elif option == 'g':
            chosen_author = 'Suzanne Collins'
        elif option == 'n':
            chosen_author = 'C.S. Lewis'
        elif option == 'got':
            chosen_author = 'George R.R. Martin'
        
    # If the user has entered search criteria, create the SQL query
    if chosen_author:
        sql = """
            SELECT orig_title, orig_publication_yr, author, num_pages, 
                num_comments, num_editions  
            FROM books NATURAL JOIN book_details NATURAL JOIN authors 
            WHERE author LIKE '%%%s%%';""" % (chosen_author)
    
    # Attempt to retrieve the books by this popular series author
    rows = execute_sql_query(sql, """An error occurred, could not retrieve 
        popular series.""")
    
    # If there are no books, let the user know. Otherwise, display
    # the results.
    if not rows:
        print("Could not find any books by %s".format(chosen_author))
    else:
        print("The following are books are by %s:".format(chosen_author))
        for row in rows:
            (orig_title, orig_publication_yr, author, num_pages, num_comments,
                num_editions) = (row) 
            print('    ', orig_title, orig_publication_yr, 
                author, num_pages, num_comments, num_editions)
    

def get_isbn_10(select_option):
    """
    Helper function for get_book_recommendation for users to either select a 
    book from a list of books or directly input an isbn. 
    """
    # If the user wants to select from a list of options, let them select one,
    # otherwise they can input the isbn_10 directly.
    if select_option == 'options':
        print('Which of these books appeals to you most?')
        print('  (h) - The Hobbit and The Lord of the Rings')
        print('  (hp) - Harry Potter and the Philosopher\'s Stone')
        print('  (m) - A Midsummer Night\'s Dream')
        print('  (g) - The Giver')
        print('  (t) - A Tale of Two Cities')
        print()

        option = input('Enter an option: ').lower()

        # We hardcode these isbn_10 identifiers in case there are duplicate
        # titles or duplicate titles are added to the db later on
        if option == 'h':
            isbn_10 = ' 345538374'
        elif option == 'hp':
            isbn_10 = ' 439554934'
        elif option == 'm':
            isbn_10 = ' 743477545'
        elif option == 'g':
            isbn_10 = ' 385732554'
        elif option == 't':
            isbn_10 = ' 141439602'
    elif select_option == 'direct_selection':
        isbn_10 = input('What is the isbn_10 of a book you\'ve enjoyed?')

    return isbn_10


def get_book_recommendation():
    """
    Users can also be recommended a book by entering a book they liked. Then,
    a similar book will be recommended by extracting information about the book 
    they liked, given that it is in the database.
    """
    # Ask the user whether they'd like to search the database using these
    # criteria 
    ans = input('Would you like to get a book recommendation?')
    isbn_10 = None

    by_genre = None
    by_year = None
    by_author = None

    # If yes, prompt the user for a book they like in the database?
    if ans and ans.lower()[0] == 'y':
        print('To recommend a book, you can either:')
        print('  (l) - See a list of books in the database and select one')
        print('  (b) - Select a book you\'ve enjoyed in the database')
        print()

        select_option = input('Enter an option: ').lower()

        if select_option == 'l':
            isbn_10 = get_isbn_10('options')
        elif select_option == 'b':
            isbn_10 = get_isbn_10('direct_selection')

        # If the user has entered search criteria, create the SQL query
        if isbn_10:
            sql = """
                SELECT isbn_10, orig_title, genre, publication_year, author
                FROM books NATURAL JOIN genres NATURAL JOIN authors
                WHERE isbn_10 = %s""" % (isbn_10)
        
        # Attempt to retrieve the books
        rows = execute_sql_query(sql, """An error occurred, could not retrieve
            book to base recommendation on.""")
        
        # If there are no books, let the user know. Otherwise, make some
        # recommendations with the same genre, publication year, and/or 
        # author
        if not rows:
            print("""A book with isbn_10 %s does not exist in the 
                database""".format(isbn_10))
        else:
            for row in rows:
                (isbn_10, orig_title, genre, year, author) = (row) 
                recommendations = []
                
                # Find a book in the same genre
                sql = """
                SELECT isbn_10, orig_title
                FROM books NATURAL JOIN genres
                WHERE genre = '%s'
                """% (genre)
                same_genre_row = execute_sql_query(sql, """An error occured, 
                    could not retrieve same genre book""")
                if same_genre_row:
                    recommendations.append(same_genre_row)

                sql = """
                SELECT isbn_10, orig_title
                FROM books
                WHERE orig_publication_yr = '%s'
                """% (year)
                # Find a book in the same publication year
                same_year_row = execute_sql_query(sql, """An error occured, 
                    could not retrieve same publication year book""")
                if same_year_row:
                    recommendations.append(same_year_row)

                sql = """
                SELECT isbn_10, orig_title
                FROM books NATURAL JOIN authors
                WHERE author = '%s'
                """% (author)
                # Find a book with the same author
                same_year_row = execute_sql_query(sql, """An error occured, 
                    could not retrieve same author book""")
                if same_year_row:
                    recommendations.append(same_year_row)

                if recommendations:
                    print('Here are some recommendations based on your selection:')
                    for row in recommendations:
                        (orig_title, orig_publication_yr) = (row) 
                        print('    ', isbn_10, orig_title)
                else:
                    print("""There are no books with the same genre, 
                        publication year, or author as the selection.""")


def get_users_top_rated():
    """
    Admin users can target specific readers and recommend them books
    by accessing their top-rated or to-read books.
    """
    # Ask the user whether they'd like to get a user's top rated books
    ans = input('Would you like to get a user\'s top rated books?')
    chosen_user_id = None

    # If yes, prompt the user for user_id
    if ans and ans.lower()[0] == 'y':
        chosen_user_id = input('Which user are you interested in?')

    # If the user has entered a user_id create the SQL query
    if chosen_user_id:
        sql = """
            SELECT isbn_10, rating
            FROM ratings
            WHERE user_id = %s
            ORDER BY rating DESC
            LIMIT 10;""" % (chosen_user_id)
    
    # Attempt to retrieve the user's top rated books
    rows = execute_sql_query(sql, """An error occurred, could not retrieve 
        user's top rated books.""")
    
    # If there are no books, let the user know. Otherwise, display
    # the results.
    if not rows:
        print("Could not find user %s's top rated books".format(chosen_user_id))
    else:
        print("User %s's top rated books:".format(chosen_user_id))
        for row in rows:
            (isbn_10, rating) = (row) 
            print('    ', isbn_10, rating)


def get_top_rated_in_timeframe():
    """
    Admin users may also view top-rated books within a specific timeframe to 
    analyze the market for books.
    """
     # Ask the user whether they'd like to get a user's top rated books
    ans = input('Would you like to get top rated books within a timeframe?')
    start_year = None
    end_year = None

    # If yes, prompt the user for start and end years
    if ans and ans.lower()[0] == 'y':
        start_year = input('What is the starting year (inclusive)?')
        end_year = input('What is the ending year (inclusive)?')

    # If the user has entered start and end years, create the SQL query
    if start_year and end_year:
        sql = """
            SELECT isbn_10, AVG(rating) AS avg_rating
            FROM ratings NATURAL JOIN books
            WHERE publication_year > %s AND publication_year < %s
            GROUP BY isbn_10
            ORDER BY avg_rating DESC;""" % (start_year, end_year)
    
    # Attempt to retrieve the user's top rated books
    rows = execute_sql_query(sql, """An error occurred, could not retrieve 
        top rated books in specified timeframe.""")
    
    # If there are no books, let the user know. Otherwise, display
    # the results.
    if not rows:
        print("""Could not find top rated books between %s 
            and %s""".format(start_year, end_year))
    else:
        print("Top rated books %s to %s:".format(start_year, end_year))
        for row in rows:
            (isbn_10, avg_rating) = (row) 
            print('    ', isbn_10, avg_rating)


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
    execute_sql_command(sql, """An error occurred, could not add user to 
        database.""")


def authenticate_login():
    """
    Ask for a user's login information, and verify whether their login
    information is valid.
    """
    print('Do you already have an account?')
    has_acct = input('Enter y/n:')
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
        sql = "SELECT authenticate('%s', '%s');" % (username, password)
    
    # Attempt to authenticate this user
    authenticated = execute_sql_command(sql, """An error occurred, could not 
        login.""")

    row = authenticated[0]
    is_authenticated = row[0]

    if is_authenticated == 1:
        print('Login successful!')
        
        # Get role of user 
        sql = """
            SELECT user_role
            FROM user_info
            WHERE username = '%s'""" % (username)

        rows = execute_sql_query(sql, 
            "An error occured, could not get user role.")

        for row in rows:
            return row
    else:
        print('Login failed. Please try again.')


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
    print('  (p) - view information on books by popular series authors')
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
    print('  (utr) - get a user\'s top rated')
    print('  (trt) - get top rated books in a specific timeframe')
    print('  (q) - quit')
    print()
    ans = input('Enter an option: ').lower()
    if ans == 'q':
        quit_ui()
    elif ans == 'utr':
        get_users_top_rated()
    elif ans == 'trt':
        get_top_rated_in_timeframe()


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
    # Allow users to login
    role = authenticate_login()

    # Depending on whether the user is admin or not, show options
    if role == 'reader':
        show_options()
    if role == 'retailer':
        show_admin_options()

if __name__ == '__main__':
    # This conn is a global object that other functinos can access.
    # You'll need to use cursor = conn.cursor() each time you are
    # about to execute a query with cursor.execute(<sqlquery>)
    conn = get_conn()
    main()
