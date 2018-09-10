-- MySQL Script generated by MySQL Workbench
-- Mon Sep 10 18:49:32 2018
-- Model: New Model    Version: 1.0
-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `mydb` DEFAULT CHARACTER SET utf8 ;
USE `mydb` ;

-- -----------------------------------------------------
-- Table `mydb`.`status`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`status` (
  `idstatus` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  `description` LONGTEXT NULL,
  PRIMARY KEY (`idstatus`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`user`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`user` (
  `iduser` INT NOT NULL AUTO_INCREMENT,
  `login` VARCHAR(45) NOT NULL,
  `password` VARCHAR(200) NOT NULL,
  `email` VARCHAR(45) NOT NULL,
  `email_confirm` BINARY(1) NOT NULL DEFAULT 0,
  `status_id` INT NOT NULL,
  PRIMARY KEY (`iduser`),
  INDEX `fk_user_status_idx` (`status_id` ASC),
  CONSTRAINT `fk_user_status`
    FOREIGN KEY (`status_id`)
    REFERENCES `mydb`.`status` (`idstatus`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`usergroup`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`usergroup` (
  `idusergroup` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  `color` VARCHAR(7) NOT NULL DEFAULT '#ffffff',
  `description` LONGTEXT NULL,
  `image_path` VARCHAR(200) NOT NULL DEFAULT 'img/default.jpg',
  PRIMARY KEY (`idusergroup`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`user_membership`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`user_membership` (
  `iduser_membership` INT NOT NULL AUTO_INCREMENT,
  `usergroup_id` INT NOT NULL,
  `user_id` INT NOT NULL,
  PRIMARY KEY (`iduser_membership`),
  INDEX `fk_user_membership_usergroup1_idx` (`usergroup_id` ASC),
  INDEX `fk_user_membership_user1_idx` (`user_id` ASC),
  CONSTRAINT `fk_user_membership_usergroup1`
    FOREIGN KEY (`usergroup_id`)
    REFERENCES `mydb`.`usergroup` (`idusergroup`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_user_membership_user1`
    FOREIGN KEY (`user_id`)
    REFERENCES `mydb`.`user` (`iduser`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`note_type`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`note_type` (
  `idnote_type` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NULL,
  `description` LONGTEXT NULL,
  PRIMARY KEY (`idnote_type`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`note`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`note` (
  `idnote` INT NOT NULL AUTO_INCREMENT,
  `value` LONGTEXT NOT NULL,
  `note_type_id` INT NOT NULL,
  `user_id` INT NOT NULL,
  `usergroup_id` INT NOT NULL,
  PRIMARY KEY (`idnote`),
  INDEX `fk_note_note_type1_idx` (`note_type_id` ASC),
  INDEX `fk_note_user1_idx` (`user_id` ASC),
  INDEX `fk_note_usergroup1_idx` (`usergroup_id` ASC),
  CONSTRAINT `fk_note_note_type1`
    FOREIGN KEY (`note_type_id`)
    REFERENCES `mydb`.`note_type` (`idnote_type`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_note_user1`
    FOREIGN KEY (`user_id`)
    REFERENCES `mydb`.`user` (`iduser`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_note_usergroup1`
    FOREIGN KEY (`usergroup_id`)
    REFERENCES `mydb`.`usergroup` (`idusergroup`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`tag`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`tag` (
  `idtag` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NULL,
  PRIMARY KEY (`idtag`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`tagging`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`tagging` (
  `idtagging` INT NOT NULL AUTO_INCREMENT,
  `note_id` INT NOT NULL,
  `tag_id` INT NOT NULL,
  PRIMARY KEY (`idtagging`),
  INDEX `fk_tagging_note1_idx` (`note_id` ASC),
  INDEX `fk_tagging_tag1_idx` (`tag_id` ASC),
  CONSTRAINT `fk_tagging_note1`
    FOREIGN KEY (`note_id`)
    REFERENCES `mydb`.`note` (`idnote`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_tagging_tag1`
    FOREIGN KEY (`tag_id`)
    REFERENCES `mydb`.`tag` (`idtag`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`action`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`action` (
  `idaction` INT NOT NULL AUTO_INCREMENT,
  `content` LONGTEXT NULL,
  `user_id` INT NOT NULL,
  `note_id` INT NOT NULL,
  PRIMARY KEY (`idaction`),
  INDEX `fk_action_user1_idx` (`user_id` ASC),
  INDEX `fk_action_note1_idx` (`note_id` ASC),
  CONSTRAINT `fk_action_user1`
    FOREIGN KEY (`user_id`)
    REFERENCES `mydb`.`user` (`iduser`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_action_note1`
    FOREIGN KEY (`note_id`)
    REFERENCES `mydb`.`note` (`idnote`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
