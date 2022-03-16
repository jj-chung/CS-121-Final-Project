-- File for Password Management section of Final Project

-- (Provided) This function generates a specified number of characters for using 
-- as a salt in passwords.

DROP FUNCTION IF EXISTS make_salt;

DELIMITER !
CREATE FUNCTION make_salt(num_chars INT) 
RETURNS VARCHAR(20) DETERMINISTIC
BEGIN
    DECLARE salt VARCHAR(20) DEFAULT '';

    -- Don't want to generate more than 20 characters of salt.
    SET num_chars = LEAST(20, num_chars);

    -- Generate the salt!  Characters used are ASCII code 32 (space)
    -- through 126 ('z').
    WHILE num_chars > 0 DO
        SET salt = CONCAT(salt, CHAR(32 + FLOOR(RAND() * 95)));
        SET num_chars = num_chars - 1;
    END WHILE;

    RETURN salt;
END !
DELIMITER ;

-- Drop statement for table
DROP TABLE IF EXISTS user_info;

-- Provided 
-- This table holds information for authenticating users based on
-- a password.  Passwords are not stored plaintext so that they
-- cannot be used by people that shouldn't have them.
-- You may extend that table to include an is_admin or role attribute if you 
-- have admin or other roles for users in your application 
-- (e.g. store managers, data managers, etc.)
CREATE TABLE user_info (
    -- Usernames are up to 20 characters.
    username VARCHAR(20) PRIMARY KEY,

    -- Salt will be 8 characters all the time, so we can make this 8.
    salt CHAR(8) NOT NULL,

    -- We use SHA-2 with 256-bit hashes.  MySQL returns the hash
    -- value as a hexadecimal string, which means that each byte is
    -- represented as 2 characters.  Thus, 256 / 8 * 2 = 64.
    -- We can use BINARY or CHAR here; BINARY simply has a different
    -- definition for comparison/sorting than CHAR.
    password_hash BINARY(64) NOT NULL,

    -- Different roles for different users within the application.
    user_role VARCHAR(20) NOT NULL DEFAULT 'reader',
    CHECK user_role IN ('reader', 'retailer')
);

-- [Problem 1a]
-- Adds a new user to the user_info table, using the specified password (max
-- of 20 characters). Salts the password with a newly-generated salt value,
-- and then the salt and hash values are both stored in the table.

DROP PROCEDURE IF EXISTS sp_add_user;

DELIMITER !
CREATE PROCEDURE sp_add_user(
    new_username VARCHAR(20), 
    password VARCHAR(20),
    user_role VARCHAR(20)
)
BEGIN
    -- The salt we will add to the password before hashing
    DECLARE pw_salt CHAR(8);
    SELECT make_salt(8) INTO pw_salt;

    -- Insert the new user info user_info, using SHA2 with 256-bit hashes for
    -- the user's password
    INSERT INTO user_info(username, salt, password_hash)
        VALUES (new_username, pw_salt, SHA2(CONCAT(pw_salt, password), 256), 
            user_role);
END !
DELIMITER ;

-- [Problem 1b]
-- Authenticates the specified username and password against the data
-- in the user_info table.  Returns 1 if the user appears in the table, and the
-- specified password hashes to the value for the user. Otherwise returns 0.

DROP FUNCTION IF EXISTS authenticate;

DELIMITER !
CREATE FUNCTION authenticate(username VARCHAR(20), password VARCHAR(20))
RETURNS TINYINT DETERMINISTIC
BEGIN
    -- The salt added to the password before hashing, from the user_info table
    DECLARE pw_salt CHAR(8);
    -- The password hash from the user_info table
    DECLARE pw_hash BINARY(64);

    -- If the username is not in the table, the user does not appear in the 
    -- table
    IF username NOT IN (SELECT username FROM user_info)
        THEN RETURN 0;
    END IF;

    -- Retrieve this user's salt and password hash from the database
    SELECT user_info.salt, user_info.password_hash INTO pw_salt, pw_hash
        FROM user_info
        WHERE user_info.username = username;

    -- If the hashed password matches the hashed password in user_info, 
    -- the user and password are valid
    IF SHA2(CONCAT(pw_salt, password), 256) = pw_hash
        THEN RETURN 1;
        ELSE RETURN 0;
    END IF;
END !
DELIMITER ;

-- [Problem 1c]
-- Add at least two users into your user_info table so that when we run this 
-- file, we will have examples users in the database.
CALL sp_add_user('avidreader', 'WRAYp7e', 'reader');
CALL sp_add_user('bookworm', '5d3SqJX', 'reader');
CALL sp_add_user('bookseller', 'sellbooks900', 'retailer')

-- [Problem 1d]
-- Optional: Create a procedure sp_change_password to generate a new salt and 
-- change the given user's password to the given password (after salting and 
-- hashing)

DROP PROCEDURE IF EXISTS sp_change_password;

DELIMITER !
CREATE PROCEDURE sp_change_password(existing_username VARCHAR(20), 
    password VARCHAR(20))
BEGIN
    -- The salt we will add to the password before hashing
    DECLARE pw_salt CHAR(8);
    SELECT make_salt(8) INTO pw_salt;

    UPDATE user_info
        SET salt = pw_salt, 
            password_hash = SHA2(CONCAT(pw_salt, password), 256)
        WHERE username = existing_username;
END !
DELIMITER ;
