-- CS 121 Winter 2022 Final Project
-- Part F: MySQL Users and Permissions

CREATE USER 'bookretailer'@'localhost' IDENTIFIED BY '8sXjJK';
CREATE USER 'bookreader'@'localhost' IDENTIFIED BY '4qY4us';
-- Can add more users or refine permissions
GRANT ALL PRIVILEGES ON booksdb.* TO 'bookretailer'@'localhost';
GRANT SELECT ON booksdb.* TO 'bookreader'@'localhost';
FLUSH PRIVILEGES;
