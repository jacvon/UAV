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
) ENGINE=InnoDB AUTO_INCREMENT=78 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (1,'2020-06-04 16:23:01.963913','1','测试',1,'[{\"added\": {}}]',7,1),(2,'2020-06-04 16:23:26.782671','1','壹号文件',1,'[{\"added\": {}}]',8,1),(3,'2020-06-04 16:37:40.047992','1','OfflineTask object (1)',1,'[{\"added\": {}}]',13,1),(4,'2020-06-05 08:25:00.332572','2','OfflineTask object (2)',1,'[{\"added\": {}}]',13,1),(5,'2020-06-05 08:28:41.232381','3','OfflineTask object (3)',1,'[{\"added\": {}}]',13,1),(6,'2020-06-05 08:29:28.371915','3','OfflineTask object (3)',3,'',13,1),(7,'2020-06-05 08:29:28.393857','2','OfflineTask object (2)',3,'',13,1),(8,'2020-06-05 08:29:28.452701','1','OfflineTask object (1)',3,'',13,1),(9,'2020-06-05 08:29:43.580560','4','OfflineTask object (4)',1,'[{\"added\": {}}]',13,1),(10,'2020-06-05 08:37:14.192879','5','OfflineTask object (5)',1,'[{\"added\": {}}]',13,1),(11,'2020-06-05 08:38:07.832458','6','OfflineTask object (6)',1,'[{\"added\": {}}]',13,1),(12,'2020-06-05 08:42:11.605118','7','OfflineTask object (7)',1,'[{\"added\": {}}]',13,1),(13,'2020-06-05 08:43:58.505318','8','OfflineTask object (8)',1,'[{\"added\": {}}]',13,1),(14,'2020-06-05 08:45:23.552974','8','OfflineTask object (8)',3,'',13,1),(15,'2020-06-05 08:45:23.586648','7','OfflineTask object (7)',3,'',13,1),(16,'2020-06-05 08:45:23.602637','6','OfflineTask object (6)',3,'',13,1),(17,'2020-06-05 08:45:23.661599','5','OfflineTask object (5)',3,'',13,1),(18,'2020-06-05 08:45:23.677863','4','OfflineTask object (4)',3,'',13,1),(19,'2020-06-05 08:45:38.594377','9','OfflineTask object (9)',1,'[{\"added\": {}}]',13,1),(20,'2020-06-05 08:57:34.937066','2','操场',1,'[{\"added\": {}}]',7,1),(21,'2020-06-05 08:57:47.722752','10','OfflineTask object (10)',1,'[{\"added\": {}}]',13,1),(22,'2020-06-05 08:59:59.337095','11','OfflineTask object (11)',1,'[{\"added\": {}}]',13,1),(23,'2020-06-05 09:03:01.471291','12','OfflineTask object (12)',1,'[{\"added\": {}}]',13,1),(24,'2020-06-05 09:06:27.036988','13','OfflineTask object (13)',1,'[{\"added\": {}}]',13,1),(25,'2020-06-05 09:19:46.085243','14','OfflineTask object (14)',1,'[{\"added\": {}}]',13,1),(26,'2020-06-05 09:25:35.781064','15','OfflineTask object (15)',1,'[{\"added\": {}}]',13,1),(27,'2020-06-05 09:31:16.161480','16','OfflineTask object (16)',1,'[{\"added\": {}}]',13,1),(28,'2020-06-05 09:34:37.477302','17','OfflineTask object (17)',1,'[{\"added\": {}}]',13,1),(29,'2020-06-05 09:40:11.726073','18','OfflineTask object (18)',1,'[{\"added\": {}}]',13,1),(30,'2020-06-05 09:42:35.615024','19','OfflineTask object (19)',1,'[{\"added\": {}}]',13,1),(31,'2020-06-05 09:46:55.171398','20','OfflineTask object (20)',1,'[{\"added\": {}}]',13,1),(32,'2020-06-05 09:49:05.754262','21','OfflineTask object (21)',1,'[{\"added\": {}}]',13,1),(33,'2020-06-16 10:51:42.879636','21','OfflineTask object (21)',3,'',13,1),(34,'2020-06-16 11:07:21.448223','22','OfflineTask object (22)',1,'[{\"added\": {}}]',13,1),(35,'2020-06-16 11:09:00.040853','23','OfflineTask object (23)',1,'[{\"added\": {}}]',13,1),(36,'2020-06-16 11:17:34.232094','24','OfflineTask object (24)',1,'[{\"added\": {}}]',13,1),(37,'2020-06-16 11:21:07.059812','25','OfflineTask object (25)',1,'[{\"added\": {}}]',13,1),(38,'2020-06-16 11:22:11.795723','3','新电脑',1,'[{\"added\": {}}]',7,1),(39,'2020-06-16 11:23:10.408871','2','贰号文件',1,'[{\"added\": {}}]',8,1),(40,'2020-06-16 11:24:26.393602','26','OfflineTask object (26)',1,'[{\"added\": {}}]',13,1),(41,'2020-06-16 15:56:57.005942','27','OfflineTask object (27)',1,'[{\"added\": {}}]',13,1),(42,'2020-06-16 16:38:57.489176','27','OfflineTask object (27)',3,'',13,1),(43,'2020-06-16 16:38:58.794521','27','OfflineTask object (27)',3,'',13,1),(44,'2020-06-16 16:38:59.684938','26','OfflineTask object (26)',3,'',13,1),(45,'2020-06-16 16:38:59.841248','26','OfflineTask object (26)',3,'',13,1),(46,'2020-06-16 16:39:00.351817','25','OfflineTask object (25)',3,'',13,1),(47,'2020-06-16 16:39:00.472453','25','OfflineTask object (25)',3,'',13,1),(48,'2020-06-16 16:39:00.572800','24','OfflineTask object (24)',3,'',13,1),(49,'2020-06-16 16:39:00.671081','24','OfflineTask object (24)',3,'',13,1),(50,'2020-06-16 16:39:00.772241','23','OfflineTask object (23)',3,'',13,1),(51,'2020-06-16 16:39:00.860159','23','OfflineTask object (23)',3,'',13,1),(52,'2020-06-16 17:01:37.658097','1','OfflineTask object (1)',1,'[{\"added\": {}}]',13,1),(53,'2020-06-17 08:36:45.529516','2','OfflineTask object (2)',1,'[{\"added\": {}}]',13,1),(54,'2020-06-17 08:39:01.294272','3','OfflineTask object (3)',1,'[{\"added\": {}}]',13,1),(55,'2020-06-17 09:02:37.233286','4','OfflineTask object (4)',1,'[{\"added\": {}}]',13,1),(56,'2020-06-17 17:04:00.018110','5','OfflineTask object (5)',1,'[{\"added\": {}}]',13,1),(57,'2020-06-17 17:04:15.270874','5','OfflineTask object (5)',3,'',13,1),(58,'2020-06-17 17:04:35.558311','6','OfflineTask object (6)',1,'[{\"added\": {}}]',13,1),(59,'2020-06-18 09:33:43.056216','7','OfflineTask object (7)',1,'[{\"added\": {}}]',13,1),(60,'2020-06-18 09:34:58.766023','8','OfflineTask object (8)',1,'[{\"added\": {}}]',13,1),(61,'2020-06-23 09:27:22.259966','9','OfflineTask object (9)',1,'[{\"added\": {}}]',13,1),(62,'2020-06-23 09:34:18.218787','10','OfflineTask object (10)',1,'[{\"added\": {}}]',13,1),(63,'2020-06-23 09:43:40.165375','11','OfflineTask object (11)',1,'[{\"added\": {}}]',13,1),(64,'2020-06-23 09:56:46.969199','12','OfflineTask object (12)',1,'[{\"added\": {}}]',13,1),(65,'2020-06-23 09:58:57.057452','13','OfflineTask object (13)',1,'[{\"added\": {}}]',13,1),(66,'2020-06-23 10:03:01.317793','14','OfflineTask object (14)',1,'[{\"added\": {}}]',13,1),(67,'2020-06-30 09:08:26.354822','15','OfflineTask object (15)',1,'[{\"added\": {}}]',13,1),(68,'2020-06-30 09:16:00.580741','16','OfflineTask object (16)',1,'[{\"added\": {}}]',13,1),(69,'2020-06-30 09:26:27.932247','17','OfflineTask object (17)',1,'[{\"added\": {}}]',13,1),(70,'2020-06-30 16:02:51.786028','18','OfflineTask object (18)',1,'[{\"added\": {}}]',13,1),(71,'2020-06-30 16:05:23.595833','19','OfflineTask object (19)',1,'[{\"added\": {}}]',13,1),(72,'2020-06-30 16:18:20.659159','20','OfflineTask object (20)',1,'[{\"added\": {}}]',13,1),(73,'2020-07-02 14:38:45.927608','21','OfflineTask object (21)',1,'[{\"added\": {}}]',13,1),(74,'2020-07-06 10:25:34.764561','1','OnlineTask object (1)',1,'[{\"added\": {}}]',29,1),(75,'2020-07-06 10:27:51.763072','2','OnlineTask object (2)',1,'[{\"added\": {}}]',29,1),(76,'2020-07-06 10:48:00.208032','3','OnlineTask object (3)',1,'[{\"added\": {}}]',29,1),(77,'2020-07-06 10:50:41.849215','4','OnlineTask object (4)',1,'[{\"added\": {}}]',29,1);
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
) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2020-06-04 15:33:01.817747'),(2,'auth','0001_initial','2020-06-04 15:33:03.132558'),(3,'admin','0001_initial','2020-06-04 15:33:07.760038'),(4,'admin','0002_logentry_remove_auto_add','2020-06-04 15:33:08.833547'),(5,'admin','0003_logentry_add_action_flag_choices','2020-06-04 15:33:08.873444'),(6,'contenttypes','0002_remove_content_type_name','2020-06-04 15:33:09.649261'),(7,'auth','0002_alter_permission_name_max_length','2020-06-04 15:33:10.147826'),(8,'auth','0003_alter_user_email_max_length','2020-06-04 15:33:10.639616'),(9,'auth','0004_alter_user_username_opts','2020-06-04 15:33:10.672753'),(10,'auth','0005_alter_user_last_login_null','2020-06-04 15:33:11.048762'),(11,'auth','0006_require_contenttypes_0002','2020-06-04 15:33:11.073452'),(12,'auth','0007_alter_validators_add_error_messages','2020-06-04 15:33:11.099786'),(13,'auth','0008_alter_user_username_max_length','2020-06-04 15:33:11.589998'),(14,'auth','0009_alter_user_last_name_max_length','2020-06-04 15:33:12.180339'),(15,'auth','0010_alter_group_name_max_length','2020-06-04 15:33:12.699080'),(16,'auth','0011_update_proxy_permissions','2020-06-04 15:33:12.780552'),(17,'djcelery','0001_initial','2020-06-04 15:33:15.301105'),(18,'offlineTask','0001_initial','2020-06-04 15:33:20.497305'),(19,'sessions','0001_initial','2020-06-04 15:33:22.133045'),(20,'reversion','0001_squashed_0004_auto_20160611_1202','2020-06-18 10:33:34.123694'),(21,'xadmin','0001_initial','2020-06-18 10:33:37.372883'),(22,'xadmin','0002_log','2020-06-18 10:33:40.397703'),(23,'xadmin','0003_auto_20160715_0100','2020-06-18 10:33:42.384141'),(26,'onlineTask','0001_initial','2020-07-06 10:17:13.986368'),(27,'onlineTask','0002_auto_20200706_1020','2020-07-06 10:20:34.021377'),(28,'onlineTask','0003_onlinetask_identify_status','2020-07-06 10:27:06.070848');
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
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `offlinetask_offlinetask`
--

