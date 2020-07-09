-- MySQL dump 10.13  Distrib 8.0.20, for Win64 (x86_64)
--
-- Host: localhost    Database: gp1modeltosql
-- ------------------------------------------------------
-- Server version	5.6.48

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
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
INSERT INTO `auth_group` VALUES (1,'职员');
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
INSERT INTO `auth_group_permissions` VALUES (1,1,25),(2,1,26),(3,1,27),(4,1,28),(5,1,29),(6,1,30),(7,1,31),(8,1,32),(9,1,48),(10,1,49),(11,1,50),(12,1,51),(13,1,52),(14,1,129),(15,1,130),(16,1,131),(17,1,132);
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=133 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add user',4,'add_user'),(14,'Can change user',4,'change_user'),(15,'Can delete user',4,'delete_user'),(16,'Can view user',4,'view_user'),(17,'Can add content type',5,'add_contenttype'),(18,'Can change content type',5,'change_contenttype'),(19,'Can delete content type',5,'delete_contenttype'),(20,'Can view content type',5,'view_contenttype'),(21,'Can add session',6,'add_session'),(22,'Can change session',6,'change_session'),(23,'Can delete session',6,'delete_session'),(24,'Can view session',6,'view_session'),(25,'Can add 路线',7,'add_offlinemapmanage'),(26,'Can change 路线',7,'change_offlinemapmanage'),(27,'Can delete 路线',7,'delete_offlinemapmanage'),(28,'Can view 路线',7,'view_offlinemapmanage'),(29,'Can add 离线任务预处理',8,'add_offlinepreprocessset'),(30,'Can change 离线任务预处理',8,'change_offlinepreprocessset'),(31,'Can delete 离线任务预处理',8,'delete_offlinepreprocessset'),(32,'Can view 离线任务预处理',8,'view_offlinepreprocessset'),(33,'Can add 图片比对信息',9,'add_singleimagecompareinfo'),(34,'Can change 图片比对信息',9,'change_singleimagecompareinfo'),(35,'Can delete 图片比对信息',9,'delete_singleimagecompareinfo'),(36,'Can view 图片比对信息',9,'view_singleimagecompareinfo'),(37,'Can add 图片识别信息',10,'add_singleimageidentifyinfo'),(38,'Can change 图片识别信息',10,'change_singleimageidentifyinfo'),(39,'Can delete 图片识别信息',10,'delete_singleimageidentifyinfo'),(40,'Can view 图片识别信息',10,'view_singleimageidentifyinfo'),(41,'Can add 图片预处理信息',11,'add_singleimagepreprocessinfo'),(42,'Can change 图片预处理信息',11,'change_singleimagepreprocessinfo'),(43,'Can delete 图片预处理信息',11,'delete_singleimagepreprocessinfo'),(44,'Can view 图片预处理信息',11,'view_singleimagepreprocessinfo'),(45,'Can add 图片拼接信息',12,'add_singleimagespliceinfo'),(46,'Can change 图片拼接信息',12,'change_singleimagespliceinfo'),(47,'Can delete 图片拼接信息',12,'delete_singleimagespliceinfo'),(48,'Can view 图片拼接信息',12,'view_singleimagespliceinfo'),(49,'Can add 离线任务',13,'add_offlinetask'),(50,'Can change 离线任务',13,'change_offlinetask'),(51,'Can delete 离线任务',13,'delete_offlinetask'),(52,'Can view 离线任务',13,'view_offlinetask'),(53,'Can add crontab',14,'add_crontabschedule'),(54,'Can change crontab',14,'change_crontabschedule'),(55,'Can delete crontab',14,'delete_crontabschedule'),(56,'Can view crontab',14,'view_crontabschedule'),(57,'Can add interval',15,'add_intervalschedule'),(58,'Can change interval',15,'change_intervalschedule'),(59,'Can delete interval',15,'delete_intervalschedule'),(60,'Can view interval',15,'view_intervalschedule'),(61,'Can add periodic task',16,'add_periodictask'),(62,'Can change periodic task',16,'change_periodictask'),(63,'Can delete periodic task',16,'delete_periodictask'),(64,'Can view periodic task',16,'view_periodictask'),(65,'Can add periodic tasks',17,'add_periodictasks'),(66,'Can change periodic tasks',17,'change_periodictasks'),(67,'Can delete periodic tasks',17,'delete_periodictasks'),(68,'Can view periodic tasks',17,'view_periodictasks'),(69,'Can add task state',18,'add_taskmeta'),(70,'Can change task state',18,'change_taskmeta'),(71,'Can delete task state',18,'delete_taskmeta'),(72,'Can view task state',18,'view_taskmeta'),(73,'Can add saved group result',19,'add_tasksetmeta'),(74,'Can change saved group result',19,'change_tasksetmeta'),(75,'Can delete saved group result',19,'delete_tasksetmeta'),(76,'Can view saved group result',19,'view_tasksetmeta'),(77,'Can add task',20,'add_taskstate'),(78,'Can change task',20,'change_taskstate'),(79,'Can delete task',20,'delete_taskstate'),(80,'Can view task',20,'view_taskstate'),(81,'Can add worker',21,'add_workerstate'),(82,'Can change worker',21,'change_workerstate'),(83,'Can delete worker',21,'delete_workerstate'),(84,'Can view worker',21,'view_workerstate'),(85,'Can add Bookmark',22,'add_bookmark'),(86,'Can change Bookmark',22,'change_bookmark'),(87,'Can delete Bookmark',22,'delete_bookmark'),(88,'Can view Bookmark',22,'view_bookmark'),(89,'Can add User Setting',23,'add_usersettings'),(90,'Can change User Setting',23,'change_usersettings'),(91,'Can delete User Setting',23,'delete_usersettings'),(92,'Can view User Setting',23,'view_usersettings'),(93,'Can add User Widget',24,'add_userwidget'),(94,'Can change User Widget',24,'change_userwidget'),(95,'Can delete User Widget',24,'delete_userwidget'),(96,'Can view User Widget',24,'view_userwidget'),(97,'Can add log entry',25,'add_log'),(98,'Can change log entry',25,'change_log'),(99,'Can delete log entry',25,'delete_log'),(100,'Can view log entry',25,'view_log'),(101,'Can add revision',26,'add_revision'),(102,'Can change revision',26,'change_revision'),(103,'Can delete revision',26,'delete_revision'),(104,'Can view revision',26,'view_revision'),(105,'Can add version',27,'add_version'),(106,'Can change version',27,'change_version'),(107,'Can delete version',27,'delete_version'),(108,'Can view version',27,'view_version'),(125,'Can add 在线识别信息',28,'add_onlineimageidentifyinfo'),(126,'Can change 在线识别信息',28,'change_onlineimageidentifyinfo'),(127,'Can delete 在线识别信息',28,'delete_onlineimageidentifyinfo'),(128,'Can view 在线识别信息',28,'view_onlineimageidentifyinfo'),(129,'Can add 在线任务',29,'add_onlinetask'),(130,'Can change 在线任务',29,'change_onlinetask'),(131,'Can delete 在线任务',29,'delete_onlinetask'),(132,'Can view 在线任务',29,'view_onlinetask');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$150000$iWH7UG22GDCz$u+4fdgISoumpkK81fpZgHkeErXd6LZYXnHTYHH79z6o=','2020-06-29 15:35:24.591615',0,'admin','','','1234567@qq.com',1,1,'2020-06-04 15:35:45.077878');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
INSERT INTO `auth_user_groups` VALUES (1,1,1);
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `celery_taskmeta`
--

