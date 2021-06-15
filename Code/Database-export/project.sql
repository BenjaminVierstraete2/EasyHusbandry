-- MySQL dump 10.13  Distrib 8.0.25, for Win64 (x86_64)
--
-- Host: localhost    Database: project
-- ------------------------------------------------------
-- Server version	8.0.19

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `settings`
--

DROP TABLE IF EXISTS `settings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `settings` (
  `settingID` int NOT NULL AUTO_INCREMENT,
  `tempMet` VARCHAR(25),
  `minTemp` float,
  `minLight` float,
  `minHum` float,
  `maxTemp` float,
  `maxHum` float,
  `fan`varchar(25),
  `lamp`VARCHAR(25),
  `startTime`VARCHAR(25),
  `endTime`VARCHAR(25),
   PRIMARY KEY (`settingID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `settings`
--

LOCK TABLES `settings` WRITE;
/*!40000 ALTER TABLE `settings` DISABLE KEYS */;
INSERT INTO `settings` values (1,'c',15,40,40,23,90,'Auto','Auto','08:00','20:00');
/*!40000 ALTER TABLE `settings` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tblactuators`
--

DROP TABLE IF EXISTS `tblactuators`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tblactuators` (
  `actuatorID` int NOT NULL,
  `status` bit(1) DEFAULT NULL,
  `actuatorName` varchar(45) NOT NULL,
  PRIMARY KEY (`actuatorID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tblactuators`
--

LOCK TABLES `tblactuators` WRITE;
/*!40000 ALTER TABLE `tblactuators` DISABLE KEYS */;
INSERT INTO `tblactuators` VALUES (1,NULL,'Fan'),(2,NULL,'Lamp');
/*!40000 ALTER TABLE `tblactuators` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tblreads`
--

DROP TABLE IF EXISTS `tblreads`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tblreads` (
  `readID` int NOT NULL AUTO_INCREMENT,
  `sensorID` int NOT NULL,
  `timeRead` datetime DEFAULT NULL,
  `value` float DEFAULT NULL,
  PRIMARY KEY (`readID`),
  KEY `sensorID_idx` (`sensorID`),
  CONSTRAINT `sensorID` FOREIGN KEY (`sensorID`) REFERENCES `tblsensors` (`sensorID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tblreads`
--

LOCK TABLES `tblreads` WRITE;
/*!40000 ALTER TABLE `tblreads` DISABLE KEYS */;
/*!40000 ALTER TABLE `tblreads` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tblsensors`
--

DROP TABLE IF EXISTS `tblsensors`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tblsensors` (
  `sensorID` int NOT NULL,
  `status` bit(1) DEFAULT NULL,
  `sensorName` varchar(45) NOT NULL,
  PRIMARY KEY (`sensorID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tblsensors`
--

LOCK TABLES `tblsensors` WRITE;
/*!40000 ALTER TABLE `tblsensors` DISABLE KEYS */;
INSERT INTO `tblsensors` VALUES (1,NULL,'Onewire'),(2,NULL,'LDR'),(3,NULL,'DH11');
/*!40000 ALTER TABLE `tblsensors` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tblstatus`
--

DROP TABLE IF EXISTS `tblstatus`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tblstatus` (
  `statusID` int NOT NULL AUTO_INCREMENT,
  `statusChange` datetime DEFAULT NULL,
  `changedState` bit(1) DEFAULT NULL,
  `actuatorID` int NOT NULL,
  PRIMARY KEY (`statusID`),
  KEY `actuatorID_idx` (`actuatorID`),
  CONSTRAINT `actuatorID` FOREIGN KEY (`actuatorID`) REFERENCES `tblactuators` (`actuatorID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tblstatus`
--

LOCK TABLES `tblstatus` WRITE;
/*!40000 ALTER TABLE `tblstatus` DISABLE KEYS */;
INSERT INTO `tblstatus` values (1, null,0,1),(2,null,0,2);
/*!40000 ALTER TABLE `tblstatus` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-05-24 15:19:43