LOCK TABLES `offlinetask_offlinetask` WRITE;
/*!40000 ALTER TABLE `offlinetask_offlinetask` DISABLE KEYS */;
INSERT INTO `offlinetask_offlinetask` VALUES (9,'2020-06-23 09:27:22.250018','9999-12-31','admin',NULL,'2020-06-23 09:27:22.258968','2020-06-23 09:28:47.952913','','p','p','d','u','操场/20200623/092722/origin/','20200623/092722',1,1,1,1,0,0,NULL,1,2),(10,'2020-06-23 09:34:18.206820','9999-12-31','admin',NULL,'2020-06-23 09:34:18.217829','2020-06-23 09:43:47.041407','','p','p','p','d','操场/20200623/093418/origin/','20200623/093418',1,1,1,1,1,1,5,1,2),(11,'2020-06-23 09:43:40.152464','9999-12-31','admin',NULL,'2020-06-23 09:43:40.163381','2020-06-23 09:48:35.535486','','p','p','d','d','测试/20200623/094340/origin/','20200623/094340',1,1,1,1,1,1,6,1,1),(12,'2020-06-23 09:56:46.957261','9999-12-31','admin',NULL,'2020-06-23 09:56:46.968201','2020-06-23 09:56:46.968201','','p','p','p','p','新电脑/20200623/095646/origin/','20200623/095646',1,1,1,1,1,1,5,1,3),(13,'2020-06-23 09:58:56.954494','9999-12-31','admin',NULL,'2020-06-23 09:58:57.056455','2020-06-23 09:59:54.586532','','p','d','p','d','操场/20200623/095856/origin/','20200623/095857',1,1,1,1,1,1,7,1,2),(14,'2020-06-23 10:03:01.307830','9999-12-31','admin',NULL,'2020-06-23 10:03:01.317793','2020-06-23 10:04:24.167412','','p','d','d','d','操场/20200623/100301/origin/','20200623/100301',1,1,1,1,1,1,8,1,2),(15,'2020-06-30 09:08:26.346841','9999-12-31','admin',NULL,'2020-06-30 09:08:26.354822','2020-06-30 09:08:39.077970','','p','p','d','u','操场/20200630/090826/origin/','20200630/090826',1,1,1,1,0,0,NULL,1,2),(16,'2020-06-30 09:16:00.571823','9999-12-31','admin',NULL,'2020-06-30 09:16:00.580741','2020-06-30 09:16:34.100571','','p','d','d','p','新电脑/20200630/091600/origin/','20200630/091600',1,1,1,1,1,1,11,1,3),(17,'2020-06-30 09:26:27.922272','9999-12-31','admin',NULL,'2020-06-30 09:26:27.931248','2020-06-30 09:27:25.527499','','p','d','d','d','新电脑/20200630/092627/origin/','20200630/092627',1,1,1,1,1,1,12,1,3),(18,'2020-06-30 16:02:51.778049','9999-12-31','admin',NULL,'2020-06-30 16:02:51.785030','2020-06-30 16:04:39.062729','','p','d','d','d','测试/20200630/160251/origin/','20200630/160251',1,1,1,1,1,1,13,1,1),(19,'2020-06-30 16:05:23.587892','9999-12-31','admin',NULL,'2020-06-30 16:05:23.594835','2020-06-30 16:06:22.198428','','p','d','d','d','测试/20200630/160523/origin/','20200630/160523',1,1,1,1,1,1,14,1,1),(20,'2020-06-30 16:18:20.561421','9999-12-31','admin',NULL,'2020-06-30 16:18:20.658214','2020-06-30 16:19:20.190998','','p','d','d','d','测试/20200630/161820/origin/','20200630/161820',1,1,1,1,1,1,15,1,1),(21,'2020-07-02 14:38:45.919629','9999-12-31','admin',NULL,'2020-07-02 14:38:45.926609','2020-07-02 14:40:32.900694','','p','d','d','d','新电脑/20200702/143845/origin/','20200702/143845',1,1,1,1,1,1,16,1,3);
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
) ENGINE=InnoDB AUTO_INCREMENT=42 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `offlinetask_singleimagecompareinfo`
--

