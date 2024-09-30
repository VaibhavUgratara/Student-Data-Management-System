-- MySQL dump 10.13  Distrib 8.0.36, for Win64 (x86_64)
--
-- Host: localhost    Database: test
-- ------------------------------------------------------
-- Server version	8.0.36

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `activity`
--

DROP TABLE IF EXISTS `activity`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `activity` (
  `s_ID` bigint DEFAULT NULL,
  `s_name` varchar(50) DEFAULT NULL,
  `club1` varchar(50) DEFAULT NULL,
  `club2` varchar(50) DEFAULT NULL,
  `club3` varchar(50) DEFAULT NULL,
  `applied` char(3) DEFAULT 'no',
  `granted` char(3) DEFAULT 'no'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `activity`
--

LOCK TABLES `activity` WRITE;
/*!40000 ALTER TABLE `activity` DISABLE KEYS */;
INSERT INTO `activity` VALUES (223117,'Kumar Vaibhav Ugratara','Coding','Sports','','yes','yes'),(223456,'Ramesh',NULL,NULL,NULL,'no','no'),(223145,'John Doe','Coding','Sports','Dance','yes','yes');
/*!40000 ALTER TABLE `activity` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `attendance`
--

DROP TABLE IF EXISTS `attendance`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `attendance` (
  `s_ID` bigint DEFAULT NULL,
  `total_days` int DEFAULT NULL,
  `present` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `attendance`
--

LOCK TABLES `attendance` WRITE;
/*!40000 ALTER TABLE `attendance` DISABLE KEYS */;
INSERT INTO `attendance` VALUES (223117,16,13),(223456,0,0),(223145,0,0);
/*!40000 ALTER TABLE `attendance` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `marks`
--

DROP TABLE IF EXISTS `marks`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `marks` (
  `s_ID` bigint DEFAULT NULL,
  `s_name` varchar(30) DEFAULT NULL,
  `semester` int DEFAULT NULL,
  `sub1` char(10) DEFAULT NULL,
  `grade1` char(2) DEFAULT NULL,
  `sub2` char(10) DEFAULT NULL,
  `grade2` char(2) DEFAULT NULL,
  `sub3` char(10) DEFAULT NULL,
  `grade3` char(2) DEFAULT NULL,
  `sub4` char(10) DEFAULT NULL,
  `grade4` char(2) DEFAULT NULL,
  `sub5` char(10) DEFAULT NULL,
  `grade5` char(2) DEFAULT NULL,
  `cgpa` char(5) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `marks`
--

LOCK TABLES `marks` WRITE;
/*!40000 ALTER TABLE `marks` DISABLE KEYS */;
INSERT INTO `marks` VALUES (223117,'Kumar Vaibhav Ugratara',2,'BCA-201','A1','BCA-202','A2','BCA-203','A2','BCA-204','A1','BCA-205','A1','9.6');
/*!40000 ALTER TABLE `marks` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `scholarship`
--

DROP TABLE IF EXISTS `scholarship`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `scholarship` (
  `s_ID` bigint DEFAULT NULL,
  `salary` varchar(15) DEFAULT NULL,
  `applied` char(3) DEFAULT 'no',
  `granted` char(3) DEFAULT 'no',
  `bank` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `scholarship`
--

LOCK TABLES `scholarship` WRITE;
/*!40000 ALTER TABLE `scholarship` DISABLE KEYS */;
INSERT INTO `scholarship` VALUES (223117,'2,00,000','yes','yes','1234567'),(223456,NULL,'yes','no',NULL),(223145,'2,00,000','yes','yes','1234123412341234');
/*!40000 ALTER TABLE `scholarship` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `student`
--

DROP TABLE IF EXISTS `student`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `student` (
  `st_id` int DEFAULT NULL,
  `st_name` varchar(50) DEFAULT NULL,
  `st_pass` varchar(50) DEFAULT NULL,
  `st_email` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `student`
--

LOCK TABLES `student` WRITE;
/*!40000 ALTER TABLE `student` DISABLE KEYS */;
INSERT INTO `student` VALUES (223117,'Kumar Vaibhav Ugratara','asdf@123','v.assertive@gmail.com'),(223145,'John Doe','asdf@123','v.assertive@gmail.com');
/*!40000 ALTER TABLE `student` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `student_details`
--

DROP TABLE IF EXISTS `student_details`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `student_details` (
  `st_name` varchar(50) DEFAULT NULL,
  `course` varchar(20) DEFAULT NULL,
  `semester` int DEFAULT NULL,
  `year` char(9) DEFAULT NULL,
  `f_name` varchar(50) DEFAULT NULL,
  `m_name` varchar(50) DEFAULT NULL,
  `guardian` varchar(50) DEFAULT NULL,
  `st_ID` int DEFAULT NULL,
  `enroll` varchar(10) DEFAULT NULL,
  `mob` bigint DEFAULT NULL,
  `email` varchar(50) DEFAULT NULL,
  `dob` date DEFAULT NULL,
  `pass_12` char(4) DEFAULT NULL,
  `pass_10` char(4) DEFAULT NULL,
  `blood` char(3) DEFAULT NULL,
  `address` varchar(200) DEFAULT NULL,
  `ispwd` char(3) DEFAULT NULL,
  `disability` varchar(30) DEFAULT NULL,
  `per_12` varchar(5) DEFAULT NULL,
  `per_10` varchar(5) DEFAULT NULL,
  `nationality` varchar(10) DEFAULT NULL,
  `gender` char(10) DEFAULT NULL,
  `aadhar` bigint DEFAULT NULL,
  `f_qual` varchar(20) DEFAULT NULL,
  `m_qual` varchar(20) DEFAULT NULL,
  `f_occ` varchar(30) DEFAULT NULL,
  `m_occ` varchar(30) DEFAULT NULL,
  `f_no` bigint DEFAULT NULL,
  `m_no` bigint DEFAULT NULL,
  `alt_no` bigint DEFAULT NULL,
  `alt_mail` varchar(30) DEFAULT NULL,
  `f_mail` varchar(30) DEFAULT NULL,
  `m_mail` varchar(30) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `student_details`
--

LOCK TABLES `student_details` WRITE;
/*!40000 ALTER TABLE `student_details` DISABLE KEYS */;
INSERT INTO `student_details` VALUES ('Kumar Vaibhav Ugratara','B.C.A.',4,'2022-2025','Jeevan Kumar','Madhulika','Jeevan Kumar',223117,'AC-061/22',7488482702,'v.assertive@gmail.com','2003-07-18','2021','2019','O+','Bokaro Thermal','No','','94.06','94.04','Indian','Male',354212345678,'Graduation','Graduation','Business','Housewife',NULL,NULL,NULL,NULL,NULL,NULL),('John Doe','B.C.A.',1,'2024-2025','Keith Doe','Mary Doe','Keith Doe',223145,'AC-091/24',7488482702,'v.assertive@gmail.com','2006-08-08','2024','2022','O+','Greater Noida, Uttar Pradesh','No','','94.04','96.02','Indian','Male',123467893455,'B.Tech.','B. Com.','Business','Housewife',9999999999,8888888888,NULL,NULL,'keith@gmail.com','mary@gmail.com');
/*!40000 ALTER TABLE `student_details` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `student_gen`
--

DROP TABLE IF EXISTS `student_gen`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `student_gen` (
  `id` int DEFAULT NULL,
  `name` varchar(50) DEFAULT NULL,
  `email` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `student_gen`
--

LOCK TABLES `student_gen` WRITE;
/*!40000 ALTER TABLE `student_gen` DISABLE KEYS */;
/*!40000 ALTER TABLE `student_gen` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `teacher`
--

DROP TABLE IF EXISTS `teacher`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `teacher` (
  `t_id` bigint DEFAULT NULL,
  `t_pass` varchar(20) DEFAULT NULL,
  `t_email` varchar(50) DEFAULT NULL,
  `t_number` bigint DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `teacher`
--

LOCK TABLES `teacher` WRITE;
/*!40000 ALTER TABLE `teacher` DISABLE KEYS */;
INSERT INTO `teacher` VALUES (101,'python@123','v.assertive@gmail.com',7488482702);
/*!40000 ALTER TABLE `teacher` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-05-07 10:43:47
