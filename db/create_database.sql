-- Thu Nov  1 22:44:41 2018
-- Name: create_database.sql
-- Author: Patryk Niedźwiedziński
-- Version: 02.00.0000

SET @dbname = IF(@dbname, @dbname, 'pytatki');

-- -----------------------------------------------------
-- Create database
-- -----------------------------------------------------
SET @sql = CONCAT('CREATE DATABASE ', @dbname);
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;
