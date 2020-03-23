-- MySQL dump 10.13  Distrib 8.0.18, for macos10.14 (x86_64)
--
-- Host: localhost    Database: GP1ModelToSql
-- ------------------------------------------------------
-- Server version	8.0.18

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
-- Table structure for table `App_usermodel`
--

DROP TABLE IF EXISTS `App_usermodel`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `App_usermodel` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `u_name` varchar(16) NOT NULL,
  `u_icon` varchar(100) NOT NULL,
  `u_predict` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `App_usermodel`
--

LOCK TABLES `App_usermodel` WRITE;
/*!40000 ALTER TABLE `App_usermodel` DISABLE KEYS */;
/*!40000 ALTER TABLE `App_usermodel` ENABLE KEYS */;
UNLOCK TABLES;

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
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
INSERT INTO `auth_group_permissions` VALUES (1,1,33),(2,1,34),(3,1,35),(4,1,36);
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
) ENGINE=InnoDB AUTO_INCREMENT=42 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can add permission',2,'add_permission'),(5,'Can change permission',2,'change_permission'),(6,'Can delete permission',2,'delete_permission'),(7,'Can add group',3,'add_group'),(8,'Can change group',3,'change_group'),(9,'Can delete group',3,'delete_group'),(10,'Can add user',4,'add_user'),(11,'Can change user',4,'change_user'),(12,'Can delete user',4,'delete_user'),(13,'Can add content type',5,'add_contenttype'),(14,'Can change content type',5,'change_contenttype'),(15,'Can delete content type',5,'delete_contenttype'),(16,'Can add session',6,'add_session'),(17,'Can change session',6,'change_session'),(18,'Can delete session',6,'delete_session'),(19,'Can add user model',7,'add_usermodel'),(20,'Can change user model',7,'change_usermodel'),(21,'Can delete user model',7,'delete_usermodel'),(22,'Can add book',8,'add_book'),(23,'Can change book',8,'change_book'),(24,'Can delete book',8,'delete_book'),(25,'Can view log entry',1,'view_logentry'),(26,'Can view permission',2,'view_permission'),(27,'Can view group',3,'view_group'),(28,'Can view user',4,'view_user'),(29,'Can view content type',5,'view_contenttype'),(30,'Can view session',6,'view_session'),(31,'Can view book',8,'view_book'),(32,'Can view user model',7,'view_usermodel'),(33,'Can add  preprocesstask',9,'add_preprocesstask'),(34,'Can delete preprocesstask',9,'delete_preprocesstask'),(35,'Can view preprocesstask',9,'view_preprocesstask'),(36,'Can change preprocesstask',9,'change_preprocesstask');
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
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$150000$vxycj84BT9F5$OvPgZkwOlvYtcQQLYLBhI4fiqn4Hpz+IaTrdpX/6qJw=','2020-02-27 12:20:20.885646',0,'admin','','','admin123@qq.com',1,1,'2020-02-19 18:07:04.751397'),(2,'pbkdf2_sha256$150000$HkSc06ys1C6h$gdCHXh3L0P9m8naU3KogTSxk7HbD8Ux/umHuW9hwYi8=',NULL,0,'test123','','','admin123@qq.com',0,1,'2020-02-20 17:11:29.276014');
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
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
INSERT INTO `auth_user_groups` VALUES (3,1,1),(1,2,1);
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
-- Table structure for table `Book`
--

DROP TABLE IF EXISTS `Book`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Book` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `b_name` varchar(16) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Book`
--

