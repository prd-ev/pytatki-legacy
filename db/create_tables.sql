-- Thu Nov  1 22:44:41 2018
-- Name: create_tables.sql
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
  status_id INT NOT NULL DEFAULT 1,
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
  usergroup_id INT NOT NULL,
  user_id INT NOT NULL,
  PRIMARY KEY (usergroup_id, user_id),
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


-- -----------------------------------------------------
-- Table note_type
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS note_type (
  idnote_type INT NOT NULL AUTO_INCREMENT,
  name VARCHAR(45) NULL,
  description LONGTEXT NULL,
  PRIMARY KEY (idnote_type));


-- -----------------------------------------------------
-- Table notegroup
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS notegroup (
  idnotegroup INT NOT NULL AUTO_INCREMENT,
  name VARCHAR(45) NOT NULL,
  parent_id INT NOT NULL,
  PRIMARY KEY (idnotegroup));


-- -----------------------------------------------------
-- Table note
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS note (
  idnote INT NOT NULL AUTO_INCREMENT,
  value LONGTEXT NOT NULL,
  title VARCHAR(45) NOT NULL DEFAULT 'New note',
  note_type_id INT NOT NULL,
  user_id INT NOT NULL,
  notegroup_id INT NOT NULL,
  status_id INT NOT NULL,
  PRIMARY KEY (idnote),
  INDEX fk_note_note_type1_idx (note_type_id ASC),
  INDEX fk_note_user1_idx (user_id ASC),
  INDEX fk_note_notegroup1_idx (notegroup_id ASC),
  INDEX fk_note_status1_idx (status_id ASC),
  CONSTRAINT fk_note_note_type1
    FOREIGN KEY (note_type_id)
    REFERENCES note_type (idnote_type)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT fk_note_user1
    FOREIGN KEY (user_id)
    REFERENCES user (iduser)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT fk_note_notegroup1
    FOREIGN KEY (notegroup_id)
    REFERENCES notegroup (idnotegroup)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT fk_note_status1
    FOREIGN KEY (status_id)
    REFERENCES status (idstatus)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);


-- -----------------------------------------------------
-- Table tag
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS tag (
  idtag INT NOT NULL AUTO_INCREMENT,
  name VARCHAR(45) NOT NULL,
  PRIMARY KEY (idtag),
  UNIQUE INDEX name_UNIQUE (name ASC));


-- -----------------------------------------------------
-- Table tagging
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS tagging (
  idtagging INT NOT NULL AUTO_INCREMENT,
  note_id INT NOT NULL,
  tag_id INT NOT NULL,
  PRIMARY KEY (idtagging),
  INDEX fk_tagging_note1_idx (note_id ASC),
  INDEX fk_tagging_tag1_idx (tag_id ASC),
  CONSTRAINT fk_tagging_note1
    FOREIGN KEY (note_id)
    REFERENCES note (idnote)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT fk_tagging_tag1
    FOREIGN KEY (tag_id)
    REFERENCES tag (idtag)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);


-- -----------------------------------------------------
-- Table action
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS action (
  idaction INT NOT NULL AUTO_INCREMENT,
  content LONGTEXT NULL,
  user_id INT NOT NULL,
  note_id INT NOT NULL,
  date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (idaction),
  INDEX fk_action_user1_idx (user_id ASC),
  INDEX fk_action_note1_idx (note_id ASC),
  CONSTRAINT fk_action_user1
    FOREIGN KEY (user_id)
    REFERENCES user (iduser)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);


-- -----------------------------------------------------
-- Table usergroup_has_notegroup
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS usergroup_has_notegroup (
  usergroup_id INT NOT NULL,
  notegroup_id INT NOT NULL,
  PRIMARY KEY (usergroup_id, notegroup_id),
  INDEX fk_usergroup_has_notegroup_notegroup1_idx (notegroup_id ASC),
  INDEX fk_usergroup_has_notegroup_usergroup1_idx (usergroup_id ASC),
  CONSTRAINT fk_usergroup_has_notegroup_usergroup1
    FOREIGN KEY (usergroup_id)
    REFERENCES usergroup (idusergroup)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT fk_usergroup_has_notegroup_notegroup1
    FOREIGN KEY (notegroup_id)
    REFERENCES notegroup (idnotegroup)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);


-- -----------------------------------------------------
-- Table ver
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS scheme_change (
  idscheme_change INT NOT NULL AUTO_INCREMENT,
  ver INT NOT NULL,
  script VARCHAR(45) NOT NULL,
  date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (idscheme_change)