LOCK TABLES `offlinetask_singleimagecompareinfo` WRITE;
/*!40000 ALTER TABLE `offlinetask_singleimagecompareinfo` DISABLE KEYS */;
INSERT INTO `offlinetask_singleimagecompareinfo` VALUES (7,2,1,1,0.333333333333333,'','D:/202006115wjk/topic/UAV/static/upload/操场/20200623/093418/compare/DJI_0008-OrigRegion.JPG','D:/202006115wjk/topic/UAV/static/upload/操场/20200623/093418/compare/DJI_0008-Position.JPG','D:/202006115wjk/topic/UAV/static/upload/操场/20200623/093418/compare/DJI_0008-CompRegion.JPG','20200623/093418'),(8,2,1,1,0.666666666666667,'','D:/202006115wjk/topic/UAV/static/upload/操场/20200623/093418/compare/DJI_0009-OrigRegion.JPG','D:/202006115wjk/topic/UAV/static/upload/操场/20200623/093418/compare/DJI_0009-Position.JPG','D:/202006115wjk/topic/UAV/static/upload/操场/20200623/093418/compare/DJI_0009-CompRegion.JPG','20200623/093418'),(9,2,1,1,1,'','D:/202006115wjk/topic/UAV/static/upload/操场/20200623/093418/compare/DJI_0010-OrigRegion.JPG','D:/202006115wjk/topic/UAV/static/upload/操场/20200623/093418/compare/DJI_0010-Position.JPG','D:/202006115wjk/topic/UAV/static/upload/操场/20200623/093418/compare/DJI_0010-CompRegion.JPG','20200623/093418'),(10,1,1,1,0.25,'','D:/202006115wjk/topic/UAV/static/upload/测试/20200623/094340/compare/DJI_0008-OrigRegion.JPG','D:/202006115wjk/topic/UAV/static/upload/测试/20200623/094340/compare/DJI_0008-Position.JPG','D:/202006115wjk/topic/UAV/static/upload/测试/20200623/094340/compare/DJI_0008-CompRegion.JPG','20200623/094340'),(11,1,1,1,0.5,'','D:/202006115wjk/topic/UAV/static/upload/测试/20200623/094340/compare/DJI_0009-OrigRegion.JPG','D:/202006115wjk/topic/UAV/static/upload/测试/20200623/094340/compare/DJI_0009-Position.JPG','D:/202006115wjk/topic/UAV/static/upload/测试/20200623/094340/compare/DJI_0009-CompRegion.JPG','20200623/094340'),(12,1,1,1,0.75,'','D:/202006115wjk/topic/UAV/static/upload/测试/20200623/094340/compare/DJI_0010-OrigRegion.JPG','D:/202006115wjk/topic/UAV/static/upload/测试/20200623/094340/compare/DJI_0010-Position.JPG','D:/202006115wjk/topic/UAV/static/upload/测试/20200623/094340/compare/DJI_0010-CompRegion.JPG','20200623/094340'),(13,1,1,1,1,'','D:/202006115wjk/topic/UAV/static/upload/测试/20200623/094340/compare/DJI_0011-OrigRegion.JPG','D:/202006115wjk/topic/UAV/static/upload/测试/20200623/094340/compare/DJI_0011-Position.JPG','D:/202006115wjk/topic/UAV/static/upload/测试/20200623/094340/compare/DJI_0011-CompRegion.JPG','20200623/094340'),(14,3,1,0,0.25,'','D:/202006115wjk/topic/UAV/static/upload/新电脑/20200623/095646/compare/DJI_0008-OrigRegion.JPG','D:/202006115wjk/topic/UAV/static/upload/新电脑/20200623/095646/compare/DJI_0008-Position.JPG','D:/202006115wjk/topic/UAV/static/upload/新电脑/20200623/095646/compare/DJI_0008-CompRegion.JPG','20200623/095646'),(15,3,1,0,0.5,'','D:/202006115wjk/topic/UAV/static/upload/新电脑/20200623/095646/compare/DJI_0009-OrigRegion.JPG','D:/202006115wjk/topic/UAV/static/upload/新电脑/20200623/095646/compare/DJI_0009-Position.JPG','D:/202006115wjk/topic/UAV/static/upload/新电脑/20200623/095646/compare/DJI_0009-CompRegion.JPG','20200623/095646'),(16,3,1,0,0.75,'','D:/202006115wjk/topic/UAV/static/upload/新电脑/20200623/095646/compare/DJI_0010-OrigRegion.JPG','D:/202006115wjk/topic/UAV/static/upload/新电脑/20200623/095646/compare/DJI_0010-Position.JPG','D:/202006115wjk/topic/UAV/static/upload/新电脑/20200623/095646/compare/DJI_0010-CompRegion.JPG','20200623/095646'),(17,3,1,0,1,'','D:/202006115wjk/topic/UAV/static/upload/新电脑/20200623/095646/compare/DJI_0011-OrigRegion.JPG','D:/202006115wjk/topic/UAV/static/upload/新电脑/20200623/095646/compare/DJI_0011-Position.JPG','D:/202006115wjk/topic/UAV/static/upload/新电脑/20200623/095646/compare/DJI_0011-CompRegion.JPG','20200623/095646'),(18,2,1,0,0.5,'','D:/202006115wjk/topic/UAV/static/upload/操场/20200623/095856/compare/DJI_0008-OrigRegion.JPG','D:/202006115wjk/topic/UAV/static/upload/操场/20200623/095856/compare/DJI_0008-Position.JPG','D:/202006115wjk/topic/UAV/static/upload/操场/20200623/095856/compare/DJI_0008-CompRegion.JPG','20200623/095857'),(19,2,1,0,1,'','D:/202006115wjk/topic/UAV/static/upload/操场/20200623/095856/compare/DJI_0009-OrigRegion.JPG','D:/202006115wjk/topic/UAV/static/upload/操场/20200623/095856/compare/DJI_0009-Position.JPG','D:/202006115wjk/topic/UAV/static/upload/操场/20200623/095856/compare/DJI_0009-CompRegion.JPG','20200623/095857'),(20,2,1,1,0.25,'','D:/202006115wjk/topic/UAV/static/upload/操场/20200623/100301/compare/DJI_0008-OrigRegion.JPG','D:/202006115wjk/topic/UAV/static/upload/操场/20200623/100301/compare/DJI_0008-Position.JPG','D:/202006115wjk/topic/UAV/static/upload/操场/20200623/100301/compare/DJI_0008-CompRegion.JPG','20200623/100301'),(21,2,1,1,0.5,'','D:/202006115wjk/topic/UAV/static/upload/操场/20200623/100301/compare/DJI_0009-OrigRegion.JPG','D:/202006115wjk/topic/UAV/static/upload/操场/20200623/100301/compare/DJI_0009-Position.JPG','D:/202006115wjk/topic/UAV/static/upload/操场/20200623/100301/compare/DJI_0009-CompRegion.JPG','20200623/100301'),(22,2,1,1,0.75,'','D:/202006115wjk/topic/UAV/static/upload/操场/20200623/100301/compare/DJI_0010-OrigRegion.JPG','D:/202006115wjk/topic/UAV/static/upload/操场/20200623/100301/compare/DJI_0010-Position.JPG','D:/202006115wjk/topic/UAV/static/upload/操场/20200623/100301/compare/DJI_0010-CompRegion.JPG','20200623/100301'),(23,2,1,1,1,'','D:/202006115wjk/topic/UAV/static/upload/操场/20200623/100301/compare/DJI_0011-OrigRegion.JPG','D:/202006115wjk/topic/UAV/static/upload/操场/20200623/100301/compare/DJI_0011-Position.JPG','D:/202006115wjk/topic/UAV/static/upload/操场/20200623/100301/compare/DJI_0011-CompRegion.JPG','20200623/100301'),(24,3,1,0,0.333333333333333,'','D:/202006115wjk/topic/UAV/static/upload/新电脑/20200630/091600/compare/DJI_0008-OrigRegion.JPG','D:/202006115wjk/topic/UAV/static/upload/新电脑/20200630/091600/compare/DJI_0008-Position.JPG','D:/202006115wjk/topic/UAV/static/upload/新电脑/20200630/091600/compare/DJI_0008-CompRegion.JPG','20200630/091600'),(25,3,1,0,0.666666666666667,'','D:/202006115wjk/topic/UAV/static/upload/新电脑/20200630/091600/compare/DJI_0009-OrigRegion.JPG','D:/202006115wjk/topic/UAV/static/upload/新电脑/20200630/091600/compare/DJI_0009-Position.JPG','D:/202006115wjk/topic/UAV/static/upload/新电脑/20200630/091600/compare/DJI_0009-CompRegion.JPG','20200630/091600'),(26,3,1,0,1,'','D:/202006115wjk/topic/UAV/static/upload/新电脑/20200630/091600/compare/DJI_0010-OrigRegion.JPG','D:/202006115wjk/topic/UAV/static/upload/新电脑/20200630/091600/compare/DJI_0010-Position.JPG','D:/202006115wjk/topic/UAV/static/upload/新电脑/20200630/091600/compare/DJI_0010-CompRegion.JPG','20200630/091600'),(27,3,1,1,0.333333333333333,'','D:/202006115wjk/topic/UAV/static/upload/新电脑/20200630/092627/compare/DJI_0008-OrigRegion.JPG','D:/202006115wjk/topic/UAV/static/upload/新电脑/20200630/092627/compare/DJI_0008-Position.JPG','D:/202006115wjk/topic/UAV/static/upload/新电脑/20200630/092627/compare/DJI_0008-CompRegion.JPG','20200630/092627'),(28,3,1,1,0.666666666666667,'','D:/202006115wjk/topic/UAV/static/upload/新电脑/20200630/092627/compare/DJI_0009-OrigRegion.JPG','D:/202006115wjk/topic/UAV/static/upload/新电脑/20200630/092627/compare/DJI_0009-Position.JPG','D:/202006115wjk/topic/UAV/static/upload/新电脑/20200630/092627/compare/DJI_0009-CompRegion.JPG','20200630/092627'),(29,3,1,1,1,'','D:/202006115wjk/topic/UAV/static/upload/新电脑/20200630/092627/compare/DJI_0010-OrigRegion.JPG','D:/202006115wjk/topic/UAV/static/upload/新电脑/20200630/092627/compare/DJI_0010-Position.JPG','D:/202006115wjk/topic/UAV/static/upload/新电脑/20200630/092627/compare/DJI_0010-CompRegion.JPG','20200630/092627'),(30,1,1,1,0.333333333333333,'','D:/202006115wjk/topic/UAV/static/upload/测试/20200630/160251/compare/DJI_0008-OrigRegion.JPG','D:/202006115wjk/topic/UAV/static/upload/测试/20200630/160251/compare/DJI_0008-Position.JPG','D:/202006115wjk/topic/UAV/static/upload/测试/20200630/160251/compare/DJI_0008-CompRegion.JPG','20200630/160251'),(31,1,1,1,0.666666666666667,'','D:/202006115wjk/topic/UAV/static/upload/测试/20200630/160251/compare/DJI_0009-OrigRegion.JPG','D:/202006115wjk/topic/UAV/static/upload/测试/20200630/160251/compare/DJI_0009-Position.JPG','D:/202006115wjk/topic/UAV/static/upload/测试/20200630/160251/compare/DJI_0009-CompRegion.JPG','20200630/160251'),(32,1,1,0,1,'','D:/202006115wjk/topic/UAV/static/upload/测试/20200630/160251/compare/DJI_0010-OrigRegion.JPG','D:/202006115wjk/topic/UAV/static/upload/测试/20200630/160251/compare/DJI_0010-Position.JPG','D:/202006115wjk/topic/UAV/static/upload/测试/20200630/160251/compare/DJI_0010-CompRegion.JPG','20200630/160251'),(33,1,1,0,0.333333333333333,'','D:/202006115wjk/topic/UAV/static/upload/测试/20200630/160523/compare/DJI_0008-OrigRegion.JPG','D:/202006115wjk/topic/UAV/static/upload/测试/20200630/160523/compare/DJI_0008-Position.JPG','D:/202006115wjk/topic/UAV/static/upload/测试/20200630/160523/compare/DJI_0008-CompRegion.JPG','20200630/160523'),(34,1,1,0,0.666666666666667,'','D:/202006115wjk/topic/UAV/static/upload/测试/20200630/160523/compare/DJI_0009-OrigRegion.JPG','D:/202006115wjk/topic/UAV/static/upload/测试/20200630/160523/compare/DJI_0009-Position.JPG','D:/202006115wjk/topic/UAV/static/upload/测试/20200630/160523/compare/DJI_0009-CompRegion.JPG','20200630/160523'),(35,1,1,0,1,'','D:/202006115wjk/topic/UAV/static/upload/测试/20200630/160523/compare/DJI_0010-OrigRegion.JPG','D:/202006115wjk/topic/UAV/static/upload/测试/20200630/160523/compare/DJI_0010-Position.JPG','D:/202006115wjk/topic/UAV/static/upload/测试/20200630/160523/compare/DJI_0010-CompRegion.JPG','20200630/160523'),(36,1,1,1,0.333333333333333,'','D:/202006115wjk/topic/UAV/static/upload/测试/20200630/161820/compare/DJI_0008-OrigRegion.JPG','D:/202006115wjk/topic/UAV/static/upload/测试/20200630/161820/compare/DJI_0008-Position.JPG','D:/202006115wjk/topic/UAV/static/upload/测试/20200630/161820/compare/DJI_0008-CompRegion.JPG','20200630/161820'),(37,1,1,1,0.666666666666667,'','D:/202006115wjk/topic/UAV/static/upload/测试/20200630/161820/compare/DJI_0009-OrigRegion.JPG','D:/202006115wjk/topic/UAV/static/upload/测试/20200630/161820/compare/DJI_0009-Position.JPG','D:/202006115wjk/topic/UAV/static/upload/测试/20200630/161820/compare/DJI_0009-CompRegion.JPG','20200630/161820'),(38,1,1,1,1,'','D:/202006115wjk/topic/UAV/static/upload/测试/20200630/161820/compare/DJI_0010-OrigRegion.JPG','D:/202006115wjk/topic/UAV/static/upload/测试/20200630/161820/compare/DJI_0010-Position.JPG','D:/202006115wjk/topic/UAV/static/upload/测试/20200630/161820/compare/DJI_0010-CompRegion.JPG','20200630/161820'),(39,3,1,1,0.333333333333333,'','D:/202006115wjk/topic/UAV/static/upload/新电脑/20200702/143845/compare/DJI_0008-OrigRegion.JPG','D:/202006115wjk/topic/UAV/static/upload/新电脑/20200702/143845/compare/DJI_0008-Position.JPG','D:/202006115wjk/topic/UAV/static/upload/新电脑/20200702/143845/compare/DJI_0008-CompRegion.JPG','20200702/143845'),(40,3,1,1,0.666666666666667,'','D:/202006115wjk/topic/UAV/static/upload/新电脑/20200702/143845/compare/DJI_0009-OrigRegion.JPG','D:/202006115wjk/topic/UAV/static/upload/新电脑/20200702/143845/compare/DJI_0009-Position.JPG','D:/202006115wjk/topic/UAV/static/upload/新电脑/20200702/143845/compare/DJI_0009-CompRegion.JPG','20200702/143845'),(41,3,1,1,1,'','D:/202006115wjk/topic/UAV/static/upload/新电脑/20200702/143845/compare/DJI_0010-OrigRegion.JPG','D:/202006115wjk/topic/UAV/static/upload/新电脑/20200702/143845/compare/DJI_0010-Position.JPG','D:/202006115wjk/topic/UAV/static/upload/新电脑/20200702/143845/compare/DJI_0010-CompRegion.JPG','20200702/143845');
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
  `is_confirm` tinyint(1) NOT NULL,
  `is_identify` tinyint(1) NOT NULL,
  `is_show` tinyint(1) NOT NULL,
  `progress` double NOT NULL,
  `imagePreprocessPath` varchar(1000) NOT NULL,
  `imageIdentifyPath` varchar(1000) NOT NULL,
  `imageIdentifyResultPath` varchar(1000) NOT NULL,
  `overDate` varchar(45) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `offlinetask_singleimageidentifyinfo`