DROP TABLE IF EXISTS `celery_taskmeta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `celery_taskmeta` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `task_id` varchar(255) NOT NULL,
  `status` varchar(50) NOT NULL,
  `result` longtext,
  `date_done` datetime(6) NOT NULL,
  `traceback` longtext,
  `hidden` tinyint(1) NOT NULL,
  `meta` longtext,
  PRIMARY KEY (`id`),
  UNIQUE KEY `task_id` (`task_id`),
  KEY `celery_taskmeta_hidden_23fd02dc` (`hidden`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `celery_taskmeta`
--

LOCK TABLES `celery_taskmeta` WRITE;
/*!40000 ALTER TABLE `celery_taskmeta` DISABLE KEYS */;
/*!40000 ALTER TABLE `celery_taskmeta` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `celery_tasksetmeta`
--

DROP TABLE IF EXISTS `celery_tasksetmeta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `celery_tasksetmeta` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `taskset_id` varchar(255) NOT NULL,
  `result` longtext NOT NULL,
  `date_done` datetime(6) NOT NULL,
  `hidden` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `taskset_id` (`taskset_id`),
  KEY `celery_tasksetmeta_hidden_593cfc24` (`hidden`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `celery_tasksetmeta`
--

LOCK TABLES `celery_tasksetmeta` WRITE;
/*!40000 ALTER TABLE `celery_tasksetmeta` DISABLE KEYS */;
/*!40000 ALTER TABLE `celery_tasksetmeta` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=168 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (1,'2020-06-04 16:23:01.963913','1','测试',1,'[{\"added\": {}}]',7,1),(2,'2020-06-04 16:23:26.782671','1','壹号文件',1,'[{\"added\": {}}]',8,1),(3,'2020-06-04 16:37:40.047992','1','OfflineTask object (1)',1,'[{\"added\": {}}]',13,1),(4,'2020-06-05 08:25:00.332572','2','OfflineTask object (2)',1,'[{\"added\": {}}]',13,1),(5,'2020-06-05 08:28:41.232381','3','OfflineTask object (3)',1,'[{\"added\": {}}]',13,1),(6,'2020-06-05 08:29:28.371915','3','OfflineTask object (3)',3,'',13,1),(7,'2020-06-05 08:29:28.393857','2','OfflineTask object (2)',3,'',13,1),(8,'2020-06-05 08:29:28.452701','1','OfflineTask object (1)',3,'',13,1),(9,'2020-06-05 08:29:43.580560','4','OfflineTask object (4)',1,'[{\"added\": {}}]',13,1),(10,'2020-06-05 08:37:14.192879','5','OfflineTask object (5)',1,'[{\"added\": {}}]',13,1),(11,'2020-06-05 08:38:07.832458','6','OfflineTask object (6)',1,'[{\"added\": {}}]',13,1),(12,'2020-06-05 08:42:11.605118','7','OfflineTask object (7)',1,'[{\"added\": {}}]',13,1),(13,'2020-06-05 08:43:58.505318','8','OfflineTask object (8)',1,'[{\"added\": {}}]',13,1),(14,'2020-06-05 08:45:23.552974','8','OfflineTask object (8)',3,'',13,1),(15,'2020-06-05 08:45:23.586648','7','OfflineTask object (7)',3,'',13,1),(16,'2020-06-05 08:45:23.602637','6','OfflineTask object (6)',3,'',13,1),(17,'2020-06-05 08:45:23.661599','5','OfflineTask object (5)',3,'',13,1),(18,'2020-06-05 08:45:23.677863','4','OfflineTask object (4)',3,'',13,1),(19,'2020-06-05 08:45:38.594377','9','OfflineTask object (9)',1,'[{\"added\": {}}]',13,1),(20,'2020-06-05 08:57:34.937066','2','操场',1,'[{\"added\": {}}]',7,1),(21,'2020-06-05 08:57:47.722752','10','OfflineTask object (10)',1,'[{\"added\": {}}]',13,1),(22,'2020-06-05 08:59:59.337095','11','OfflineTask object (11)',1,'[{\"added\": {}}]',13,1),(23,'2020-06-05 09:03:01.471291','12','OfflineTask object (12)',1,'[{\"added\": {}}]',13,1),(24,'2020-06-05 09:06:27.036988','13','OfflineTask object (13)',1,'[{\"added\": {}}]',13,1),(25,'2020-06-05 09:19:46.085243','14','OfflineTask object (14)',1,'[{\"added\": {}}]',13,1),(26,'2020-06-05 09:25:35.781064','15','OfflineTask object (15)',1,'[{\"added\": {}}]',13,1),(27,'2020-06-05 09:31:16.161480','16','OfflineTask object (16)',1,'[{\"added\": {}}]',13,1),(28,'2020-06-05 09:34:37.477302','17','OfflineTask object (17)',1,'[{\"added\": {}}]',13,1),(29,'2020-06-05 09:40:11.726073','18','OfflineTask object (18)',1,'[{\"added\": {}}]',13,1),(30,'2020-06-05 09:42:35.615024','19','OfflineTask object (19)',1,'[{\"added\": {}}]',13,1),(31,'2020-06-05 09:46:55.171398','20','OfflineTask object (20)',1,'[{\"added\": {}}]',13,1),(32,'2020-06-05 09:49:05.754262','21','OfflineTask object (21)',1,'[{\"added\": {}}]',13,1),(33,'2020-06-16 10:51:42.879636','21','OfflineTask object (21)',3,'',13,1),(34,'2020-06-16 11:07:21.448223','22','OfflineTask object (22)',1,'[{\"added\": {}}]',13,1),(35,'2020-06-16 11:09:00.040853','23','OfflineTask object (23)',1,'[{\"added\": {}}]',13,1),(36,'2020-06-16 11:17:34.232094','24','OfflineTask object (24)',1,'[{\"added\": {}}]',13,1),(37,'2020-06-16 11:21:07.059812','25','OfflineTask object (25)',1,'[{\"added\": {}}]',13,1),(38,'2020-06-16 11:22:11.795723','3','新电脑',1,'[{\"added\": {}}]',7,1),(39,'2020-06-16 11:23:10.408871','2','贰号文件',1,'[{\"added\": {}}]',8,1),(40,'2020-06-16 11:24:26.393602','26','OfflineTask object (26)',1,'[{\"added\": {}}]',13,1),(41,'2020-06-16 15:56:57.005942','27','OfflineTask object (27)',1,'[{\"added\": {}}]',13,1),(42,'2020-06-16 16:38:57.489176','27','OfflineTask object (27)',3,'',13,1),(43,'2020-06-16 16:38:58.794521','27','OfflineTask object (27)',3,'',13,1),(44,'2020-06-16 16:38:59.684938','26','OfflineTask object (26)',3,'',13,1),(45,'2020-06-16 16:38:59.841248','26','OfflineTask object (26)',3,'',13,1),(46,'2020-06-16 16:39:00.351817','25','OfflineTask object (25)',3,'',13,1),(47,'2020-06-16 16:39:00.472453','25','OfflineTask object (25)',3,'',13,1),(48,'2020-06-16 16:39:00.572800','24','OfflineTask object (24)',3,'',13,1),(49,'2020-06-16 16:39:00.671081','24','OfflineTask object (24)',3,'',13,1),(50,'2020-06-16 16:39:00.772241','23','OfflineTask object (23)',3,'',13,1),(51,'2020-06-16 16:39:00.860159','23','OfflineTask object (23)',3,'',13,1),(52,'2020-06-16 17:01:37.658097','1','OfflineTask object (1)',1,'[{\"added\": {}}]',13,1),(53,'2020-06-17 08:36:45.529516','2','OfflineTask object (2)',1,'[{\"added\": {}}]',13,1),(54,'2020-06-17 08:39:01.294272','3','OfflineTask object (3)',1,'[{\"added\": {}}]',13,1),(55,'2020-06-17 09:02:37.233286','4','OfflineTask object (4)',1,'[{\"added\": {}}]',13,1),(56,'2020-06-17 17:04:00.018110','5','OfflineTask object (5)',1,'[{\"added\": {}}]',13,1),(57,'2020-06-17 17:04:15.270874','5','OfflineTask object (5)',3,'',13,1),(58,'2020-06-17 17:04:35.558311','6','OfflineTask object (6)',1,'[{\"added\": {}}]',13,1),(59,'2020-06-18 09:33:43.056216','7','OfflineTask object (7)',1,'[{\"added\": {}}]',13,1),(60,'2020-06-18 09:34:58.766023','8','OfflineTask object (8)',1,'[{\"added\": {}}]',13,1),(61,'2020-06-23 09:27:22.259966','9','OfflineTask object (9)',1,'[{\"added\": {}}]',13,1),(62,'2020-06-23 09:34:18.218787','10','OfflineTask object (10)',1,'[{\"added\": {}}]',13,1),(63,'2020-06-23 09:43:40.165375','11','OfflineTask object (11)',1,'[{\"added\": {}}]',13,1),(64,'2020-06-23 09:56:46.969199','12','OfflineTask object (12)',1,'[{\"added\": {}}]',13,1),(65,'2020-06-23 09:58:57.057452','13','OfflineTask object (13)',1,'[{\"added\": {}}]',13,1),(66,'2020-06-23 10:03:01.317793','14','OfflineTask object (14)',1,'[{\"added\": {}}]',13,1),(67,'2020-06-30 09:08:26.354822','15','OfflineTask object (15)',1,'[{\"added\": {}}]',13,1),(68,'2020-06-30 09:16:00.580741','16','OfflineTask object (16)',1,'[{\"added\": {}}]',13,1),(69,'2020-06-30 09:26:27.932247','17','OfflineTask object (17)',1,'[{\"added\": {}}]',13,1),(70,'2020-06-30 16:02:51.786028','18','OfflineTask object (18)',1,'[{\"added\": {}}]',13,1),(71,'2020-06-30 16:05:23.595833','19','OfflineTask object (19)',1,'[{\"added\": {}}]',13,1),(72,'2020-06-30 16:18:20.659159','20','OfflineTask object (20)',1,'[{\"added\": {}}]',13,1),(73,'2020-07-02 14:38:45.927608','21','OfflineTask object (21)',1,'[{\"added\": {}}]',13,1),(74,'2020-07-06 10:25:34.764561','1','OnlineTask object (1)',1,'[{\"added\": {}}]',29,1),(75,'2020-07-06 10:27:51.763072','2','OnlineTask object (2)',1,'[{\"added\": {}}]',29,1),(76,'2020-07-06 10:48:00.208032','3','OnlineTask object (3)',1,'[{\"added\": {}}]',29,1),(77,'2020-07-06 10:50:41.849215','4','OnlineTask object (4)',1,'[{\"added\": {}}]',29,1),(78,'2020-07-07 11:07:42.086176','1','OnlineTask object (1)',1,'[{\"added\": {}}]',29,1),(79,'2020-07-07 15:21:21.405602','2','OnlineTask object (2)',1,'[{\"added\": {}}]',29,1),(80,'2020-07-07 15:34:46.436402','2','OnlineTask object (2)',3,'',29,1),(81,'2020-07-07 15:34:58.725683','3','OnlineTask object (3)',1,'[{\"added\": {}}]',29,1),(82,'2020-07-07 15:37:00.416404','3','OnlineTask object (3)',3,'',29,1),(83,'2020-07-07 15:37:07.934087','4','OnlineTask object (4)',1,'[{\"added\": {}}]',29,1),(84,'2020-07-07 15:48:26.440882','5','OnlineTask object (5)',1,'[{\"added\": {}}]',29,1),(85,'2020-07-07 15:56:02.246233','6','OnlineTask object (6)',1,'[{\"added\": {}}]',29,1),(86,'2020-07-07 15:56:11.409440','5','OnlineTask object (5)',3,'',29,1),(87,'2020-07-07 15:56:11.539395','4','OnlineTask object (4)',3,'',29,1),(88,'2020-07-07 15:58:06.534854','7','OnlineTask object (7)',1,'[{\"added\": {}}]',29,1),(89,'2020-07-07 15:58:16.822570','6','OnlineTask object (6)',3,'',29,1),(90,'2020-07-07 16:01:12.735264','8','OnlineTask object (8)',1,'[{\"added\": {}}]',29,1),(91,'2020-07-07 16:02:20.158244','9','OnlineTask object (9)',1,'[{\"added\": {}}]',29,1),(92,'2020-07-07 16:02:25.772943','8','OnlineTask object (8)',3,'',29,1),(93,'2020-07-07 16:02:25.903592','7','OnlineTask object (7)',3,'',29,1),(94,'2020-07-07 16:04:47.464731','10','OnlineTask object (10)',1,'[{\"added\": {}}]',29,1),(95,'2020-07-07 16:06:06.598992','11','OnlineTask object (11)',1,'[{\"added\": {}}]',29,1),(96,'2020-07-07 16:08:39.704132','12','OnlineTask object (12)',1,'[{\"added\": {}}]',29,1),(97,'2020-07-07 16:13:57.802213','13','OnlineTask object (13)',1,'[{\"added\": {}}]',29,1),(98,'2020-07-07 16:15:59.912444','14','OnlineTask object (14)',1,'[{\"added\": {}}]',29,1),(99,'2020-07-07 16:21:24.876722','14','OnlineTask object (14)',3,'',29,1),(100,'2020-07-07 16:21:39.201191','15','OnlineTask object (15)',1,'[{\"added\": {}}]',29,1),(101,'2020-07-07 16:34:35.332502','16','OnlineTask object (16)',1,'[{\"added\": {}}]',29,1),(102,'2020-07-07 17:03:05.979424','17','OnlineTask object (17)',1,'[{\"added\": {}}]',29,1),(103,'2020-07-08 08:20:22.848589','17','OnlineTask object (17)',3,'',29,1),(104,'2020-07-08 08:20:23.027903','16','OnlineTask object (16)',3,'',29,1),(105,'2020-07-08 08:20:41.366699','18','OnlineTask object (18)',1,'[{\"added\": {}}]',29,1),(106,'2020-07-08 10:10:52.883236','19','OnlineTask object (19)',1,'[{\"added\": {}}]',29,1),(107,'2020-07-08 10:29:16.436916','19','OnlineTask object (19)',3,'',29,1),(108,'2020-07-08 10:29:16.652514','18','OnlineTask object (18)',3,'',29,1),(109,'2020-07-08 10:29:43.931225','20','OnlineTask object (20)',1,'[{\"added\": {}}]',29,1),(110,'2020-07-08 10:35:01.033509','20','OnlineTask object (20)',3,'',29,1),(111,'2020-07-08 10:35:09.210993','21','OnlineTask object (21)',1,'[{\"added\": {}}]',29,1),(112,'2020-07-08 10:36:03.227690','21','OnlineTask object (21)',3,'',29,1),(113,'2020-07-08 10:36:26.106283','22','OnlineTask object (22)',1,'[{\"added\": {}}]',29,1),(114,'2020-07-08 10:38:27.649178','22','OnlineTask object (22)',3,'',29,1),(115,'2020-07-08 10:38:54.970898','23','OnlineTask object (23)',1,'[{\"added\": {}}]',29,1),(116,'2020-07-09 09:21:08.105959','21','OfflineTask object (21)',3,'',13,1),(117,'2020-07-09 09:21:08.265198','20','OfflineTask object (20)',3,'',13,1),(118,'2020-07-09 09:21:08.306683','19','OfflineTask object (19)',3,'',13,1),(119,'2020-07-09 09:21:08.353477','18','OfflineTask object (18)',3,'',13,1),(120,'2020-07-09 09:21:08.487245','17','OfflineTask object (17)',3,'',13,1),(121,'2020-07-09 09:21:08.529132','16','OfflineTask object (16)',3,'',13,1),(122,'2020-07-09 09:21:08.565037','15','OfflineTask object (15)',3,'',13,1),(123,'2020-07-09 09:21:08.605928','14','OfflineTask object (14)',3,'',13,1),(124,'2020-07-09 09:21:08.641831','13','OfflineTask object (13)',3,'',13,1),(125,'2020-07-09 09:21:08.683719','12','OfflineTask object (12)',3,'',13,1),(126,'2020-07-09 09:21:14.579011','11','OfflineTask object (11)',3,'',13,1),(127,'2020-07-09 09:21:14.708073','10','OfflineTask object (10)',3,'',13,1),(128,'2020-07-09 09:21:14.750006','9','OfflineTask object (9)',3,'',13,1),(129,'2020-07-09 09:21:40.105924','22','OfflineTask object (22)',1,'[{\"added\": {}}]',13,1),(130,'2020-07-09 09:25:25.603020','22','OfflineTask object (22)',3,'',13,1),(131,'2020-07-09 09:31:13.141327','23','OfflineTask object (23)',1,'[{\"added\": {}}]',13,1),(132,'2020-07-09 09:33:42.117363','24','OfflineTask object (24)',1,'[{\"added\": {}}]',13,1),(133,'2020-07-09 09:33:46.707060','23','OfflineTask object (23)',3,'',13,1),(134,'2020-07-09 09:36:11.801329','25','OfflineTask object (25)',1,'[{\"added\": {}}]',13,1),(135,'2020-07-09 09:36:16.330447','24','OfflineTask object (24)',3,'',13,1),(136,'2020-07-09 09:44:34.858706','25','OfflineTask object (25)',3,'',13,1),(137,'2020-07-09 09:44:47.001647','26','OfflineTask object (26)',1,'[{\"added\": {}}]',13,1),(138,'2020-07-09 09:59:14.025576','27','OfflineTask object (27)',1,'[{\"added\": {}}]',13,1),(139,'2020-07-09 10:41:44.042542','28','OfflineTask object (28)',1,'[{\"added\": {}}]',13,1),(140,'2020-07-09 10:46:58.740060','29','OfflineTask object (29)',1,'[{\"added\": {}}]',13,1),(141,'2020-07-09 10:52:49.720470','30','OfflineTask object (30)',1,'[{\"added\": {}}]',13,1),(142,'2020-07-09 10:55:05.583350','30','OfflineTask object (30)',3,'',13,1),(143,'2020-07-09 10:55:05.717292','29','OfflineTask object (29)',3,'',13,1),(144,'2020-07-09 10:55:05.760451','28','OfflineTask object (28)',3,'',13,1),(145,'2020-07-09 10:55:05.805389','27','OfflineTask object (27)',3,'',13,1),(146,'2020-07-09 10:55:05.849020','26','OfflineTask object (26)',3,'',13,1),(147,'2020-07-09 10:55:17.862485','31','OfflineTask object (31)',1,'[{\"added\": {}}]',13,1),(148,'2020-07-09 11:01:11.285346','32','OfflineTask object (32)',1,'[{\"added\": {}}]',13,1),(149,'2020-07-09 11:09:16.013939','33','OfflineTask object (33)',1,'[{\"added\": {}}]',13,1),(150,'2020-07-09 11:10:47.640776','34','OfflineTask object (34)',1,'[{\"added\": {}}]',13,1),(151,'2020-07-09 11:14:48.669361','35','OfflineTask object (35)',1,'[{\"added\": {}}]',13,1),(152,'2020-07-09 11:15:31.819444','36','OfflineTask object (36)',1,'[{\"added\": {}}]',13,1),(153,'2020-07-09 11:18:28.002832','36','OfflineTask object (36)',3,'',13,1),(154,'2020-07-09 11:18:28.049193','35','OfflineTask object (35)',3,'',13,1),(155,'2020-07-09 11:18:28.093978','34','OfflineTask object (34)',3,'',13,1),(156,'2020-07-09 11:18:28.137817','33','OfflineTask object (33)',3,'',13,1),(157,'2020-07-09 11:18:28.181568','32','OfflineTask object (32)',3,'',13,1),(158,'2020-07-09 11:18:28.247994','31','OfflineTask object (31)',3,'',13,1),(159,'2020-07-09 11:25:49.046633','37','OfflineTask object (37)',1,'[{\"added\": {}}]',13,1),(160,'2020-07-09 11:28:55.809383','38','OfflineTask object (38)',1,'[{\"added\": {}}]',13,1),(161,'2020-07-09 11:29:29.530530','39','OfflineTask object (39)',1,'[{\"added\": {}}]',13,1),(162,'2020-07-09 15:22:58.130604','39','OfflineTask object (39)',3,'',13,1),(163,'2020-07-09 15:22:58.272137','38','OfflineTask object (38)',3,'',13,1),(164,'2020-07-09 15:22:58.315834','37','OfflineTask object (37)',3,'',13,1),(165,'2020-07-09 15:24:29.698042','40','OfflineTask object (40)',1,'[{\"added\": {}}]',13,1),(166,'2020-07-09 15:26:34.020394','41','OfflineTask object (41)',1,'[{\"added\": {}}]',13,1),(167,'2020-07-09 15:29:47.699470','24','OnlineTask object (24)',1,'[{\"added\": {}}]',29,1);
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=30 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(4,'auth','user'),(5,'contenttypes','contenttype'),(14,'djcelery','crontabschedule'),(15,'djcelery','intervalschedule'),(16,'djcelery','periodictask'),(17,'djcelery','periodictasks'),(18,'djcelery','taskmeta'),(19,'djcelery','tasksetmeta'),(20,'djcelery','taskstate'),(21,'djcelery','workerstate'),(7,'offlineTask','offlinemapmanage'),(8,'offlineTask','offlinepreprocessset'),(13,'offlineTask','offlinetask'),(9,'offlineTask','singleimagecompareinfo'),(10,'offlineTask','singleimageidentifyinfo'),(11,'offlineTask','singleimagepreprocessinfo'),(12,'offlineTask','singleimagespliceinfo'),(28,'onlineTask','onlineimageidentifyinfo'),(29,'onlineTask','onlinetask'),(26,'reversion','revision'),(27,'reversion','version'),(6,'sessions','session'),(22,'xadmin','bookmark'),(25,'xadmin','log'),(23,'xadmin','usersettings'),(24,'xadmin','userwidget');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=42 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2020-06-04 15:33:01.817747'),(2,'auth','0001_initial','2020-06-04 15:33:03.132558'),(3,'admin','0001_initial','2020-06-04 15:33:07.760038'),(4,'admin','0002_logentry_remove_auto_add','2020-06-04 15:33:08.833547'),(5,'admin','0003_logentry_add_action_flag_choices','2020-06-04 15:33:08.873444'),(6,'contenttypes','0002_remove_content_type_name','2020-06-04 15:33:09.649261'),(7,'auth','0002_alter_permission_name_max_length','2020-06-04 15:33:10.147826'),(8,'auth','0003_alter_user_email_max_length','2020-06-04 15:33:10.639616'),(9,'auth','0004_alter_user_username_opts','2020-06-04 15:33:10.672753'),(10,'auth','0005_alter_user_last_login_null','2020-06-04 15:33:11.048762'),(11,'auth','0006_require_contenttypes_0002','2020-06-04 15:33:11.073452'),(12,'auth','0007_alter_validators_add_error_messages','2020-06-04 15:33:11.099786'),(13,'auth','0008_alter_user_username_max_length','2020-06-04 15:33:11.589998'),(14,'auth','0009_alter_user_last_name_max_length','2020-06-04 15:33:12.180339'),(15,'auth','0010_alter_group_name_max_length','2020-06-04 15:33:12.699080'),(16,'auth','0011_update_proxy_permissions','2020-06-04 15:33:12.780552'),(17,'djcelery','0001_initial','2020-06-04 15:33:15.301105'),(18,'offlineTask','0001_initial','2020-06-04 15:33:20.497305'),(19,'sessions','0001_initial','2020-06-04 15:33:22.133045'),(20,'reversion','0001_squashed_0004_auto_20160611_1202','2020-06-18 10:33:34.123694'),(21,'xadmin','0001_initial','2020-06-18 10:33:37.372883'),(22,'xadmin','0002_log','2020-06-18 10:33:40.397703'),(23,'xadmin','0003_auto_20160715_0100','2020-06-18 10:33:42.384141'),(29,'onlineTask','0001_initial','2020-07-07 09:42:55.873446'),(30,'onlineTask','0002_auto_20200706_1020','2020-07-07 09:42:56.589604'),(31,'onlineTask','0003_onlinetask_identify_status','2020-07-07 09:42:57.244011'),(32,'onlineTask','0004_onlinetask_preprocessset','2020-07-07 09:42:57.755022'),(33,'onlineTask','0005_auto_20200707_0941','2020-07-07 09:42:59.390022'),(34,'onlineTask','0006_auto_20200707_0942','2020-07-07 09:43:00.155754'),(35,'onlineTask','0007_auto_20200707_0950','2020-07-07 09:50:16.823766'),(36,'onlineTask','0008_onlineimageidentifyinfo_imageoriginpath','2020-07-07 09:53:11.612217'),(37,'onlineTask','0009_auto_20200707_1023','2020-07-07 10:24:01.887494'),(38,'onlineTask','0010_auto_20200707_1027','2020-07-07 10:27:08.537077'),(39,'onlineTask','0011_onlinetask_preprocess_status','2020-07-07 10:54:32.389482'),(40,'onlineTask','0012_auto_20200707_1126','2020-07-07 11:26:21.702377'),(41,'onlineTask','0013_auto_20200708_1113','2020-07-08 11:14:07.882806');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('1yt66fto6w265l69x8nepeyw7dsuq503','ZmRkMmI4YTI1ZGYwMDlhYmM1MzhlZGI2MzA0M2ZjYzIzMGY2NmEwZTp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJkMTY3NTk5NzU2ZGNmNTVhMjM5Y2Y5N2I0YTNjMGQwODQ5NDhlNTVkIn0=','2020-07-13 15:35:24.681375'),('4k0mrfhay25wyivts4d3p5m4xmeanzwm','ZmRkMmI4YTI1ZGYwMDlhYmM1MzhlZGI2MzA0M2ZjYzIzMGY2NmEwZTp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJkMTY3NTk5NzU2ZGNmNTVhMjM5Y2Y5N2I0YTNjMGQwODQ5NDhlNTVkIn0=','2020-06-30 10:57:22.982001'),('8vwx64n0ni88730e20xge6ohcfg1ipxy','ZmRkMmI4YTI1ZGYwMDlhYmM1MzhlZGI2MzA0M2ZjYzIzMGY2NmEwZTp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJkMTY3NTk5NzU2ZGNmNTVhMjM5Y2Y5N2I0YTNjMGQwODQ5NDhlNTVkIn0=','2020-06-30 11:30:07.900406'),('cim1gxf38o6lsxlaew11vl2faxqfugs7','NjJkOTEwZGM3NTRkZGE0NmZlY2FmY2QxNTEyN2U3NDdmNzExNTBkMDp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJkMTY3NTk5NzU2ZGNmNTVhMjM5Y2Y5N2I0YTNjMGQwODQ5NDhlNTVkIiwiTElTVF9RVUVSWSI6W1sib2ZmbGluZVRhc2siLCJvZmZsaW5ldGFzayJdLCIiXX0=','2020-07-02 11:17:10.700685'),('nvxsftmk461c6dwu37xg3xhdv8f0ixx0','ZmRkMmI4YTI1ZGYwMDlhYmM1MzhlZGI2MzA0M2ZjYzIzMGY2NmEwZTp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJkMTY3NTk5NzU2ZGNmNTVhMjM5Y2Y5N2I0YTNjMGQwODQ5NDhlNTVkIn0=','2020-06-18 15:43:23.494764'),('p15taqshbmhmu3a6rbpqva67pk0ox4u1','ZmRkMmI4YTI1ZGYwMDlhYmM1MzhlZGI2MzA0M2ZjYzIzMGY2NmEwZTp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJkMTY3NTk5NzU2ZGNmNTVhMjM5Y2Y5N2I0YTNjMGQwODQ5NDhlNTVkIn0=','2020-06-30 16:57:08.470188'),('u8ed75j1q23a3pizcmfahpp77fbck0ca','ZmRkMmI4YTI1ZGYwMDlhYmM1MzhlZGI2MzA0M2ZjYzIzMGY2NmEwZTp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJkMTY3NTk5NzU2ZGNmNTVhMjM5Y2Y5N2I0YTNjMGQwODQ5NDhlNTVkIn0=','2020-06-30 10:51:35.213903'),('wsa51cocnbg4f08yvxpioo2vfijhlc06','ZmRkMmI4YTI1ZGYwMDlhYmM1MzhlZGI2MzA0M2ZjYzIzMGY2NmEwZTp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJkMTY3NTk5NzU2ZGNmNTVhMjM5Y2Y5N2I0YTNjMGQwODQ5NDhlNTVkIn0=','2020-06-30 16:57:08.373452');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `djcelery_crontabschedule`
--

DROP TABLE IF EXISTS `djcelery_crontabschedule`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `djcelery_crontabschedule` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `minute` varchar(64) NOT NULL,
  `hour` varchar(64) NOT NULL,
  `day_of_week` varchar(64) NOT NULL,
  `day_of_month` varchar(64) NOT NULL,
  `month_of_year` varchar(64) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `djcelery_crontabschedule`
--

LOCK TABLES `djcelery_crontabschedule` WRITE;
/*!40000 ALTER TABLE `djcelery_crontabschedule` DISABLE KEYS */;
/*!40000 ALTER TABLE `djcelery_crontabschedule` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `djcelery_intervalschedule`
--

DROP TABLE IF EXISTS `djcelery_intervalschedule`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `djcelery_intervalschedule` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `every` int(11) NOT NULL,
  `period` varchar(24) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `djcelery_intervalschedule`
--

LOCK TABLES `djcelery_intervalschedule` WRITE;
/*!40000 ALTER TABLE `djcelery_intervalschedule` DISABLE KEYS */;
/*!40000 ALTER TABLE `djcelery_intervalschedule` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `djcelery_periodictask`
--

DROP TABLE IF EXISTS `djcelery_periodictask`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `djcelery_periodictask` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(200) NOT NULL,
  `task` varchar(200) NOT NULL,
  `args` longtext NOT NULL,
  `kwargs` longtext NOT NULL,
  `queue` varchar(200) DEFAULT NULL,
  `exchange` varchar(200) DEFAULT NULL,
  `routing_key` varchar(200) DEFAULT NULL,
  `expires` datetime(6) DEFAULT NULL,
  `enabled` tinyint(1) NOT NULL,
  `last_run_at` datetime(6) DEFAULT NULL,
  `total_run_count` int(10) unsigned NOT NULL,
  `date_changed` datetime(6) NOT NULL,
  `description` longtext NOT NULL,
  `crontab_id` int(11) DEFAULT NULL,
  `interval_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `djcelery_periodictas_crontab_id_75609bab_fk_djcelery_` (`crontab_id`),
  KEY `djcelery_periodictas_interval_id_b426ab02_fk_djcelery_` (`interval_id`),
  CONSTRAINT `djcelery_periodictas_crontab_id_75609bab_fk_djcelery_` FOREIGN KEY (`crontab_id`) REFERENCES `djcelery_crontabschedule` (`id`),
  CONSTRAINT `djcelery_periodictas_interval_id_b426ab02_fk_djcelery_` FOREIGN KEY (`interval_id`) REFERENCES `djcelery_intervalschedule` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `djcelery_periodictask`
--

LOCK TABLES `djcelery_periodictask` WRITE;
/*!40000 ALTER TABLE `djcelery_periodictask` DISABLE KEYS */;
/*!40000 ALTER TABLE `djcelery_periodictask` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `djcelery_periodictasks`
--

DROP TABLE IF EXISTS `djcelery_periodictasks`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `djcelery_periodictasks` (
  `ident` smallint(6) NOT NULL,
  `last_update` datetime(6) NOT NULL,
  PRIMARY KEY (`ident`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `djcelery_periodictasks`
--

LOCK TABLES `djcelery_periodictasks` WRITE;
/*!40000 ALTER TABLE `djcelery_periodictasks` DISABLE KEYS */;
/*!40000 ALTER TABLE `djcelery_periodictasks` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `djcelery_taskstate`
--

DROP TABLE IF EXISTS `djcelery_taskstate`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `djcelery_taskstate` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `state` varchar(64) NOT NULL,
  `task_id` varchar(36) NOT NULL,
  `name` varchar(200) DEFAULT NULL,
  `tstamp` datetime(6) NOT NULL,
  `args` longtext,
  `kwargs` longtext,
  `eta` datetime(6) DEFAULT NULL,
  `expires` datetime(6) DEFAULT NULL,
  `result` longtext,
  `traceback` longtext,
  `runtime` double DEFAULT NULL,
  `retries` int(11) NOT NULL,
  `hidden` tinyint(1) NOT NULL,
  `worker_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `task_id` (`task_id`),
  KEY `djcelery_taskstate_state_53543be4` (`state`),
  KEY `djcelery_taskstate_name_8af9eded` (`name`),
  KEY `djcelery_taskstate_tstamp_4c3f93a1` (`tstamp`),
  KEY `djcelery_taskstate_hidden_c3905e57` (`hidden`),
  KEY `djcelery_taskstate_worker_id_f7f57a05_fk_djcelery_workerstate_id` (`worker_id`),
  CONSTRAINT `djcelery_taskstate_worker_id_f7f57a05_fk_djcelery_workerstate_id` FOREIGN KEY (`worker_id`) REFERENCES `djcelery_workerstate` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `djcelery_taskstate`
--

LOCK TABLES `djcelery_taskstate` WRITE;
/*!40000 ALTER TABLE `djcelery_taskstate` DISABLE KEYS */;
/*!40000 ALTER TABLE `djcelery_taskstate` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `djcelery_workerstate`
--

DROP TABLE IF EXISTS `djcelery_workerstate`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `djcelery_workerstate` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `hostname` varchar(255) NOT NULL,
  `last_heartbeat` datetime(6) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `hostname` (`hostname`),
  KEY `djcelery_workerstate_last_heartbeat_4539b544` (`last_heartbeat`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `djcelery_workerstate`
--

LOCK TABLES `djcelery_workerstate` WRITE;
/*!40000 ALTER TABLE `djcelery_workerstate` DISABLE KEYS */;
/*!40000 ALTER TABLE `djcelery_workerstate` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `offlinetask_offlinemapmanage`
--

DROP TABLE IF EXISTS `offlinetask_offlinemapmanage`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `offlinetask_offlinemapmanage` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `addTime` datetime(6) DEFAULT NULL,
  `mapNickName` varchar(100) NOT NULL,
  `mapDescription` longtext,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `offlinetask_offlinemapmanage`
--

LOCK TABLES `offlinetask_offlinemapmanage` WRITE;
/*!40000 ALTER TABLE `offlinetask_offlinemapmanage` DISABLE KEYS */;
INSERT INTO `offlinetask_offlinemapmanage` VALUES (1,'2020-06-04 16:23:01.962944','测试','1111'),(2,'2020-06-05 08:57:34.937066','操场',''),(3,'2020-06-16 11:22:11.794754','新电脑','');
/*!40000 ALTER TABLE `offlinetask_offlinemapmanage` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `offlinetask_offlinepreprocessset`
--

DROP TABLE IF EXISTS `offlinetask_offlinepreprocessset`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `offlinetask_offlinepreprocessset` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `addTime` datetime(6) NOT NULL,
  `setNickName` varchar(100) NOT NULL,
  `is_brightness` tinyint(1) NOT NULL,
  `is_dehaze` tinyint(1) NOT NULL,
  `is_gamma` tinyint(1) NOT NULL,
  `is_clahe` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `offlinetask_offlinepreprocessset`
--

LOCK TABLES `offlinetask_offlinepreprocessset` WRITE;
/*!40000 ALTER TABLE `offlinetask_offlinepreprocessset` DISABLE KEYS */;
INSERT INTO `offlinetask_offlinepreprocessset` VALUES (1,'2020-06-04 16:23:26.781673','壹号文件',1,0,1,1),(2,'2020-06-16 11:23:10.407834','贰号文件',1,1,1,1);
/*!40000 ALTER TABLE `offlinetask_offlinepreprocessset` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `offlinetask_offlinetask`
--

DROP TABLE IF EXISTS `offlinetask_offlinetask`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `offlinetask_offlinetask` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `begin` datetime(6) DEFAULT NULL,
  `end` date DEFAULT NULL,
  `creator` varchar(20) DEFAULT NULL,
  `modifier` varchar(20) DEFAULT NULL,
  `creation` datetime(6) DEFAULT NULL,
  `modification` datetime(6) DEFAULT NULL,
  `description` longtext,
  `identify_status` varchar(6) DEFAULT NULL,
  `splice_status` varchar(6) DEFAULT NULL,
  `preprocess_status` varchar(6) DEFAULT NULL,
  `comparison_status` varchar(6) DEFAULT NULL,
  `folderOriginPath` varchar(100) NOT NULL,
  `overDate` varchar(45) NOT NULL,
  `isIdentify` tinyint(1) NOT NULL,
  `isIdentifyPre` tinyint(1) NOT NULL,
  `isSplice` tinyint(1) NOT NULL,
  `isSplicePre` tinyint(1) NOT NULL,
  `isCompare` tinyint(1) NOT NULL,
  `isComparePre` tinyint(1) NOT NULL,
  `comparePath_id` int(11) DEFAULT NULL,
  `preprocessSet_id` int(11) DEFAULT NULL,
  `title_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `offlineTask_offlinet_title_id_af2a5e9e_fk_offlineTa` (`title_id`),
  KEY `offlineTask_offlinet_comparePath_id_e2285530_fk_offlineTa` (`comparePath_id`),
  KEY `offlineTask_offlinet_preprocessSet_id_09553ca2_fk_offlineTa` (`preprocessSet_id`),
  CONSTRAINT `offlineTask_offlinet_comparePath_id_e2285530_fk_offlineTa` FOREIGN KEY (`comparePath_id`) REFERENCES `offlinetask_singleimagespliceinfo` (`id`),
  CONSTRAINT `offlineTask_offlinet_preprocessSet_id_09553ca2_fk_offlineTa` FOREIGN KEY (`preprocessSet_id`) REFERENCES `offlinetask_offlinepreprocessset` (`id`),
  CONSTRAINT `offlineTask_offlinet_title_id_af2a5e9e_fk_offlineTa` FOREIGN KEY (`title_id`) REFERENCES `offlinetask_offlinemapmanage` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=42 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `offlinetask_offlinetask`
--

LOCK TABLES `offlinetask_offlinetask` WRITE;
/*!40000 ALTER TABLE `offlinetask_offlinetask` DISABLE KEYS */;
INSERT INTO `offlinetask_offlinetask` VALUES (40,'2020-07-09 15:24:29.683043','9999-12-31','admin',NULL,'2020-07-09 15:24:29.697006','2020-07-09 15:25:20.391856','','d','d','d','u','操场/20200709/152429/origin/','20200709/152429',1,1,1,1,0,0,NULL,1,2),(41,'2020-07-09 15:26:34.006433','9999-12-31','admin',NULL,'2020-07-09 15:26:34.019398','2020-07-09 15:28:09.265854','','d','d','d','d','操场/20200709/152634/origin/','20200709/152634',1,1,1,1,1,1,34,1,2);
/*!40000 ALTER TABLE `offlinetask_offlinetask` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `offlinetask_singleimagecompareinfo`
--

DROP TABLE IF EXISTS `offlinetask_singleimagecompareinfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `offlinetask_singleimagecompareinfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `titleId` int(11) NOT NULL,
  `is_compare` tinyint(1) NOT NULL,
  `is_show` tinyint(1) NOT NULL,
  `progress` double NOT NULL,
  `imagePreprocessPath` varchar(1000) NOT NULL,
  `imageComOriginPartPath` varchar(1000) NOT NULL,
  `imageComOriginPanoPath` varchar(1000) NOT NULL,
  `imageComOriginResultPath` varchar(1000) NOT NULL,
  `overDate` varchar(45) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=48 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `offlinetask_singleimagecompareinfo`
--

LOCK TABLES `offlinetask_singleimagecompareinfo` WRITE;
/*!40000 ALTER TABLE `offlinetask_singleimagecompareinfo` DISABLE KEYS */;
INSERT INTO `offlinetask_singleimagecompareinfo` VALUES (42,2,1,1,0.166666666666667,'','D:/202006115wjk/topic/UAV/static/upload/操场/20200709/152634/compare/DJI_0013-OrigRegion.JPG','D:/202006115wjk/topic/UAV/static/upload/操场/20200709/152634/compare/DJI_0013-Position.JPG','D:/202006115wjk/topic/UAV/static/upload/操场/20200709/152634/compare/DJI_0013-CompRegion.JPG','20200709/152634'),(43,2,1,1,0.333333333333333,'','D:/202006115wjk/topic/UAV/static/upload/操场/20200709/152634/compare/DJI_0014-OrigRegion.JPG','D:/202006115wjk/topic/UAV/static/upload/操场/20200709/152634/compare/DJI_0014-Position.JPG','D:/202006115wjk/topic/UAV/static/upload/操场/20200709/152634/compare/DJI_0014-CompRegion.JPG','20200709/152634'),(44,2,1,1,0.5,'','D:/202006115wjk/topic/UAV/static/upload/操场/20200709/152634/compare/DJI_0015-OrigRegion.JPG','D:/202006115wjk/topic/UAV/static/upload/操场/20200709/152634/compare/DJI_0015-Position.JPG','D:/202006115wjk/topic/UAV/static/upload/操场/20200709/152634/compare/DJI_0015-CompRegion.JPG','20200709/152634'),(45,2,1,1,0.666666666666667,'','D:/202006115wjk/topic/UAV/static/upload/操场/20200709/152634/compare/DJI_0016-OrigRegion.JPG','D:/202006115wjk/topic/UAV/static/upload/操场/20200709/152634/compare/DJI_0016-Position.JPG','D:/202006115wjk/topic/UAV/static/upload/操场/20200709/152634/compare/DJI_0016-CompRegion.JPG','20200709/152634'),(46,2,1,1,0.833333333333333,'','D:/202006115wjk/topic/UAV/static/upload/操场/20200709/152634/compare/DJI_0017-OrigRegion.JPG','D:/202006115wjk/topic/UAV/static/upload/操场/20200709/152634/compare/DJI_0017-Position.JPG','D:/202006115wjk/topic/UAV/static/upload/操场/20200709/152634/compare/DJI_0017-CompRegion.JPG','20200709/152634'),(47,2,1,1,1,'','D:/202006115wjk/topic/UAV/static/upload/操场/20200709/152634/compare/DJI_0018-OrigRegion.JPG','D:/202006115wjk/topic/UAV/static/upload/操场/20200709/152634/compare/DJI_0018-Position.JPG','D:/202006115wjk/topic/UAV/static/upload/操场/20200709/152634/compare/DJI_0018-CompRegion.JPG','20200709/152634');
/*!40000 ALTER TABLE `offlinetask_singleimagecompareinfo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `offlinetask_singleimageidentifyinfo`
--

DROP TABLE IF EXISTS `offlinetask_singleimageidentifyinfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `offlinetask_singleimageidentifyinfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `titleId` int(11) NOT NULL,
  `is_confirm` tinyint(1) DEFAULT NULL,
  `is_identify` tinyint(1) NOT NULL,
  `is_show` tinyint(1) NOT NULL,
  `progress` double NOT NULL,
  `imagePreprocessPath` varchar(1000) NOT NULL,
  `imageIdentifyPath` varchar(1000) NOT NULL,
  `imageIdentifyResultPath` varchar(1000) NOT NULL,
  `overDate` varchar(45) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `offlinetask_singleimageidentifyinfo`
--

LOCK TABLES `offlinetask_singleimageidentifyinfo` WRITE;
/*!40000 ALTER TABLE `offlinetask_singleimageidentifyinfo` DISABLE KEYS */;
INSERT INTO `offlinetask_singleimageidentifyinfo` VALUES (9,2,1,0,1,0.166666666666667,'','D:/202006115wjk/topic/UAV/static/upload/操场/20200709/152429/identify/DJI_0013.JPG','D:/202006115wjk/topic/UAV/static/upload/操场/20200709/152429/identifyResult/DJI_0013.JPG','20200709/152429'),(10,2,1,0,1,0.333333333333333,'','D:/202006115wjk/topic/UAV/static/upload/操场/20200709/152429/identify/DJI_0014.JPG','D:/202006115wjk/topic/UAV/static/upload/操场/20200709/152429/identifyResult/DJI_0014.JPG','20200709/152429'),(11,2,0,0,1,0.5,'','D:/202006115wjk/topic/UAV/static/upload/操场/20200709/152429/identify/DJI_0015.JPG','','20200709/152429'),(12,2,1,0,1,0.666666666666667,'','D:/202006115wjk/topic/UAV/static/upload/操场/20200709/152429/identify/DJI_0016.JPG','D:/202006115wjk/topic/UAV/static/upload/操场/20200709/152429/identifyResult/DJI_0016.JPG','20200709/152429'),(13,2,1,0,1,0.833333333333333,'','D:/202006115wjk/topic/UAV/static/upload/操场/20200709/152429/identify/DJI_0017.JPG','D:/202006115wjk/topic/UAV/static/upload/操场/20200709/152429/identifyResult/DJI_0017.JPG','20200709/152429'),(14,2,0,0,1,1,'','D:/202006115wjk/topic/UAV/static/upload/操场/20200709/152429/identify/DJI_0018.JPG','','20200709/152429'),(15,2,1,0,1,0.166666666666667,'','D:/202006115wjk/topic/UAV/static/upload/操场/20200709/152634/identify/DJI_0013.JPG','D:/202006115wjk/topic/UAV/static/upload/操场/20200709/152634/identifyResult/DJI_0013.JPG','20200709/152634'),(16,2,1,0,1,0.333333333333333,'','D:/202006115wjk/topic/UAV/static/upload/操场/20200709/152634/identify/DJI_0014.JPG','D:/202006115wjk/topic/UAV/static/upload/操场/20200709/152634/identifyResult/DJI_0014.JPG','20200709/152634'),(17,2,0,0,1,0.5,'','D:/202006115wjk/topic/UAV/static/upload/操场/20200709/152634/identify/DJI_0015.JPG','','20200709/152634'),(18,2,1,0,1,0.666666666666667,'','D:/202006115wjk/topic/UAV/static/upload/操场/20200709/152634/identify/DJI_0016.JPG','D:/202006115wjk/topic/UAV/static/upload/操场/20200709/152634/identifyResult/DJI_0016.JPG','20200709/152634'),(19,2,1,0,1,0.833333333333333,'','D:/202006115wjk/topic/UAV/static/upload/操场/20200709/152634/identify/DJI_0017.JPG','D:/202006115wjk/topic/UAV/static/upload/操场/20200709/152634/identifyResult/DJI_0017.JPG','20200709/152634'),(20,2,1,0,1,1,'','D:/202006115wjk/topic/UAV/static/upload/操场/20200709/152634/identify/DJI_0018.JPG','D:/202006115wjk/topic/UAV/static/upload/操场/20200709/152634/identifyResult/DJI_0018.JPG','20200709/152634');
/*!40000 ALTER TABLE `offlinetask_singleimageidentifyinfo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `offlinetask_singleimagepreprocessinfo`
--

DROP TABLE IF EXISTS `offlinetask_singleimagepreprocessinfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `offlinetask_singleimagepreprocessinfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `titleId` int(11) NOT NULL,
  `is_preprocess` tinyint(1) NOT NULL,
  `is_show` tinyint(1) NOT NULL,
  `imageOriginPath` varchar(10000) NOT NULL,
  `imagePreprocessPath` varchar(10000) NOT NULL,
  `overDate` varchar(45) NOT NULL,
  `progress` double NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=132 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `offlinetask_singleimagepreprocessinfo`
--

LOCK TABLES `offlinetask_singleimagepreprocessinfo` WRITE;
/*!40000 ALTER TABLE `offlinetask_singleimagepreprocessinfo` DISABLE KEYS */;
INSERT INTO `offlinetask_singleimagepreprocessinfo` VALUES (120,2,1,1,'D:/202006115wjk/topic/UAV/static/upload/操场/20200709/152429/origin/DJI_0013.JPG','D:/202006115wjk/topic/UAV/static/upload/操场/20200709/152429/preprocess/DJI_0013.JPG','20200709/152429',0.166666666666667),(121,2,1,1,'D:/202006115wjk/topic/UAV/static/upload/操场/20200709/152429/origin/DJI_0014.JPG','D:/202006115wjk/topic/UAV/static/upload/操场/20200709/152429/preprocess/DJI_0014.JPG','20200709/152429',0.333333333333333),(122,2,1,1,'D:/202006115wjk/topic/UAV/static/upload/操场/20200709/152429/origin/DJI_0015.JPG','D:/202006115wjk/topic/UAV/static/upload/操场/20200709/152429/preprocess/DJI_0015.JPG','20200709/152429',0.5),(123,2,1,1,'D:/202006115wjk/topic/UAV/static/upload/操场/20200709/152429/origin/DJI_0016.JPG','D:/202006115wjk/topic/UAV/static/upload/操场/20200709/152429/preprocess/DJI_0016.JPG','20200709/152429',0.666666666666667),(124,2,1,1,'D:/202006115wjk/topic/UAV/static/upload/操场/20200709/152429/origin/DJI_0017.JPG','D:/202006115wjk/topic/UAV/static/upload/操场/20200709/152429/preprocess/DJI_0017.JPG','20200709/152429',0.833333333333333),(125,2,1,1,'D:/202006115wjk/topic/UAV/static/upload/操场/20200709/152429/origin/DJI_0018.JPG','D:/202006115wjk/topic/UAV/static/upload/操场/20200709/152429/preprocess/DJI_0018.JPG','20200709/152429',1),(126,2,1,1,'D:/202006115wjk/topic/UAV/static/upload/操场/20200709/152634/origin/DJI_0013.JPG','D:/202006115wjk/topic/UAV/static/upload/操场/20200709/152634/preprocess/DJI_0013.JPG','20200709/152634',0.166666666666667),(127,2,1,1,'D:/202006115wjk/topic/UAV/static/upload/操场/20200709/152634/origin/DJI_0014.JPG','D:/202006115wjk/topic/UAV/static/upload/操场/20200709/152634/preprocess/DJI_0014.JPG','20200709/152634',0.333333333333333),(128,2,1,1,'D:/202006115wjk/topic/UAV/static/upload/操场/20200709/152634/origin/DJI_0015.JPG','D:/202006115wjk/topic/UAV/static/upload/操场/20200709/152634/preprocess/DJI_0015.JPG','20200709/152634',0.5),(129,2,1,1,'D:/202006115wjk/topic/UAV/static/upload/操场/20200709/152634/origin/DJI_0016.JPG','D:/202006115wjk/topic/UAV/static/upload/操场/20200709/152634/preprocess/DJI_0016.JPG','20200709/152634',0.666666666666667),(130,2,1,1,'D:/202006115wjk/topic/UAV/static/upload/操场/20200709/152634/origin/DJI_0017.JPG','D:/202006115wjk/topic/UAV/static/upload/操场/20200709/152634/preprocess/DJI_0017.JPG','20200709/152634',0.833333333333333),(131,2,1,0,'D:/202006115wjk/topic/UAV/static/upload/操场/20200709/152634/origin/DJI_0018.JPG','D:/202006115wjk/topic/UAV/static/upload/操场/20200709/152634/preprocess/DJI_0018.JPG','20200709/152634',1);
/*!40000 ALTER TABLE `offlinetask_singleimagepreprocessinfo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `offlinetask_singleimagespliceinfo`
--

DROP TABLE IF EXISTS `offlinetask_singleimagespliceinfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `offlinetask_singleimagespliceinfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `titleId` int(11) NOT NULL,
  `is_splice` tinyint(1) NOT NULL,
  `is_show` tinyint(1) NOT NULL,
  `progress` double NOT NULL,
  `imagePreprocessPath` varchar(1000) NOT NULL,
  `imageSplicePath` varchar(1000) NOT NULL,
  `gpsCsvPath` varchar(1000) NOT NULL,
  `overDate` varchar(45) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=36 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `offlinetask_singleimagespliceinfo`
--

LOCK TABLES `offlinetask_singleimagespliceinfo` WRITE;
/*!40000 ALTER TABLE `offlinetask_singleimagespliceinfo` DISABLE KEYS */;
INSERT INTO `offlinetask_singleimagespliceinfo` VALUES (34,2,1,1,1,'','D:/202006115wjk/topic/UAV/static/upload/操场/20200709/152429/splice/thumbnail.JPG','D:/202006115wjk/topic/UAV/static/upload/操场/20200709/152429/splice/gps_points.csv','20200709/152429'),(35,2,1,1,1,'','D:/202006115wjk/topic/UAV/static/upload/操场/20200709/152634/splice/thumbnail.JPG','D:/202006115wjk/topic/UAV/static/upload/操场/20200709/152634/splice/gps_points.csv','20200709/152634');
/*!40000 ALTER TABLE `offlinetask_singleimagespliceinfo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `onlinetask_onlineimageidentifyinfo`
--

DROP TABLE IF EXISTS `onlinetask_onlineimageidentifyinfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `onlinetask_onlineimageidentifyinfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `is_confirm` tinyint(1) DEFAULT NULL,
  `is_selected` tinyint(1) NOT NULL,
  `is_show` tinyint(1) NOT NULL,
  `progress` tinyint(1) NOT NULL,
  `imagePreprocessPath` varchar(1000) NOT NULL,
  `imageIdentifyPath` varchar(1000) NOT NULL,
  `imageIdentifyResultPath` varchar(1000) NOT NULL,
  `overDate` varchar(45) NOT NULL,
  `title` varchar(1000) NOT NULL,
  `imageOriginPath` varchar(1000) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=140 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `onlinetask_onlineimageidentifyinfo`
--

LOCK TABLES `onlinetask_onlineimageidentifyinfo` WRITE;
/*!40000 ALTER TABLE `onlinetask_onlineimageidentifyinfo` DISABLE KEYS */;
INSERT INTO `onlinetask_onlineimageidentifyinfo` VALUES (135,0,0,1,1,'D:/202006115wjk/topic/UAV/static/upload/onlineTask/操场/20200709/152947/preprocess/DJI_0063.JPG','D:/202006115wjk/topic/UAV/static/upload/onlineTask/操场/20200709/152947/identify/DJI_0063.JPG','','20200709/152947','操场','D:/202006115wjk/topic/UAV/static/upload/onlineTask/操场/20200709/152947/origin/DJI_0063.JPG'),(136,0,0,1,1,'D:/202006115wjk/topic/UAV/static/upload/onlineTask/操场/20200709/152947/preprocess/DJI_0062.JPG','D:/202006115wjk/topic/UAV/static/upload/onlineTask/操场/20200709/152947/identify/DJI_0062.JPG','','20200709/152947','操场','D:/202006115wjk/topic/UAV/static/upload/onlineTask/操场/20200709/152947/origin/DJI_0062.JPG'),(137,1,0,1,1,'D:/202006115wjk/topic/UAV/static/upload/onlineTask/操场/20200709/152947/preprocess/DJI_0061.JPG','D:/202006115wjk/topic/UAV/static/upload/onlineTask/操场/20200709/152947/identify/DJI_0061.JPG','D:/202006115wjk/topic/UAV/static/upload/onlineTask/操场/20200709/152947/identifyResult/DJI_0061.JPG','20200709/152947','操场','D:/202006115wjk/topic/UAV/static/upload/onlineTask/操场/20200709/152947/origin/DJI_0061.JPG'),(138,0,0,1,1,'D:/202006115wjk/topic/UAV/static/upload/onlineTask/操场/20200709/152947/preprocess/DJI_0060.JPG','D:/202006115wjk/topic/UAV/static/upload/onlineTask/操场/20200709/152947/identify/DJI_0060.JPG','','20200709/152947','操场','D:/202006115wjk/topic/UAV/static/upload/onlineTask/操场/20200709/152947/origin/DJI_0060.JPG'),(139,1,0,1,1,'D:/202006115wjk/topic/UAV/static/upload/onlineTask/操场/20200709/152947/preprocess/DJI_0059.JPG','D:/202006115wjk/topic/UAV/static/upload/onlineTask/操场/20200709/152947/identify/DJI_0059.JPG','D:/202006115wjk/topic/UAV/static/upload/onlineTask/操场/20200709/152947/identifyResult/DJI_0059.JPG','20200709/152947','操场','D:/202006115wjk/topic/UAV/static/upload/onlineTask/操场/20200709/152947/origin/DJI_0059.JPG');
/*!40000 ALTER TABLE `onlinetask_onlineimageidentifyinfo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `onlinetask_onlinetask`
--

DROP TABLE IF EXISTS `onlinetask_onlinetask`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `onlinetask_onlinetask` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `begin` datetime(6) DEFAULT NULL,
  `end` date DEFAULT NULL,
  `creator` varchar(20) DEFAULT NULL,
  `modifier` varchar(20) DEFAULT NULL,
  `creation` datetime(6) DEFAULT NULL,
  `modification` datetime(6) DEFAULT NULL,
  `title_id` int(11) NOT NULL,
  `description` longtext,
  `overDate` varchar(45) NOT NULL,
  `isIdentifyPre` tinyint(1) NOT NULL,
  `identify_status` varchar(6),
  `preprocessSet_id` int(11) DEFAULT NULL,
  `preprocess_status` varchar(6),
  PRIMARY KEY (`id`),
  KEY `onlineTask_onlinetas_preprocessSet_id_7068b18d_fk_offlineTa` (`preprocessSet_id`),
  KEY `onlineTask_onlinetask_title_id_eca9f708` (`title_id`),
  CONSTRAINT `onlineTask_onlinetas_preprocessSet_id_7068b18d_fk_offlineTa` FOREIGN KEY (`preprocessSet_id`) REFERENCES `offlinetask_offlinepreprocessset` (`id`),
  CONSTRAINT `onlineTask_onlinetas_title_id_eca9f708_fk_offlineTa` FOREIGN KEY (`title_id`) REFERENCES `offlinetask_offlinemapmanage` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `onlinetask_onlinetask`
--

LOCK TABLES `onlinetask_onlinetask` WRITE;
/*!40000 ALTER TABLE `onlinetask_onlinetask` DISABLE KEYS */;
INSERT INTO `onlinetask_onlinetask` VALUES (23,'2020-07-08 10:38:54.969900','9999-12-31','admin',NULL,'2020-07-08 10:38:54.969900','2020-07-08 10:38:54.969900',2,'','20200708/103854',1,'u',1,'p'),(24,'2020-07-09 15:29:47.698504','9999-12-31','admin',NULL,'2020-07-09 15:29:47.698504','2020-07-09 15:29:47.698504',2,'','20200709/152947',1,'p',1,'p');
/*!40000 ALTER TABLE `onlinetask_onlinetask` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-07-09 15:46:54
