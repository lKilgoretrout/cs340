CREATE DATABASE IOERD;
--USE IOERD;
DROP TABLE IF EXISTS `genres`;
CREATE TABLE `genres` (
  `genreID` int AUTO_INCREMENT,
  `genreName` varchar(255) NOT NULL,
  PRIMARY KEY (`genreID`),
  UNIQUE KEY `genreID` (`genreID`)
); 

INSERT INTO `genres` (genreName) VALUES ('None'),('Drama'),('Biography'),('Comedy'),('Action'),('Crime'),('Thriller'),('Western'),('Horror'),('Sci-Fi'),('Adventure'),('Mystery'),('Unknown'),('Fantasy'),('Documentary'),('Romance');


DROP TABLE IF EXISTS `movies`;
CREATE TABLE `movies` (
  `movieID` int NOT NULL AUTO_INCREMENT,
  `primaryTitle` varchar(255) NOT NULL,
  `startYear` int NOT NULL,
  `genreID` int,
  PRIMARY KEY (`movieID`),
  FOREIGN KEY (`genreID`) REFERENCES `genres` (`genreID`)
);
INSERT INTO `movies` VALUES (1,'Runaway Train',1985,4),(2,'Best of the Best',1989,4),(3,'By the Sword',1991,10),(4,'Love Is a Gun',1994,5),(5,'The Immortals',1995,4),(6,'It\'s My Party',1996,1),(7,'Power 98',1996,4),(8,'Heaven\'s Prisoners',1996,1),(9,'Past Perfect',1996,4),(10,'The Shadow Men',1997,4),(11,'Facade',1999,4),(12,'Purgatory',1999,13),(13,'Two Shades of Blue',1999,6),(14,'Restraining Order',1999,4),(15,'Tripfall',2000,6),(16,'No Alibi',2000,5),(17,'Luck of the Draw',2000,5),(18,'Miss Castaway and the Island Girls',2004,10),(19,'First Dog',2010,3),(20,'The Human Centipede III (Final Sequence)',2015,3),(21,'Eyes of the Roshi',2017,4),(22,'Untitled Michael Andretti Project',420,14),(23,'A Perfect Chaos',420,3),(24,'Victory by Submission',2017,1),(25,'Enemy Within',2016,4),(26,'Stalked by My Doctor',2015,6),(27,'Someone Dies Tonight',2022,6),(28,'Rusty Tulloch',2018,4);


DROP TABLE IF EXISTS `actors`;
CREATE TABLE `actors` (
  `actorID` int NOT NULL AUTO_INCREMENT,
  `primaryName` varchar(255) NOT NULL,
  PRIMARY KEY (`actorID`)
);

INSERT INTO `actors` VALUES (1,'Eric Roberts'),(2,'Rebecca De Mornay'),(3,'Jon Voight'),(4,'Misha Segal'),(5,'Dan Schlaack'),(6,'Sabine El Gemayel'),(7,'Marc Grossman'),(8,'Caitlin Blue'),(9,'Egidio Tari'),(10,'David R. Casey'),(11,'Richard Foreman Jr.'),(12,'Kandice King'),(13,'Timothy Bond'),(14,'Robyn Knoll'),(15,'Mick Erausquin'),(16,'Michael B. Druxman'),(17,'Gloria Pryor'),(18,'Timothy J. Warenz'),(19,'Christian Williams'),(20,'Bethany Scott'),(21,'Michael Andretti'),(22,'Paulo Benedeti'),(23,'Paula Devicq'),(24,'Tatjana Patitz'),(25,'Brad Rowe'),(26,'Bernd Heinl'),(27,'Chuck Cirino'),(28,'Antonio Vivaldi'),(29,'Axel Melzener'),(30,'Richard Halpern'),(31,'Kelly Deco'),(32,'Paul van den Boom'),(33,'Ken Sanders'),(34,'Pat Tagliaferro'),(35,'Katherine Dover'),(36,'James Shavick'),(37,'Bryce Zabel'),(38,'Larry Abrams'),(39,'Deana Molle'),(40,'Tara Marks'),(41,'David Adams'),(42,'John Adams'),(43,'Paige Adams'),(44,'C.C. Adcock'),(45,'Gale M. Adler'),(46,'Justin Adler'),(47,'Terrance Afer-Anderson'),(48,'Roy Ageloff'),(49,'David Agresta'),(50,'Fatos Akdeniz');


DROP TABLE IF EXISTS `actors_movies`;
CREATE TABLE `actors_movies` (
  `actorID` int,
  `movieID` int,
  PRIMARY KEY (`actorID`, `movieID`),
  FOREIGN KEY (`actorID`) REFERENCES `actors` (`actorID`) ON DELETE CASCADE,
  FOREIGN KEY (`movieID`) REFERENCES `movies` (`movieID`) ON DELETE CASCADE
); 

INSERT INTO `actors_movies` VALUES (2,1),(1,1),(3,1),(4,20),(5,15),(6,5),(7,4),(8,7),(9,2),(10,1),(11,17),(12,10),(13,11),(14,14),(15,18),(16,8),(17,22),(18,25),(19,19),(20,14),(21,12),(22,6),(23,28),(24,1),(25,27),(26,18),(27,1),(28,16),(29,26),(30,1),(31,1),(32,9),(33,3),(34,23),(35,24),(36,8),(37,2),(38,11),(39,8),(40,1),(41,21),(42,13),(43,2);

DROP TABLE IF EXISTS `characters`;
CREATE TABLE `characters` (
  `characterID` int NOT NULL AUTO_INCREMENT,
  `characterName` varchar(255) NOT NULL,
  `actorID` int,
  `movieID` int,
  PRIMARY KEY (`characterID`),
  FOREIGN KEY (`actorID`) REFERENCES `actors` (`actorID`) ,
  FOREIGN KEY (`movieID`) REFERENCES `movies` (`movieID`) 
);
INSERT INTO `characters` (characterName, actorID, movieID) VALUES ('Buck',1,1),('Sara',2,1),('Alex Grady',2,2),('Villard',3,3),('Jack Hart',4,4),('Jack',5,5),('Nick Stark',6,6),('Karlin Pickett',7,7),('Bubba Rocque',8,8),('Dylan Cooper',1,9),('Bob Wilson',1,10),('Colin Wentworth',1,11),('Blackjack Britton',9,12),('Calvin Stasi',10,13),('Robert Woodfield',11,14),('Mr. Eddie',12,15),('Victor Haddock',13,16),('Stanley Joiner',14,16),('Carlo',15,17),('Maximus Powers',14,18),('President of the United States',16,19),('Governor Hughes',17,20),('Booker',18,21),('Narrator',12,22),('Carl Bigsby',22,23),('Leon \'The Neon\' Harris',23,24),('Jack #2',24,25),('Dr. Beck',24,26),('Niko Dukakis',25,27),('Mr. G',28,28);