--

LOCK TABLES `offlinetask_singleimageidentifyinfo` WRITE;
/*!40000 ALTER TABLE `offlinetask_singleimageidentifyinfo` DISABLE KEYS */;
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
) ENGINE=InnoDB AUTO_INCREMENT=66 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `offlinetask_singleimagepreprocessinfo`
--

LOCK TABLES `offlinetask_singleimagepreprocessinfo` WRITE;
/*!40000 ALTER TABLE `offlinetask_singleimagepreprocessinfo` DISABLE KEYS */;
INSERT INTO `offlinetask_singleimagepreprocessinfo` VALUES (25,2,1,1,'D:/202006115wjk/topic/UAV/static/upload/操场/20200623/092722/origin/DJI_0008.JPG','D:/202006115wjk/topic/UAV/static/upload/操场/20200623/092722/preprocess/DJI_0008.JPG','20200623/092722',0.333333333333333),(26,2,1,1,'D:/202006115wjk/topic/UAV/static/upload/操场/20200623/092722/origin/DJI_0009.JPG','D:/202006115wjk/topic/UAV/static/upload/操场/20200623/092722/preprocess/DJI_0009.JPG','20200623/092722',1.33333333333333),(27,2,1,1,'D:/202006115wjk/topic/UAV/static/upload/操场/20200623/092722/origin/DJI_0010.JPG','D:/202006115wjk/topic/UAV/static/upload/操场/20200623/092722/preprocess/DJI_0010.JPG','20200623/092722',2.33333333333333),(28,2,1,0,'D:/202006115wjk/topic/UAV/static/upload/操场/20200623/093418/origin/DJI_0008.JPG','D:/202006115wjk/topic/UAV/static/upload/操场/20200623/093418/preprocess/DJI_0008.JPG','20200623/093418',0.333333333333333),(29,2,1,0,'D:/202006115wjk/topic/UAV/static/upload/操场/20200623/093418/origin/DJI_0009.JPG','D:/202006115wjk/topic/UAV/static/upload/操场/20200623/093418/preprocess/DJI_0009.JPG','20200623/093418',1.33333333333333),(30,2,1,0,'D:/202006115wjk/topic/UAV/static/upload/操场/20200623/093418/origin/DJI_0010.JPG','D:/202006115wjk/topic/UAV/static/upload/操场/20200623/093418/preprocess/DJI_0010.JPG','20200623/093418',2.33333333333333),(31,1,1,1,'D:/202006115wjk/topic/UAV/static/upload/测试/20200623/094340/origin/DJI_0008.JPG','D:/202006115wjk/topic/UAV/static/upload/测试/20200623/094340/preprocess/DJI_0008.JPG','20200623/094340',0.25),(32,1,1,1,'D:/202006115wjk/topic/UAV/static/upload/测试/20200623/094340/origin/DJI_0009.JPG','D:/202006115wjk/topic/UAV/static/upload/测试/20200623/094340/preprocess/DJI_0009.JPG','20200623/094340',0.5),(33,1,1,1,'D:/202006115wjk/topic/UAV/static/upload/测试/20200623/094340/origin/DJI_0010.JPG','D:/202006115wjk/topic/UAV/static/upload/测试/20200623/094340/preprocess/DJI_0010.JPG','20200623/094340',0.75),(34,1,1,1,'D:/202006115wjk/topic/UAV/static/upload/测试/20200623/094340/origin/DJI_0011.JPG','D:/202006115wjk/topic/UAV/static/upload/测试/20200623/094340/preprocess/DJI_0011.JPG','20200623/094340',1),(35,3,1,0,'D:/202006115wjk/topic/UAV/static/upload/新电脑/20200623/095646/origin/DJI_0008.JPG','D:/202006115wjk/topic/UAV/static/upload/新电脑/20200623/095646/preprocess/DJI_0008.JPG','20200623/095646',0.25),(36,3,1,0,'D:/202006115wjk/topic/UAV/static/upload/新电脑/20200623/095646/origin/DJI_0009.JPG','D:/202006115wjk/topic/UAV/static/upload/新电脑/20200623/095646/preprocess/DJI_0009.JPG','20200623/095646',0.5),(37,3,1,0,'D:/202006115wjk/topic/UAV/static/upload/新电脑/20200623/095646/origin/DJI_0010.JPG','D:/202006115wjk/topic/UAV/static/upload/新电脑/20200623/095646/preprocess/DJI_0010.JPG','20200623/095646',0.75),(38,3,1,0,'D:/202006115wjk/topic/UAV/static/upload/新电脑/20200623/095646/origin/DJI_0011.JPG','D:/202006115wjk/topic/UAV/static/upload/新电脑/20200623/095646/preprocess/DJI_0011.JPG','20200623/095646',1),(39,2,1,1,'D:/202006115wjk/topic/UAV/static/upload/操场/20200623/095856/origin/DJI_0008.JPG','D:/202006115wjk/topic/UAV/static/upload/操场/20200623/095856/preprocess/DJI_0008.JPG','20200623/095857',0.5),(40,2,1,1,'D:/202006115wjk/topic/UAV/static/upload/操场/20200623/095856/origin/DJI_0009.JPG','D:/202006115wjk/topic/UAV/static/upload/操场/20200623/095856/preprocess/DJI_0009.JPG','20200623/095857',1),(41,2,1,1,'D:/202006115wjk/topic/UAV/static/upload/操场/20200623/100301/origin/DJI_0008.JPG','D:/202006115wjk/topic/UAV/static/upload/操场/20200623/100301/preprocess/DJI_0008.JPG','20200623/100301',0.25),(42,2,1,1,'D:/202006115wjk/topic/UAV/static/upload/操场/20200623/100301/origin/DJI_0009.JPG','D:/202006115wjk/topic/UAV/static/upload/操场/20200623/100301/preprocess/DJI_0009.JPG','20200623/100301',0.5),(43,2,1,1,'D:/202006115wjk/topic/UAV/static/upload/操场/20200623/100301/origin/DJI_0010.JPG','D:/202006115wjk/topic/UAV/static/upload/操场/20200623/100301/preprocess/DJI_0010.JPG','20200623/100301',0.75),(44,2,1,1,'D:/202006115wjk/topic/UAV/static/upload/操场/20200623/100301/origin/DJI_0011.JPG','D:/202006115wjk/topic/UAV/static/upload/操场/20200623/100301/preprocess/DJI_0011.JPG','20200623/100301',1),(45,2,1,1,'D:/202006115wjk/topic/UAV/static/upload/操场/20200630/090826/origin/DJI_0008.JPG','D:/202006115wjk/topic/UAV/static/upload/操场/20200630/090826/preprocess/DJI_0008.JPG','20200630/090826',0.333333333333333),(46,2,1,1,'D:/202006115wjk/topic/UAV/static/upload/操场/20200630/090826/origin/DJI_0009.JPG','D:/202006115wjk/topic/UAV/static/upload/操场/20200630/090826/preprocess/DJI_0009.JPG','20200630/090826',0.666666666666667),(47,2,1,1,'D:/202006115wjk/topic/UAV/static/upload/操场/20200630/090826/origin/DJI_0010.JPG','D:/202006115wjk/topic/UAV/static/upload/操场/20200630/090826/preprocess/DJI_0010.JPG','20200630/090826',1),(48,3,1,1,'D:/202006115wjk/topic/UAV/static/upload/新电脑/20200630/091600/origin/DJI_0008.JPG','D:/202006115wjk/topic/UAV/static/upload/新电脑/20200630/091600/preprocess/DJI_0008.JPG','20200630/091600',0.333333333333333),(49,3,1,1,'D:/202006115wjk/topic/UAV/static/upload/新电脑/20200630/091600/origin/DJI_0009.JPG','D:/202006115wjk/topic/UAV/static/upload/新电脑/20200630/091600/preprocess/DJI_0009.JPG','20200630/091600',0.666666666666667),(50,3,1,1,'D:/202006115wjk/topic/UAV/static/upload/新电脑/20200630/091600/origin/DJI_0010.JPG','D:/202006115wjk/topic/UAV/static/upload/新电脑/20200630/091600/preprocess/DJI_0010.JPG','20200630/091600',1),(51,3,1,1,'D:/202006115wjk/topic/UAV/static/upload/新电脑/20200630/092627/origin/DJI_0008.JPG','D:/202006115wjk/topic/UAV/static/upload/新电脑/20200630/092627/preprocess/DJI_0008.JPG','20200630/092627',0.333333333333333),(52,3,1,1,'D:/202006115wjk/topic/UAV/static/upload/新电脑/20200630/092627/origin/DJI_0009.JPG','D:/202006115wjk/topic/UAV/static/upload/新电脑/20200630/092627/preprocess/DJI_0009.JPG','20200630/092627',0.666666666666667),(53,3,1,1,'D:/202006115wjk/topic/UAV/static/upload/新电脑/20200630/092627/origin/DJI_0010.JPG','D:/202006115wjk/topic/UAV/static/upload/新电脑/20200630/092627/preprocess/DJI_0010.JPG','20200630/092627',1),(54,1,1,1,'D:/202006115wjk/topic/UAV/static/upload/测试/20200630/160251/origin/DJI_0008.JPG','D:/202006115wjk/topic/UAV/static/upload/测试/20200630/160251/preprocess/DJI_0008.JPG','20200630/160251',0.333333333333333),(55,1,1,1,'D:/202006115wjk/topic/UAV/static/upload/测试/20200630/160251/origin/DJI_0009.JPG','D:/202006115wjk/topic/UAV/static/upload/测试/20200630/160251/preprocess/DJI_0009.JPG','20200630/160251',0.666666666666667),(56,1,1,1,'D:/202006115wjk/topic/UAV/static/upload/测试/20200630/160251/origin/DJI_0010.JPG','D:/202006115wjk/topic/UAV/static/upload/测试/20200630/160251/preprocess/DJI_0010.JPG','20200630/160251',1),(57,1,1,0,'D:/202006115wjk/topic/UAV/static/upload/测试/20200630/160523/origin/DJI_0008.JPG','D:/202006115wjk/topic/UAV/static/upload/测试/20200630/160523/preprocess/DJI_0008.JPG','20200630/160523',0.333333333333333),(58,1,1,0,'D:/202006115wjk/topic/UAV/static/upload/测试/20200630/160523/origin/DJI_0009.JPG','D:/202006115wjk/topic/UAV/static/upload/测试/20200630/160523/preprocess/DJI_0009.JPG','20200630/160523',0.666666666666667),(59,1,1,0,'D:/202006115wjk/topic/UAV/static/upload/测试/20200630/160523/origin/DJI_0010.JPG','D:/202006115wjk/topic/UAV/static/upload/测试/20200630/160523/preprocess/DJI_0010.JPG','20200630/160523',1),(60,1,1,1,'D:/202006115wjk/topic/UAV/static/upload/测试/20200630/161820/origin/DJI_0008.JPG','D:/202006115wjk/topic/UAV/static/upload/测试/20200630/161820/preprocess/DJI_0008.JPG','20200630/161820',0.333333333333333),(61,1,1,1,'D:/202006115wjk/topic/UAV/static/upload/测试/20200630/161820/origin/DJI_0009.JPG','D:/202006115wjk/topic/UAV/static/upload/测试/20200630/161820/preprocess/DJI_0009.JPG','20200630/161820',0.666666666666667),(62,1,1,1,'D:/202006115wjk/topic/UAV/static/upload/测试/20200630/161820/origin/DJI_0010.JPG','D:/202006115wjk/topic/UAV/static/upload/测试/20200630/161820/preprocess/DJI_0010.JPG','20200630/161820',1),(63,3,1,1,'D:/202006115wjk/topic/UAV/static/upload/新电脑/20200702/143845/origin/DJI_0008.JPG','D:/202006115wjk/topic/UAV/static/upload/新电脑/20200702/143845/preprocess/DJI_0008.JPG','20200702/143845',0.333333333333333),(64,3,1,1,'D:/202006115wjk/topic/UAV/static/upload/新电脑/20200702/143845/origin/DJI_0009.JPG','D:/202006115wjk/topic/UAV/static/upload/新电脑/20200702/143845/preprocess/DJI_0009.JPG','20200702/143845',0.666666666666667),(65,3,1,1,'D:/202006115wjk/topic/UAV/static/upload/新电脑/20200702/143845/origin/DJI_0010.JPG','D:/202006115wjk/topic/UAV/static/upload/新电脑/20200702/143845/preprocess/DJI_0010.JPG','20200702/143845',1);
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
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `offlinetask_singleimagespliceinfo`
--