LOCK TABLES `Book` WRITE;
/*!40000 ALTER TABLE `Book` DISABLE KEYS */;
/*!40000 ALTER TABLE `Book` ENABLE KEYS */;
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
) ENGINE=InnoDB AUTO_INCREMENT=56 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (1,'2020-02-27 10:05:49.451878','1','PreprocessTask object (1)',1,'[{\"added\": {}}]',9,1),(2,'2020-02-27 10:06:03.839941','1','PreprocessTask object (1)',3,'',9,1),(3,'2020-02-27 10:06:40.818855','2','PreprocessTask object (2)',1,'[{\"added\": {}}]',9,1),(4,'2020-02-27 11:27:41.722757','3','PreprocessTask object (3)',1,'[{\"added\": {}}]',9,1),(5,'2020-02-27 11:31:10.869447','2','PreprocessTask object (2)',3,'',9,1),(6,'2020-02-27 11:51:59.975823','4','PreprocessTask object (4)',1,'[{\"added\": {}}]',9,1),(7,'2020-02-27 11:52:11.285697','4','PreprocessTask object (4)',3,'',9,1),(8,'2020-02-27 11:52:11.287034','3','PreprocessTask object (3)',3,'',9,1),(9,'2020-02-27 12:10:42.721380','5','PreprocessTask object (5)',1,'[{\"added\": {}}]',9,1),(10,'2020-02-28 10:22:01.077188','6','PreprocessTask object (6)',1,'[{\"added\": {}}]',9,1),(11,'2020-02-28 10:22:25.208677','6','PreprocessTask object (6)',3,'',9,1),(12,'2020-02-28 10:22:25.219688','5','PreprocessTask object (5)',3,'',9,1),(13,'2020-02-28 13:16:55.262257','7','PreprocessTask object (7)',1,'[{\"added\": {}}]',9,1),(14,'2020-02-28 13:50:43.887043','7','PreprocessTask object (7)',3,'',9,1),(15,'2020-02-28 13:51:00.704282','8','PreprocessTask object (8)',1,'[{\"added\": {}}]',9,1),(16,'2020-02-28 14:15:05.964572','9','PreprocessTask object (9)',1,'[{\"added\": {}}]',9,1),(17,'2020-02-28 14:21:28.445741','10','PreprocessTask object (10)',1,'[{\"added\": {}}]',9,1),(18,'2020-02-28 18:13:05.770728','11','PreprocessTask object (11)',1,'[{\"added\": {}}]',9,1),(19,'2020-02-28 18:17:57.389478','12','PreprocessTask object (12)',1,'[{\"added\": {}}]',9,1),(20,'2020-02-28 18:19:17.524685','13','PreprocessTask object (13)',1,'[{\"added\": {}}]',9,1),(21,'2020-02-29 16:51:35.953746','13','PreprocessTask object (13)',3,'',9,1),(22,'2020-02-29 16:51:35.963538','12','PreprocessTask object (12)',3,'',9,1),(23,'2020-02-29 16:51:35.964636','11','PreprocessTask object (11)',3,'',9,1),(24,'2020-02-29 16:52:25.353998','14','PreprocessTask object (14)',1,'[{\"added\": {}}]',9,1),(25,'2020-02-29 16:58:32.591552','14','PreprocessTask object (14)',3,'',9,1),(26,'2020-02-29 16:58:44.766487','15','PreprocessTask object (15)',1,'[{\"added\": {}}]',9,1),(27,'2020-03-02 19:32:06.185195','15','PreprocessTask object (15)',3,'',9,1),(28,'2020-03-02 19:32:20.388618','16','PreprocessTask object (16)',1,'[{\"added\": {}}]',9,1),(29,'2020-03-02 20:01:27.098410','16','PreprocessTask object (16)',3,'',9,1),(30,'2020-03-02 20:01:51.744893','17','PreprocessTask object (17)',1,'[{\"added\": {}}]',9,1),(31,'2020-03-02 20:08:01.940696','19','PreprocessTask object (19)',1,'[{\"added\": {}}]',9,1),(32,'2020-03-03 11:02:10.298351','20','PreprocessTask object (20)',1,'[{\"added\": {}}]',9,1),(33,'2020-03-03 11:20:46.728598','20','PreprocessTask object (20)',3,'',9,1),(34,'2020-03-03 11:22:00.382808','21','PreprocessTask object (21)',1,'[{\"added\": {}}]',9,1),(35,'2020-03-03 11:30:48.597617','22','PreprocessTask object (22)',1,'[{\"added\": {}}]',9,1),(36,'2020-03-03 11:42:59.488262','23','PreprocessTask object (23)',1,'[{\"added\": {}}]',9,1),(37,'2020-03-03 11:44:07.571361','24','PreprocessTask object (24)',1,'[{\"added\": {}}]',9,1),(38,'2020-03-03 11:48:00.759331','25','PreprocessTask object (25)',1,'[{\"added\": {}}]',9,1),(39,'2020-03-03 11:54:56.826198','26','PreprocessTask object (26)',1,'[{\"added\": {}}]',9,1),(40,'2020-03-03 11:55:43.767476','27','PreprocessTask object (27)',1,'[{\"added\": {}}]',9,1),(41,'2020-03-03 11:57:00.991766','28','PreprocessTask object (28)',1,'[{\"added\": {}}]',9,1),(42,'2020-03-03 11:58:27.121160','29','PreprocessTask object (29)',1,'[{\"added\": {}}]',9,1),(43,'2020-03-03 12:06:15.285071','30','PreprocessTask object (30)',1,'[{\"added\": {}}]',9,1),(44,'2020-03-03 12:13:13.924958','31','PreprocessTask object (31)',1,'[{\"added\": {}}]',9,1),(45,'2020-03-03 12:17:27.731791','32','PreprocessTask object (32)',1,'[{\"added\": {}}]',9,1),(46,'2020-03-03 13:47:41.409652','33','PreprocessTask object (33)',1,'[{\"added\": {}}]',9,1),(47,'2020-03-03 17:00:02.716410','33','PreprocessTask object (33)',3,'',9,1),(48,'2020-03-03 17:00:31.051718','34','PreprocessTask object (34)',1,'[{\"added\": {}}]',9,1),(49,'2020-03-03 17:17:09.229764','34','PreprocessTask object (34)',3,'',9,1),(50,'2020-03-03 17:17:20.110178','35','PreprocessTask object (35)',1,'[{\"added\": {}}]',9,1),(51,'2020-03-03 17:22:26.152676','35','PreprocessTask object (35)',3,'',9,1),(52,'2020-03-03 17:22:34.993458','36','PreprocessTask object (36)',1,'[{\"added\": {}}]',9,1),(53,'2020-03-03 18:12:17.256217','37','PreprocessTask object (37)',1,'[{\"added\": {}}]',9,1),(54,'2020-03-03 18:14:19.079648','38','PreprocessTask object (38)',1,'[{\"added\": {}}]',9,1),(55,'2020-03-03 18:20:54.148123','39','PreprocessTask object (39)',1,'[{\"added\": {}}]',9,1);
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
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(8,'App','book'),(7,'App','usermodel'),(3,'auth','group'),(2,'auth','permission'),(4,'auth','user'),(5,'contenttypes','contenttype'),(9,'preprocess','preprocesstask'),(6,'sessions','session');
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
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'App','0001_initial','2020-02-02 21:57:26.755089'),(2,'App','0002_auto_20180921_1605','2020-02-02 21:57:26.766641'),(3,'App','0003_auto_20180921_1606','2020-02-02 21:57:26.770825'),(4,'contenttypes','0001_initial','2020-02-02 21:57:26.798101'),(5,'auth','0001_initial','2020-02-02 21:57:27.045102'),(6,'admin','0001_initial','2020-02-02 21:57:27.093056'),(7,'admin','0002_logentry_remove_auto_add','2020-02-02 21:57:27.113729'),(8,'contenttypes','0002_remove_content_type_name','2020-02-02 21:57:27.168565'),(9,'auth','0002_alter_permission_name_max_length','2020-02-02 21:57:27.184280'),(10,'auth','0003_alter_user_email_max_length','2020-02-02 21:57:27.213988'),(11,'auth','0004_alter_user_username_opts','2020-02-02 21:57:27.228417'),(12,'auth','0005_alter_user_last_login_null','2020-02-02 21:57:27.251539'),(13,'auth','0006_require_contenttypes_0002','2020-02-02 21:57:27.254320'),(14,'auth','0007_alter_validators_add_error_messages','2020-02-02 21:57:27.262708'),(15,'auth','0008_alter_user_username_max_length','2020-02-02 21:57:27.285471'),(16,'sessions','0001_initial','2020-02-02 21:57:27.305951'),(17,'App','0004_usermodel_u_predict','2020-02-11 23:19:40.335820'),(18,'admin','0003_logentry_add_action_flag_choices','2020-02-19 18:00:40.437152'),(19,'auth','0009_alter_user_last_name_max_length','2020-02-19 18:00:40.495899'),(20,'auth','0010_alter_group_name_max_length','2020-02-19 18:00:40.521819'),(21,'auth','0011_update_proxy_permissions','2020-02-19 18:00:40.532858');
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
INSERT INTO `django_session` VALUES ('0e24le9dtep59gjebz6fsoai8alw66se','YmU2ZTQzNGE2NzBiMDY1YmMwN2YxNjYzNjQ5MWFhYzNjM2FlOWZkNTp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI5MmViY2I1MzA3MWNkMzAwMzA0ZGQwZGY2M2Y3ZTZkZTg2Y2NjOGJhIn0=','2020-03-12 09:44:27.940578'),('4cbfkektwlz624bobgcyblp149ji097f','YmU2ZTQzNGE2NzBiMDY1YmMwN2YxNjYzNjQ5MWFhYzNjM2FlOWZkNTp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI5MmViY2I1MzA3MWNkMzAwMzA0ZGQwZGY2M2Y3ZTZkZTg2Y2NjOGJhIn0=','2020-03-11 17:57:14.936551'),('7nfopbd7w45q7igxqgroy9y1auqpnqfv','YmU2ZTQzNGE2NzBiMDY1YmMwN2YxNjYzNjQ5MWFhYzNjM2FlOWZkNTp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI5MmViY2I1MzA3MWNkMzAwMzA0ZGQwZGY2M2Y3ZTZkZTg2Y2NjOGJhIn0=','2020-03-11 17:12:34.784755'),('8vzl5ozoh4t2pby18rafca2udffz2u9o','YmU2ZTQzNGE2NzBiMDY1YmMwN2YxNjYzNjQ5MWFhYzNjM2FlOWZkNTp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI5MmViY2I1MzA3MWNkMzAwMzA0ZGQwZGY2M2Y3ZTZkZTg2Y2NjOGJhIn0=','2020-03-11 11:13:22.282625'),('cr3ta0dme3zlubor6d752mdtv33hmdnq','YmU2ZTQzNGE2NzBiMDY1YmMwN2YxNjYzNjQ5MWFhYzNjM2FlOWZkNTp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI5MmViY2I1MzA3MWNkMzAwMzA0ZGQwZGY2M2Y3ZTZkZTg2Y2NjOGJhIn0=','2020-03-12 11:27:31.984831'),('cw6g5rldpfm5f0s8nw2bu2fgt702uhaf','YmU2ZTQzNGE2NzBiMDY1YmMwN2YxNjYzNjQ5MWFhYzNjM2FlOWZkNTp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI5MmViY2I1MzA3MWNkMzAwMzA0ZGQwZGY2M2Y3ZTZkZTg2Y2NjOGJhIn0=','2020-03-05 17:25:45.163593'),('d0ocijx3jnlshp5me5yaxe0myqddyuzd','YmU2ZTQzNGE2NzBiMDY1YmMwN2YxNjYzNjQ5MWFhYzNjM2FlOWZkNTp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI5MmViY2I1MzA3MWNkMzAwMzA0ZGQwZGY2M2Y3ZTZkZTg2Y2NjOGJhIn0=','2020-03-11 17:39:27.055170'),('g1d3bslgil1go45ffba9z4fy1rfcoxr7','YmU2ZTQzNGE2NzBiMDY1YmMwN2YxNjYzNjQ5MWFhYzNjM2FlOWZkNTp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI5MmViY2I1MzA3MWNkMzAwMzA0ZGQwZGY2M2Y3ZTZkZTg2Y2NjOGJhIn0=','2020-03-11 17:06:27.003034'),('kh545gigzm2uddyojdj5flbt197hz77c','YmU2ZTQzNGE2NzBiMDY1YmMwN2YxNjYzNjQ5MWFhYzNjM2FlOWZkNTp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI5MmViY2I1MzA3MWNkMzAwMzA0ZGQwZGY2M2Y3ZTZkZTg2Y2NjOGJhIn0=','2020-03-12 12:20:20.888920'),('tca3rgv2svb24asnns91gsuevi2skzyd','YmU2ZTQzNGE2NzBiMDY1YmMwN2YxNjYzNjQ5MWFhYzNjM2FlOWZkNTp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI5MmViY2I1MzA3MWNkMzAwMzA0ZGQwZGY2M2Y3ZTZkZTg2Y2NjOGJhIn0=','2020-03-04 18:10:19.147005'),('vgjirg87iv4zu5zl7fimfdgrm56v3s29','YmU2ZTQzNGE2NzBiMDY1YmMwN2YxNjYzNjQ5MWFhYzNjM2FlOWZkNTp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI5MmViY2I1MzA3MWNkMzAwMzA0ZGQwZGY2M2Y3ZTZkZTg2Y2NjOGJhIn0=','2020-03-11 16:37:06.846099');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `my_cache_table`
--

