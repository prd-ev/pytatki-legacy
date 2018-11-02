-- Fri Nov  2 12:59:47 2018
-- Name: predifined.sql
-- Author: Patryk Niedźwiedziński
-- Version: 02.00.0000

-- -----------------------------------------------------
-- status
-- -----------------------------------------------------

-- active
INSERT INTO status VALUES (1, "active", "Is active");

-- removed
INSERT INTO status VALUES (2, "removed", "Scheduled to remove");

-- -----------------------------------------------------
-- note_type
-- -----------------------------------------------------

-- file
INSERT INTO note_type VALUES (1, "file", "File note type");