LOCK TABLES `offlinetask_singleimagespliceinfo` WRITE;
/*!40000 ALTER TABLE `offlinetask_singleimagespliceinfo` DISABLE KEYS */;
INSERT INTO `offlinetask_singleimagespliceinfo` VALUES (5,2,1,1,1,'','D:/202006115wjk/topic/UAV/static/upload/操场/20200623/092722/splice/merged_img.JPG','D:/202006115wjk/topic/UAV/static/upload/操场/20200623/092722/splice/gps_points.csv','20200623/092722'),(6,2,1,0,1,'','D:/202006115wjk/topic/UAV/static/upload/操场/20200623/093418/splice/merged_img.JPG','D:/202006115wjk/topic/UAV/static/upload/操场/20200623/093418/splice/gps_points.csv','20200623/093418'),(7,1,1,1,1,'','D:/202006115wjk/topic/UAV/static/upload/测试/20200623/094340/splice/merged_img.JPG','D:/202006115wjk/topic/UAV/static/upload/测试/20200623/094340/splice/gps_points.csv','20200623/094340'),(8,3,1,0,1,'','D:/202006115wjk/topic/UAV/static/upload/新电脑/20200623/095646/splice/merged_img.JPG','D:/202006115wjk/topic/UAV/static/upload/新电脑/20200623/095646/splice/gps_points.csv','20200623/095646'),(9,2,1,0,1,'','D:/202006115wjk/topic/UAV/static/upload/操场/20200623/095856/splice/merged_img.JPG','D:/202006115wjk/topic/UAV/static/upload/操场/20200623/095856/splice/gps_points.csv','20200623/095857'),(10,2,1,1,1,'','D:/202006115wjk/topic/UAV/static/upload/操场/20200623/100301/splice/merged_img.JPG','D:/202006115wjk/topic/UAV/static/upload/操场/20200623/100301/splice/gps_points.csv','20200623/100301'),(11,2,1,1,1,'','D:/202006115wjk/topic/UAV/static/upload/操场/20200630/090826/splice/thumbnail.JPG','D:/202006115wjk/topic/UAV/static/upload/操场/20200630/090826/splice/gps_points.csv','20200630/090826'),(12,3,1,1,1,'','D:/202006115wjk/topic/UAV/static/upload/新电脑/20200630/091600/splice/thumbnail.JPG','D:/202006115wjk/topic/UAV/static/upload/新电脑/20200630/091600/splice/gps_points.csv','20200630/091600'),(13,3,1,1,1,'','D:/202006115wjk/topic/UAV/static/upload/新电脑/20200630/092627/splice/thumbnail.JPG','D:/202006115wjk/topic/UAV/static/upload/新电脑/20200630/092627/splice/gps_points.csv','20200630/092627'),(14,1,1,1,1,'','D:/202006115wjk/topic/UAV/static/upload/测试/20200630/160251/splice/thumbnail.JPG','D:/202006115wjk/topic/UAV/static/upload/测试/20200630/160251/splice/gps_points.csv','20200630/160251'),(15,1,1,1,1,'','D:/202006115wjk/topic/UAV/static/upload/测试/20200630/160523/splice/thumbnail.JPG','D:/202006115wjk/topic/UAV/static/upload/测试/20200630/160523/splice/gps_points.csv','20200630/160523'),(16,1,1,1,1,'','D:/202006115wjk/topic/UAV/static/upload/测试/20200630/161820/splice/thumbnail.JPG','D:/202006115wjk/topic/UAV/static/upload/测试/20200630/161820/splice/gps_points.csv','20200630/161820'),(17,3,1,1,1,'','D:/202006115wjk/topic/UAV/static/upload/新电脑/20200702/143845/splice/thumbnail.JPG','D:/202006115wjk/topic/UAV/static/upload/新电脑/20200702/143845/splice/gps_points.csv','20200702/143845');
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
  `titleId` int(11) NOT NULL,
  `is_confirm` tinyint(1) NOT NULL,
  `is_identify` tinyint(1) NOT NULL,
  `is_show` tinyint(1) NOT NULL,
  `progress` double NOT NULL,
  `imagePreprocessPath` varchar(1000) NOT NULL,
  `imageIdentifyPath` varchar(1000) NOT NULL,
  `imageIdentifyResultPath` varchar(1000) NOT NULL,
  `overDate` varchar(45) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `onlinetask_onlineimageidentifyinfo`
