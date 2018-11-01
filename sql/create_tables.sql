-- Thu Nov  1 22:44:41 2018
-- Name: tables.sql
-- Author: Patryk Niedźwiedziński
-- Version: 02.00.0000

SET @dbname = IF(@dbname, @dbname, 'pytatki');

-- -----------------------------------------------------
-- Use database
-- -----------------------------------------------------
PREPARE stmt FROM CONCAT('USE ', @dbname);
EXECUTE stmt;
DEALLOCATE PREPARE stmt;


-- -----------------------------------------------------
-- Table status
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS status (
  idstatus INT NOT NULL AUTO_INCREMENT,
  name VARCHAR(45) NOT NULL,
  description LONGTEXT NULL,
  PRIMARY KEY (idstatus));


-- -----------------------------------------------------
-- Table user
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS user (
  iduser INT NOT NULL AUTO_INCREMENT,
  login VARCHAR(45) NOT NULL,
  password VARCHAR(200) NOT NULL,
  email VARCHAR(45) NOT NULL,
  email_confirm BINARY(1) NOT NULL DEFAULT 0,
  status_id INT NOT NULL,
  PRIMARY KEY (iduser),
  INDEX fk_user_status_idx (status_id ASC),
  UNIQUE INDEX login_UNIQUE (login ASC),
  UNIQUE INDEX email_UNIQUE (email ASC),
  CONSTRAINT fk_user_status
    FOREIGN KEY (status_id)
    REFERENCES status (idstatus)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);


-- -----------------------------------------------------
-- Table usergroup
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS usergroup (
  idusergroup INT NOT NULL AUTO_INCREMENT,
  name VARCHAR(45) NOT NULL,
  color VARCHAR(7) NOT NULL DEFAULT '#ffffff',
  description LONGTEXT NULL,
  image_path VARCHAR(200) NOT NULL DEFAULT 'img/default.jpg',
  parent_id INT NOT NULL DEFAULT 0,
  PRIMARY KEY (idusergroup),
  UNIQUE INDEX name_UNIQUE (name ASC));


-- -----------------------------------------------------
-- Table user_membership
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS user_membership (
  iduser_membership INT NOT NULL AUTO_INCREMENT,
  usergroup_id INT NOT NULL,
  user_id INT NOT NULL,
  PRIMARY KEY (iduser_membership),
  INDEX fk_user_membership_usergroup1_idx (usergroup_id ASC),
  INDEX fk_user_membership_user1_idx (user_id ASC),
  CONSTRAINT fk_user_membership_usergroup1
    FOREIGN KEY (usergroup_id)
    REFERENCES usergroup (idusergroup)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT fk_user_membership_user1
    FOREIGN KEY (user_id)
    REFERENCES user (iduser)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);