DROP TABLE IF EXISTS `my_cache_table`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `my_cache_table` (
  `cache_key` varchar(255) NOT NULL,
  `value` longtext NOT NULL,
  `expires` datetime(6) NOT NULL,
  PRIMARY KEY (`cache_key`),
  KEY `my_cache_table_expires` (`expires`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `my_cache_table`
--

LOCK TABLES `my_cache_table` WRITE;
/*!40000 ALTER TABLE `my_cache_table` DISABLE KEYS */;
INSERT INTO `my_cache_table` VALUES (':1:news','gASVygEAAAAAAABCwwEAADwhRE9DVFlQRSBodG1sPgo8aHRtbCBsYW5nPSJlbiI+CjxoZWFkPgogICAgPG1ldGEgY2hhcnNldD0iVVRGLTgiPgogICAgPHRpdGxlPm5ld3M8L3RpdGxlPgo8L2hlYWQ+Cjxib2R5Pgo8dWw+CiAgICAKICAgICAgICA8bGk+d2Ugd29uIDA8L2xpPgogICAgCiAgICAgICAgPGxpPndlIHdvbiAxPC9saT4KICAgIAogICAgICAgIDxsaT53ZSB3b24gMjwvbGk+CiAgICAKICAgICAgICA8bGk+d2Ugd29uIDM8L2xpPgogICAgCiAgICAgICAgPGxpPndlIHdvbiA0PC9saT4KICAgIAogICAgICAgIDxsaT53ZSB3b24gNTwvbGk+CiAgICAKICAgICAgICA8bGk+d2Ugd29uIDY8L2xpPgogICAgCiAgICAgICAgPGxpPndlIHdvbiA3PC9saT4KICAgIAogICAgICAgIDxsaT53ZSB3b24gODwvbGk+CiAgICAKICAgICAgICA8bGk+d2Ugd29uIDk8L2xpPgogICAgCgoKCgo8L3VsPgo8L2JvZHk+CjwvaHRtbD6ULg==','2020-02-13 12:45:36.000000');
/*!40000 ALTER TABLE `my_cache_table` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `preprocess_preprocessTask`
--

DROP TABLE IF EXISTS `preprocess_preprocessTask`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `preprocess_preprocessTask` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `begin` datetime DEFAULT NULL,
  `end` datetime DEFAULT NULL,
  `title` varchar(120) NOT NULL,
  `creator` varchar(45) DEFAULT NULL,
  `creation` datetime DEFAULT NULL,
  `modification` datetime DEFAULT NULL,
  `modifier` varchar(20) DEFAULT NULL,
  `description` longtext,
  `imageupload` varchar(100) DEFAULT NULL,
  `is_predict` tinyint(1) DEFAULT NULL,
  `imagepredict` varchar(100) DEFAULT NULL,
  `predict_result` int(11) DEFAULT NULL,
  `status` varchar(6) DEFAULT NULL,
  `is_confirm` tinyint(1) DEFAULT NULL,
  `imageresult` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=40 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `preprocess_preprocessTask`
--

LOCK TABLES `preprocess_preprocessTask` WRITE;
/*!40000 ALTER TABLE `preprocess_preprocessTask` DISABLE KEYS */;
INSERT INTO `preprocess_preprocessTask` VALUES (39,'2020-03-03 00:00:00','9999-12-31 00:00:00','final','admin','2020-03-03 18:20:54','2020-03-03 18:21:03',NULL,'','2020/03/icons/origin/final/dog1.jpg',1,'',1,'p',1,'2020/03/icons/result/final/dog1.jpg');
/*!40000 ALTER TABLE `preprocess_preprocessTask` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-03-14 11:07:39