--

LOCK TABLES `onlinetask_onlineimageidentifyinfo` WRITE;
/*!40000 ALTER TABLE `onlinetask_onlineimageidentifyinfo` DISABLE KEYS */;
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
  `title` varchar(45) NOT NULL,
  `description` longtext,
  `overDate` varchar(45) NOT NULL,
  `isIdentifyPre` tinyint(1) NOT NULL,
  `identify_status` varchar(6),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `onlinetask_onlinetask`
--

LOCK TABLES `onlinetask_onlinetask` WRITE;
/*!40000 ALTER TABLE `onlinetask_onlinetask` DISABLE KEYS */;
INSERT INTO `onlinetask_onlinetask` VALUES (1,'2020-07-06 10:25:34.763565','9999-12-31','admin',NULL,'2020-07-06 10:25:34.763565','2020-07-06 10:25:34.763565','123','','20200706/102534',1,'u'),(2,'2020-07-06 10:27:51.762073','9999-12-31','admin',NULL,'2020-07-06 10:27:51.762073','2020-07-06 10:27:51.762073','13','','20200706/102751',1,'u'),(3,'2020-07-06 10:48:00.206992','9999-12-31','admin',NULL,'2020-07-06 10:48:00.208032','2020-07-06 10:48:00.208032','啊实打实1','','20200706/104800',1,'u'),(4,'2020-07-06 10:50:41.848258','9999-12-31','admin',NULL,'2020-07-06 10:50:41.849215','2020-07-06 10:50:41.849215','太','','20200706/105041',1,'u');
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

-- Dump completed on 2020-07-06 14:48:05
