CREATE DATABASE IF NOT EXISTS CHAMELEON;
USE CHAMELEON;

CREATE TABLE IF NOT EXISTS `usertbl` (
  `accountid` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `username` CHAR(255) NOT NULL,
  `password` VARCHAR(255) NOT NULL,
  `email` CHAR(255) NOT NULL,
  `first_name` VARCHAR(255) NOT NULL,
  `last_name` VARCHAR(255) NOT NULL,
  `address` VARCHAR(255),
  `cityid` INT,
  PRIMARY KEY (accountid),
  CONSTRAINT usertbl_unique UNIQUE(accountid, username, email)
) ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS `citytbl` (
  `cityid` INT UNIQUE PRIMARY KEY,
  `city_name` VARCHAR(255),
  `state` CHAR(255),
  `country` CHAR(255)
) ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS `posttbl` (
  `postid` INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY ,
  `accountid` INT UNSIGNED NOT NULL,
  `pictureid` INT UNSIGNED,
  `title` VARCHAR(255) NOT NULL,
  `description` BLOB,
  `address` VARCHAR(200),
  `cityid` INT,
  `tagname` VARCHAR(255),
  `post_type` CHAR(255),
  `renew_number` INT UNSIGNED,
  `renew_time` INT UNSIGNED,
  `timestamp` TIMESTAMP,
  `modified_time` TIMESTAMP,
  CONSTRAINT fk_accountid FOREIGN KEY (accountid) REFERENCES usertbl(accountid) ON DELETE CASCADE,
  CONSTRAINT fk_cityid FOREIGN KEY (cityid) REFERENCES citytbl(cityid),
  CONSTRAINT posttbl_unique UNIQUE(postid, pictureid)
) ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS `picturetbl` (
  `pictureid` INT UNSIGNED NOT NULL UNIQUE PRIMARY KEY,
  `postid` INT UNSIGNED NOT NULL UNIQUE,
  `source` CHAR(255),
  CONSTRAINT fk_picture_postid FOREIGN KEY (postid) REFERENCES posttbl(postid) ON DELETE CASCADE
) ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS `tagtbl` (
  `tagid` INT UNSIGNED NOT NULL UNIQUE PRIMARY KEY,
  `tagname` CHAR(255)
) ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS `tagmappingtbl` (
  `tagid` INT UNSIGNED NOT NULL UNIQUE PRIMARY KEY,
  `postid` INT UNSIGNED NOT NULL,
  `tagname` CHAR(255),
  CONSTRAINT fk_tag_postid FOREIGN KEY (postid) REFERENCES posttbl(postid) ON DELETE CASCADE
) ENGINE = InnoDB;
