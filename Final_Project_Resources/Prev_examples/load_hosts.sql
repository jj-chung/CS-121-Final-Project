-- Loading data locally (within the directory you started mysql in)
-- SHOW GLOBAL VARIABLES LIKE 'local_infile';
-- SET GLOBAL local_infile = 'ON'
-- or, start the console with
-- mysql --local-infile=1 -u root -p
-- Make sure you have a hosts table created to run this!
LOAD DATA LOCAL INFILE 'seattle_hosts.csv' INTO TABLE hosts
FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 ROWS;

-- For windows:
-- LOAD DATA LOCAL INFILE 'artists.csv' INTO TABLE artist
-- FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\r\n' IGNORE 1 ROWS;

