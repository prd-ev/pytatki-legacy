-- Thu Nov  1 22:44:41 2018
-- Name: create_database.sql
-- Author: Patryk Niedźwiedziński
-- Version: 02.00.0000

SET @dbname = IF(@dbname, @dbname, 'pytatki');

-- -----------------------------------------------------
-- Create database
-- -----------------------------------------------------
PREPARE stmt FROM CONCAT('CREATE DATABASE ', @dbname);
EXECUTE stmt;
DEALLOCATE PREPARE stmt;
