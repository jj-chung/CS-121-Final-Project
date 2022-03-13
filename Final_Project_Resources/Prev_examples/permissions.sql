-- To see all of the users in your mysql settings:
SELECT user FROM mysql.user;

-- To create users with passwords (locally) (can also set up this up on phpMyAdmin or Workbench)
CREATE USER 'airbnbadmin'@'localhost' IDENTIFIED BY 'adminpw';
CREATE USER 'airbnbclient'@'localhost' IDENTIFIED BY 'clientpw';
SELECT user, execute_priv FROM mysql.user;

GRANT ALL PRIVILEGES ON *.* TO 'airbnbadmin'@'localhost';
GRANT SELECT ON airbnbdb.* TO 'airbnbclient'@'localhost';
 
FLUSH PRIVILEGES;
SELECT user, execute_priv FROM mysql.user WHERE user LIKE 'airbnb%';
-- Now, only airbnbadmin has admin privileges, airbnbclient only has SELECT privileges (no procedures)

-- Permissions in action (after logging in with mysql -u airbnbclient -p)
USE airbnbdb;
-- Client doesn't have execute permissions, thus this will cause an error
CALL superhosts();
-- ERROR 1370 (42000): execute command denied to user 'airbnbclient'@'localhost' for routine 'airbnbdb.superhosts'
