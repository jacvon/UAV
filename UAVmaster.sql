-- MySQL dump 10.13  Distrib 8.0.18, for macos10.14 (x86_64)
--
-- Host: localhost    Database: GP1ModelToSql
-- ------------------------------------------------------
-- Server version	5.7.29

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `App_usermodel`
--

LOCK TABLES `App_usermodel` WRITE;
/*!40000 ALTER TABLE `App_usermodel` DISABLE KEYS */;
/*!40000 ALTER TABLE `App_usermodel` ENABLE KEYS */;
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
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
INSERT INTO `auth_group_permissions` VALUES (1,1,45),(2,1,46),(3,1,47),(4,1,48),(5,1,49),(6,1,50),(7,1,51),(8,1,52);
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
) ENGINE=InnoDB AUTO_INCREMENT=97 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can add permission',2,'add_permission'),(5,'Can change permission',2,'change_permission'),(6,'Can delete permission',2,'delete_permission'),(7,'Can add group',3,'add_group'),(8,'Can change group',3,'change_group'),(9,'Can delete group',3,'delete_group'),(10,'Can add user',4,'add_user'),(11,'Can change user',4,'change_user'),(12,'Can delete user',4,'delete_user'),(13,'Can add content type',5,'add_contenttype'),(14,'Can change content type',5,'change_contenttype'),(15,'Can delete content type',5,'delete_contenttype'),(16,'Can add session',6,'add_session'),(17,'Can change session',6,'change_session'),(18,'Can delete session',6,'delete_session'),(19,'Can add user model',7,'add_usermodel'),(20,'Can change user model',7,'change_usermodel'),(21,'Can delete user model',7,'delete_usermodel'),(22,'Can add book',8,'add_book'),(23,'Can change book',8,'change_book'),(24,'Can delete book',8,'delete_book'),(25,'Can view log entry',1,'view_logentry'),(26,'Can view permission',2,'view_permission'),(27,'Can view group',3,'view_group'),(28,'Can view user',4,'view_user'),(29,'Can view content type',5,'view_contenttype'),(30,'Can view session',6,'view_session'),(31,'Can view book',8,'view_book'),(32,'Can view user model',7,'view_usermodel'),(45,'Can add 路线',12,'add_offlinemapmanage'),(46,'Can change 路线',12,'change_offlinemapmanage'),(47,'Can delete 路线',12,'delete_offlinemapmanage'),(48,'Can view 路线',12,'view_offlinemapmanage'),(49,'Can add 离线任务',13,'add_offlinetask'),(50,'Can change 离线任务',13,'change_offlinetask'),(51,'Can delete 离线任务',13,'delete_offlinetask'),(52,'Can view 离线任务',13,'view_offlinetask'),(53,'Can add 图片信息',14,'add_singleimageinfo'),(54,'Can change 图片信息',14,'change_singleimageinfo'),(55,'Can delete 图片信息',14,'delete_singleimageinfo'),(56,'Can view 图片信息',14,'view_singleimageinfo'),(57,'Can add crontab',15,'add_crontabschedule'),(58,'Can change crontab',15,'change_crontabschedule'),(59,'Can delete crontab',15,'delete_crontabschedule'),(60,'Can view crontab',15,'view_crontabschedule'),(61,'Can add periodic task',16,'add_periodictask'),(62,'Can change periodic task',16,'change_periodictask'),(63,'Can delete periodic task',16,'delete_periodictask'),(64,'Can view periodic task',16,'view_periodictask'),(65,'Can add interval',17,'add_intervalschedule'),(66,'Can change interval',17,'change_intervalschedule'),(67,'Can delete interval',17,'delete_intervalschedule'),(68,'Can view interval',17,'view_intervalschedule'),(69,'Can add periodic tasks',18,'add_periodictasks'),(70,'Can change periodic tasks',18,'change_periodictasks'),(71,'Can delete periodic tasks',18,'delete_periodictasks'),(72,'Can view periodic tasks',18,'view_periodictasks'),(73,'Can add task state',19,'add_taskmeta'),(74,'Can change task state',19,'change_taskmeta'),(75,'Can delete task state',19,'delete_taskmeta'),(76,'Can view task state',19,'view_taskmeta'),(77,'Can add saved group result',20,'add_tasksetmeta'),(78,'Can change saved group result',20,'change_tasksetmeta'),(79,'Can delete saved group result',20,'delete_tasksetmeta'),(80,'Can view saved group result',20,'view_tasksetmeta'),(81,'Can add worker',21,'add_workerstate'),(82,'Can change worker',21,'change_workerstate'),(83,'Can delete worker',21,'delete_workerstate'),(84,'Can view worker',21,'view_workerstate'),(85,'Can add task',22,'add_taskstate'),(86,'Can change task',22,'change_taskstate'),(87,'Can delete task',22,'delete_taskstate'),(88,'Can view task',22,'view_taskstate'),(89,'Can add 图片识别信息',23,'add_singleimageidentifyinfo'),(90,'Can change 图片识别信息',23,'change_singleimageidentifyinfo'),(91,'Can delete 图片识别信息',23,'delete_singleimageidentifyinfo'),(92,'Can view 图片识别信息',23,'view_singleimageidentifyinfo'),(93,'Can add 图片比对信息',24,'add_singleimagespliceinfo'),(94,'Can change 图片比对信息',24,'change_singleimagespliceinfo'),(95,'Can delete 图片比对信息',24,'delete_singleimagespliceinfo'),(96,'Can view 图片比对信息',24,'view_singleimagespliceinfo');
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
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$150000$vxycj84BT9F5$OvPgZkwOlvYtcQQLYLBhI4fiqn4Hpz+IaTrdpX/6qJw=','2020-05-12 15:34:09.553400',0,'admin','','','admin123@qq.com',1,1,'2020-02-19 18:07:04.751397'),(2,'pbkdf2_sha256$150000$HkSc06ys1C6h$gdCHXh3L0P9m8naU3KogTSxk7HbD8Ux/umHuW9hwYi8=',NULL,0,'test123','','','admin123@qq.com',0,1,'2020-02-20 17:11:29.276014');
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
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
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
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
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
) ENGINE=InnoDB AUTO_INCREMENT=256 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (201,'2020-04-17 11:07:07.218578','3','东区教学楼',1,'[{\"added\": {}}]',12,1),(202,'2020-04-17 11:07:14.021950','4','OfflineTask object (4)',1,'[{\"added\": {}}]',13,1),(203,'2020-04-17 11:21:03.477007','4','地库',1,'[{\"added\": {}}]',12,1),(204,'2020-04-17 11:21:09.115305','5','OfflineTask object (5)',1,'[{\"added\": {}}]',13,1),(205,'2020-04-17 11:22:12.961294','6','OfflineTask object (6)',1,'[{\"added\": {}}]',13,1),(206,'2020-04-17 15:06:37.961243','7','OfflineTask object (7)',1,'[{\"added\": {}}]',13,1),(207,'2020-04-21 11:29:36.206522','5','888',1,'[{\"added\": {}}]',12,1),(208,'2020-04-21 11:29:48.247064','2','新校区3',2,'[{\"changed\": {\"fields\": [\"mapNickName\"]}}]',12,1),(209,'2020-04-21 11:30:29.518593','2','新校区',2,'[{\"changed\": {\"fields\": [\"mapNickName\"]}}]',12,1),(210,'2020-04-27 16:44:06.362171','8','OfflineTask object (8)',1,'[{\"added\": {}}]',13,1),(211,'2020-04-27 16:49:58.144335','8','OfflineTask object (8)',3,'',13,1),(212,'2020-04-27 16:50:27.764917','9','OfflineTask object (9)',1,'[{\"added\": {}}]',13,1),(213,'2020-04-28 08:24:27.243287','9','OfflineTask object (9)',3,'',13,1),(214,'2020-04-28 08:33:10.864277','10','OfflineTask object (10)',1,'[{\"added\": {}}]',13,1),(215,'2020-04-28 08:40:28.845897','11','OfflineTask object (11)',1,'[{\"added\": {}}]',13,1),(216,'2020-04-28 08:44:34.351682','12','OfflineTask object (12)',1,'[{\"added\": {}}]',13,1),(217,'2020-04-28 08:48:02.117839','13','OfflineTask object (13)',1,'[{\"added\": {}}]',13,1),(218,'2020-04-28 09:06:11.005791','14','OfflineTask object (14)',1,'[{\"added\": {}}]',13,1),(219,'2020-04-28 14:49:58.805602','15','OfflineTask object (15)',1,'[{\"added\": {}}]',13,1),(220,'2020-04-28 14:53:24.340729','16','OfflineTask object (16)',1,'[{\"added\": {}}]',13,1),(221,'2020-04-28 14:58:16.145282','17','OfflineTask object (17)',1,'[{\"added\": {}}]',13,1),(222,'2020-04-28 14:59:22.352413','17','OfflineTask object (17)',3,'',13,1),(223,'2020-04-28 14:59:22.353607','16','OfflineTask object (16)',3,'',13,1),(224,'2020-04-28 14:59:22.355241','15','OfflineTask object (15)',3,'',13,1),(225,'2020-04-28 15:00:08.154270','18','OfflineTask object (18)',1,'[{\"added\": {}}]',13,1),(226,'2020-04-28 15:47:54.202152','18','OfflineTask object (18)',3,'',13,1),(227,'2020-04-28 15:49:01.245538','19','OfflineTask object (19)',1,'[{\"added\": {}}]',13,1),(228,'2020-04-28 15:51:01.911487','19','OfflineTask object (19)',3,'',13,1),(229,'2020-04-28 15:51:13.850197','20','OfflineTask object (20)',1,'[{\"added\": {}}]',13,1),(230,'2020-04-28 15:59:08.775293','20','OfflineTask object (20)',3,'',13,1),(231,'2020-04-28 15:59:19.274843','21','OfflineTask object (21)',1,'[{\"added\": {}}]',13,1),(232,'2020-04-28 16:02:34.650996','22','OfflineTask object (22)',1,'[{\"added\": {}}]',13,1),(233,'2020-04-28 16:04:36.012017','23','OfflineTask object (23)',1,'[{\"added\": {}}]',13,1),(234,'2020-04-28 16:08:52.693146','24','OfflineTask object (24)',1,'[{\"added\": {}}]',13,1),(235,'2020-04-28 16:11:08.624244','25','OfflineTask object (25)',1,'[{\"added\": {}}]',13,1),(236,'2020-04-28 16:14:03.392566','26','OfflineTask object (26)',1,'[{\"added\": {}}]',13,1),(237,'2020-04-28 16:15:24.976944','26','OfflineTask object (26)',3,'',13,1),(238,'2020-04-28 16:15:24.978035','25','OfflineTask object (25)',3,'',13,1),(239,'2020-04-28 16:15:24.979271','24','OfflineTask object (24)',3,'',13,1),(240,'2020-04-28 16:15:24.980299','23','OfflineTask object (23)',3,'',13,1),(241,'2020-04-28 16:15:24.981333','22','OfflineTask object (22)',3,'',13,1),(242,'2020-04-28 16:15:24.982879','21','OfflineTask object (21)',3,'',13,1),(243,'2020-04-28 16:15:43.745030','27','OfflineTask object (27)',1,'[{\"added\": {}}]',13,1),(244,'2020-04-28 16:25:39.691119','28','OfflineTask object (28)',1,'[{\"added\": {}}]',13,1),(245,'2020-04-28 16:26:58.277474','29','OfflineTask object (29)',1,'[{\"added\": {}}]',13,1),(246,'2020-04-28 16:30:34.857780','30','OfflineTask object (30)',1,'[{\"added\": {}}]',13,1),(247,'2020-04-28 16:32:54.934102','31','OfflineTask object (31)',1,'[{\"added\": {}}]',13,1),(248,'2020-04-28 16:45:17.773906','32','OfflineTask object (32)',1,'[{\"added\": {}}]',13,1),(249,'2020-04-28 16:49:05.356673','33','OfflineTask object (33)',1,'[{\"added\": {}}]',13,1),(250,'2020-04-30 09:42:19.901365','34','OfflineTask object (34)',1,'[{\"added\": {}}]',13,1),(251,'2020-05-09 10:47:09.823560','35','OfflineTask object (35)',1,'[{\"added\": {}}]',13,1),(252,'2020-05-12 15:37:32.690285','1','OfflineTask object (1)',1,'[{\"added\": {}}]',13,1),(253,'2020-05-12 15:40:12.501610','2','OfflineTask object (2)',1,'[{\"added\": {}}]',13,1),(254,'2020-05-12 15:45:20.714412','2','OfflineTask object (2)',3,'',13,1),(255,'2020-05-12 15:45:41.098547','3','OfflineTask object (3)',1,'[{\"added\": {}}]',13,1);
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
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(8,'App','book'),(7,'App','usermodel'),(3,'auth','group'),(2,'auth','permission'),(4,'auth','user'),(5,'contenttypes','contenttype'),(15,'djcelery','crontabschedule'),(17,'djcelery','intervalschedule'),(16,'djcelery','periodictask'),(18,'djcelery','periodictasks'),(19,'djcelery','taskmeta'),(20,'djcelery','tasksetmeta'),(22,'djcelery','taskstate'),(21,'djcelery','workerstate'),(12,'offlineTask','offlinemapmanage'),(13,'offlineTask','offlinetask'),(23,'offlineTask','singleimageidentifyinfo'),(14,'offlineTask','singleimageinfo'),(24,'offlineTask','singleimagespliceinfo'),(6,'sessions','session');
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
) ENGINE=InnoDB AUTO_INCREMENT=43 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'App','0001_initial','2020-02-02 21:57:26.755089'),(2,'App','0002_auto_20180921_1605','2020-02-02 21:57:26.766641'),(3,'App','0003_auto_20180921_1606','2020-02-02 21:57:26.770825'),(4,'contenttypes','0001_initial','2020-02-02 21:57:26.798101'),(5,'auth','0001_initial','2020-02-02 21:57:27.045102'),(6,'admin','0001_initial','2020-02-02 21:57:27.093056'),(7,'admin','0002_logentry_remove_auto_add','2020-02-02 21:57:27.113729'),(8,'contenttypes','0002_remove_content_type_name','2020-02-02 21:57:27.168565'),(9,'auth','0002_alter_permission_name_max_length','2020-02-02 21:57:27.184280'),(10,'auth','0003_alter_user_email_max_length','2020-02-02 21:57:27.213988'),(11,'auth','0004_alter_user_username_opts','2020-02-02 21:57:27.228417'),(12,'auth','0005_alter_user_last_login_null','2020-02-02 21:57:27.251539'),(13,'auth','0006_require_contenttypes_0002','2020-02-02 21:57:27.254320'),(14,'auth','0007_alter_validators_add_error_messages','2020-02-02 21:57:27.262708'),(15,'auth','0008_alter_user_username_max_length','2020-02-02 21:57:27.285471'),(16,'sessions','0001_initial','2020-02-02 21:57:27.305951'),(17,'App','0004_usermodel_u_predict','2020-02-11 23:19:40.335820'),(18,'admin','0003_logentry_add_action_flag_choices','2020-02-19 18:00:40.437152'),(19,'auth','0009_alter_user_last_name_max_length','2020-02-19 18:00:40.495899'),(20,'auth','0010_alter_group_name_max_length','2020-02-19 18:00:40.521819'),(21,'auth','0011_update_proxy_permissions','2020-02-19 18:00:40.532858'),(22,'preprocess','0001_initial','2020-04-16 14:49:21.215682'),(23,'preprocess','0002_auto_20200416_1131','2020-04-16 14:49:21.313222'),(24,'preprocess','0003_auto_20200416_1140','2020-04-16 14:49:21.398877'),(25,'preprocess','0004_auto_20200416_1447','2020-04-16 15:05:33.900203'),(26,'preprocess','0005_auto_20200416_1500','2020-04-16 15:12:51.567878'),(27,'preprocess','0006_auto_20200416_1501','2020-04-16 15:12:51.572155'),(28,'preprocess','0007_auto_20200416_1504','2020-04-16 15:12:51.578401'),(29,'preprocess','0008_auto_20200416_1510','2020-04-16 15:12:51.583673'),(30,'preprocess','0009_auto_20200416_1522','2020-04-16 15:22:14.134281'),(31,'preprocess','0010_auto_20200416_1532','2020-04-16 15:32:03.951498'),(32,'preprocess','0011_auto_20200416_1533','2020-04-16 15:33:29.132377'),(33,'preprocess','0012_remove_singleimageinfo_title','2020-04-16 16:28:43.173928'),(34,'preprocess','0013_singleimageinfo_title','2020-04-16 16:32:36.869012'),(35,'preprocess','0014_auto_20200416_1650','2020-04-16 16:50:38.277717'),(36,'preprocess','0015_auto_20200416_1652','2020-04-16 16:52:20.667496'),(37,'preprocess','0016_auto_20200416_1653','2020-04-16 16:53:12.644307'),(38,'preprocess','0017_auto_20200416_1654','2020-04-16 16:54:58.440280'),(39,'preprocess','0018_auto_20200417_1028','2020-04-17 10:29:15.679708'),(40,'offlineTask','0001_initial','2020-04-17 10:34:40.776466'),(41,'djcelery','0001_initial','2020-04-28 15:10:33.584113'),(42,'offlineTask','0002_singleimageidentifyinfo_singleimagespliceinfo','2020-04-28 15:12:22.595977');
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
INSERT INTO `django_session` VALUES ('0e24le9dtep59gjebz6fsoai8alw66se','YmU2ZTQzNGE2NzBiMDY1YmMwN2YxNjYzNjQ5MWFhYzNjM2FlOWZkNTp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI5MmViY2I1MzA3MWNkMzAwMzA0ZGQwZGY2M2Y3ZTZkZTg2Y2NjOGJhIn0=','2020-03-12 09:44:27.940578'),('4cbfkektwlz624bobgcyblp149ji097f','YmU2ZTQzNGE2NzBiMDY1YmMwN2YxNjYzNjQ5MWFhYzNjM2FlOWZkNTp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI5MmViY2I1MzA3MWNkMzAwMzA0ZGQwZGY2M2Y3ZTZkZTg2Y2NjOGJhIn0=','2020-03-11 17:57:14.936551'),('7nfopbd7w45q7igxqgroy9y1auqpnqfv','YmU2ZTQzNGE2NzBiMDY1YmMwN2YxNjYzNjQ5MWFhYzNjM2FlOWZkNTp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI5MmViY2I1MzA3MWNkMzAwMzA0ZGQwZGY2M2Y3ZTZkZTg2Y2NjOGJhIn0=','2020-03-11 17:12:34.784755'),('8vzl5ozoh4t2pby18rafca2udffz2u9o','YmU2ZTQzNGE2NzBiMDY1YmMwN2YxNjYzNjQ5MWFhYzNjM2FlOWZkNTp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI5MmViY2I1MzA3MWNkMzAwMzA0ZGQwZGY2M2Y3ZTZkZTg2Y2NjOGJhIn0=','2020-03-11 11:13:22.282625'),('ahg7yqvbavl2vtnisyyz1pdk92vagawe','YmU2ZTQzNGE2NzBiMDY1YmMwN2YxNjYzNjQ5MWFhYzNjM2FlOWZkNTp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI5MmViY2I1MzA3MWNkMzAwMzA0ZGQwZGY2M2Y3ZTZkZTg2Y2NjOGJhIn0=','2020-04-01 14:55:54.324872'),('cr3ta0dme3zlubor6d752mdtv33hmdnq','YmU2ZTQzNGE2NzBiMDY1YmMwN2YxNjYzNjQ5MWFhYzNjM2FlOWZkNTp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI5MmViY2I1MzA3MWNkMzAwMzA0ZGQwZGY2M2Y3ZTZkZTg2Y2NjOGJhIn0=','2020-03-12 11:27:31.984831'),('cw6g5rldpfm5f0s8nw2bu2fgt702uhaf','YmU2ZTQzNGE2NzBiMDY1YmMwN2YxNjYzNjQ5MWFhYzNjM2FlOWZkNTp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI5MmViY2I1MzA3MWNkMzAwMzA0ZGQwZGY2M2Y3ZTZkZTg2Y2NjOGJhIn0=','2020-03-05 17:25:45.163593'),('cysxibwhkz4b6e6yg2sebys4msixz0r3','YmU2ZTQzNGE2NzBiMDY1YmMwN2YxNjYzNjQ5MWFhYzNjM2FlOWZkNTp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI5MmViY2I1MzA3MWNkMzAwMzA0ZGQwZGY2M2Y3ZTZkZTg2Y2NjOGJhIn0=','2020-04-24 09:18:01.213920'),('d0ocijx3jnlshp5me5yaxe0myqddyuzd','YmU2ZTQzNGE2NzBiMDY1YmMwN2YxNjYzNjQ5MWFhYzNjM2FlOWZkNTp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI5MmViY2I1MzA3MWNkMzAwMzA0ZGQwZGY2M2Y3ZTZkZTg2Y2NjOGJhIn0=','2020-03-11 17:39:27.055170'),('e9bwl9gkrdkdvxzri8nhipkizyzssgib','YmU2ZTQzNGE2NzBiMDY1YmMwN2YxNjYzNjQ5MWFhYzNjM2FlOWZkNTp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI5MmViY2I1MzA3MWNkMzAwMzA0ZGQwZGY2M2Y3ZTZkZTg2Y2NjOGJhIn0=','2020-05-26 15:34:09.557851'),('g1d3bslgil1go45ffba9z4fy1rfcoxr7','YmU2ZTQzNGE2NzBiMDY1YmMwN2YxNjYzNjQ5MWFhYzNjM2FlOWZkNTp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI5MmViY2I1MzA3MWNkMzAwMzA0ZGQwZGY2M2Y3ZTZkZTg2Y2NjOGJhIn0=','2020-03-11 17:06:27.003034'),('kh545gigzm2uddyojdj5flbt197hz77c','YmU2ZTQzNGE2NzBiMDY1YmMwN2YxNjYzNjQ5MWFhYzNjM2FlOWZkNTp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI5MmViY2I1MzA3MWNkMzAwMzA0ZGQwZGY2M2Y3ZTZkZTg2Y2NjOGJhIn0=','2020-03-12 12:20:20.888920'),('t0fdt9pbmsbnowmcole3gdp9ececo9b1','YmU2ZTQzNGE2NzBiMDY1YmMwN2YxNjYzNjQ5MWFhYzNjM2FlOWZkNTp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI5MmViY2I1MzA3MWNkMzAwMzA0ZGQwZGY2M2Y3ZTZkZTg2Y2NjOGJhIn0=','2020-05-11 11:23:59.561884'),('tca3rgv2svb24asnns91gsuevi2skzyd','YmU2ZTQzNGE2NzBiMDY1YmMwN2YxNjYzNjQ5MWFhYzNjM2FlOWZkNTp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI5MmViY2I1MzA3MWNkMzAwMzA0ZGQwZGY2M2Y3ZTZkZTg2Y2NjOGJhIn0=','2020-03-04 18:10:19.147005'),('vgjirg87iv4zu5zl7fimfdgrm56v3s29','YmU2ZTQzNGE2NzBiMDY1YmMwN2YxNjYzNjQ5MWFhYzNjM2FlOWZkNTp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI5MmViY2I1MzA3MWNkMzAwMzA0ZGQwZGY2M2Y3ZTZkZTg2Y2NjOGJhIn0=','2020-03-11 16:37:06.846099'),('yk38dpkqoomfxaj0b28qf1k2r3m7ilbq','YmU2ZTQzNGE2NzBiMDY1YmMwN2YxNjYzNjQ5MWFhYzNjM2FlOWZkNTp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI5MmViY2I1MzA3MWNkMzAwMzA0ZGQwZGY2M2Y3ZTZkZTg2Y2NjOGJhIn0=','2020-03-31 15:38:28.881852');
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
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
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
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
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
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
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
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
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
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
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
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `djcelery_workerstate`
--

LOCK TABLES `djcelery_workerstate` WRITE;
/*!40000 ALTER TABLE `djcelery_workerstate` DISABLE KEYS */;
/*!40000 ALTER TABLE `djcelery_workerstate` ENABLE KEYS */;
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
-- Table structure for table `offlineTask_offlinemapmanage`
--

DROP TABLE IF EXISTS `offlineTask_offlinemapmanage`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `offlineTask_offlinemapmanage` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `addTime` datetime(6) DEFAULT NULL,
  `mapNickName` varchar(100) CHARACTER SET utf8 NOT NULL,
  `mapDescription` longtext CHARACTER SET utf8,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `offlineTask_offlinemapmanage`
--

LOCK TABLES `offlineTask_offlinemapmanage` WRITE;
/*!40000 ALTER TABLE `offlineTask_offlinemapmanage` DISABLE KEYS */;
INSERT INTO `offlineTask_offlinemapmanage` VALUES (1,'2020-04-17 10:42:47.830992','离线测试西食堂',''),(2,'2020-04-21 11:30:29.517650','新校区',''),(3,'2020-04-17 11:07:07.217554','东区教学楼','在东区教学楼逆时针分一圈'),(4,'2020-04-17 11:21:03.476137','地库','来一圈'),(5,'2020-04-21 11:29:36.205587','888','说是');
/*!40000 ALTER TABLE `offlineTask_offlinemapmanage` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `offlineTask_offlinetask`
--

DROP TABLE IF EXISTS `offlineTask_offlinetask`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `offlineTask_offlinetask` (
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
  `folderOriginPath` varchar(10000) CHARACTER SET utf8 NOT NULL,
  `imagesOriginPathList` varchar(10000) CHARACTER SET utf8 NOT NULL,
  `overDate` varchar(45) NOT NULL,
  `title_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `offlineTask_offlinet_title_id_af2a5e9e_fk_offlineTa` (`title_id`),
  CONSTRAINT `offlineTask_offlinet_title_id_af2a5e9e_fk_offlineTa` FOREIGN KEY (`title_id`) REFERENCES `offlineTask_offlinemapmanage` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `offlineTask_offlinetask`
--

LOCK TABLES `offlineTask_offlinetask` WRITE;
/*!40000 ALTER TABLE `offlineTask_offlinetask` DISABLE KEYS */;
INSERT INTO `offlineTask_offlinetask` VALUES (3,'2020-05-12 15:45:41.037974','9999-12-31','admin',NULL,'2020-05-12 15:45:41.096973','2020-05-12 15:45:41.096991','','p','p','p','u','新校区/20200512/154541/origin/','[\'新校区/20200512/154541/origin/667f8fb7-0b2b-46e1-8da6-8433f5ca4672.JPG\', \'新校区/20200512/154541/origin/3955b227-f2c4-4152-95dc-c86b98ab8670.JPG\', \'新校区/20200512/154541/origin/3a60cd48-4dd1-4a0e-bedb-6a836a61ae34.JPG\', \'新校区/20200512/154541/origin/0e7c82aa-88ba-439c-b3b2-64653bfd5092.JPG\', \'新校区/20200512/154541/origin/5ac0bd97-6df7-4a5b-9578-7b120104d5bc.JPG\', \'新校区/20200512/154541/origin/e261c765-a6da-477b-bc61-a1031d9f18ae.JPG\', \'新校区/20200512/154541/origin/744daac5-59df-40e6-a416-a9e741217ad6.JPG\', \'新校区/20200512/154541/origin/24911e47-78f2-4244-9c36-53052728601b.JPG\', \'新校区/20200512/154541/origin/6103bea3-3ea4-4ed6-9a0b-66cda63185b4.JPG\', \'新校区/20200512/154541/origin/26154837-920b-4e1c-9f02-e3799b867882.JPG\', \'新校区/20200512/154541/origin/3bb1ce17-e563-46e6-a3cd-50cfb47c51a6.JPG\', \'新校区/20200512/154541/origin/47ceabb4-45e0-42b6-8788-1552c7303c72.JPG\', \'新校区/20200512/154541/origin/91b956e0-a171-4c75-b82c-a8dd1b235cbc.JPG\', \'新校区/20200512/154541/origin/2f0c0450-8e4c-4ff5-84f2-51f57bf592a4.JPG\', \'新校区/20200512/154541/origin/2193022d-80b6-44cb-99e6-55a7cb09f116.JPG\', \'新校区/20200512/154541/origin/ec829701-ef68-4a0e-9446-712a9ed81a73.JPG\', \'新校区/20200512/154541/origin/917e1a2c-ce79-40a4-a2cc-4ad95b3487e6.JPG\', \'新校区/20200512/154541/origin/a15d68a4-5aec-420b-8719-d0e85b2f257f.JPG\', \'新校区/20200512/154541/origin/36f1ae19-038d-436d-bb21-fb57c8789cb3.JPG\', \'新校区/20200512/154541/origin/5819b01a-4c50-45d8-93d4-6be6ca1cd961.JPG\', \'新校区/20200512/154541/origin/e258cc19-b41a-4c12-9f31-34ce69f6c290.JPG\', \'新校区/20200512/154541/origin/1dc8dbe2-8f90-4f19-b488-291a270bc7ce.JPG\', \'新校区/20200512/154541/origin/c731ef4f-004d-4d31-8d1f-fc5828c8dc83.JPG\', \'新校区/20200512/154541/origin/2096c4dc-e0e7-44c4-8486-d3bf4443a99a.JPG\', \'新校区/20200512/154541/origin/52a41e62-5c7a-4357-a3ed-92e765596c03.JPG\', \'新校区/20200512/154541/origin/99fd89db-94f4-48f4-b148-633405614897.JPG\', \'新校区/20200512/154541/origin/f7463a16-4164-4b23-9c90-ddbb80d772d5.JPG\', \'新校区/20200512/154541/origin/23ce7ebf-ac18-4126-adc2-448ea11e0746.JPG\', \'新校区/20200512/154541/origin/8a9a79f6-dd67-4b70-b7b1-10926b96739f.JPG\', \'新校区/20200512/154541/origin/685f5b1a-310a-4017-ad86-30827c2b8f21.JPG\', \'新校区/20200512/154541/origin/afdf7a10-aad4-44af-9908-88684d056739.JPG\', \'新校区/20200512/154541/origin/260a8b0e-292d-4585-bca1-d507a9e61640.JPG\', \'新校区/20200512/154541/origin/2bb626d7-3174-4b1a-879d-05f9f6458b14.JPG\', \'新校区/20200512/154541/origin/2414c8e5-4772-4140-adab-ce970f1c650a.JPG\', \'新校区/20200512/154541/origin/ceadb11f-cc47-4352-9b4a-e5eff8613e9b.JPG\', \'新校区/20200512/154541/origin/92bbfe09-8560-4e1a-908e-59fcfaf6372c.JPG\', \'新校区/20200512/154541/origin/7c64d259-2348-4ed2-a2ac-3e87e4021b36.JPG\', \'新校区/20200512/154541/origin/33fd4b6e-dcf7-4efb-9681-b336bbe995bf.JPG\', \'新校区/20200512/154541/origin/5153ba9f-0ac6-4d02-a123-18211bf352f5.JPG\', \'新校区/20200512/154541/origin/5a382853-e3a5-4d00-98ad-83ba7b769b0c.JPG\', \'新校区/20200512/154541/origin/648d54c5-9805-45cf-b36f-754a335da57d.JPG\', \'新校区/20200512/154541/origin/11bc6a91-60d9-46cc-b0f8-ce6eb1bc218a.JPG\', \'新校区/20200512/154541/origin/45e17ca3-2930-4f24-afa4-422bcf9ff81f.JPG\', \'新校区/20200512/154541/origin/dea822a5-9424-4a91-9726-0508371d0ab3.JPG\', \'新校区/20200512/154541/origin/aa672216-eec5-4c03-83d7-a6ab3eeeab71.JPG\', \'新校区/20200512/154541/origin/3adcd319-ff6b-4755-9ff3-fc5eb233bf37.JPG\', \'新校区/20200512/154541/origin/7824cee4-5b0d-4b52-8039-731681db689e.JPG\', \'新校区/20200512/154541/origin/1d1d7ce1-fb02-49f3-8a8a-c8fafd6a246e.JPG\', \'新校区/20200512/154541/origin/ce91b47e-5a35-4abf-80dc-2a041ccc4153.JPG\', \'新校区/20200512/154541/origin/b026b335-a6d9-4588-bdc4-e96c64167566.JPG\', \'新校区/20200512/154541/origin/a83d945f-6fb5-4432-8370-35d83756be37.JPG\', \'新校区/20200512/154541/origin/396374c5-18f4-4bc3-b2a6-fdc8cc7ca0c7.JPG\', \'新校区/20200512/154541/origin/adcfff8c-706a-48ba-9b54-aa3e88ff7d51.JPG\', \'新校区/20200512/154541/origin/7227e1ef-0b5a-439a-a9aa-19df656ba691.JPG\', \'新校区/20200512/154541/origin/375da0a1-3770-4d01-983e-1f3ba52e7b11.JPG\', \'新校区/20200512/154541/origin/f16a1fea-a7c3-40b5-831f-410ef8f410a3.JPG\', \'新校区/20200512/154541/origin/8d65f9b6-1169-41c0-aa0d-9701c987e30e.JPG\', \'新校区/20200512/154541/origin/598d1a16-051b-4f70-9f9a-301728cdb345.JPG\', \'新校区/20200512/154541/origin/382e64c0-e4a2-4d9a-93b9-74be3a46ea78.JPG\', \'新校区/20200512/154541/origin/c0b4ae68-d8dd-4a16-b0ed-728f6fec8b83.JPG\', \'新校区/20200512/154541/origin/ec0227b5-9dbe-48ea-90a8-0c4b9c85c43b.JPG\', \'新校区/20200512/154541/origin/08996982-e188-4cdd-b977-e91b1df1b5d6.JPG\']','20200512/154541',2);
/*!40000 ALTER TABLE `offlineTask_offlinetask` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `offlineTask_singleimageidentifyinfo`
--

DROP TABLE IF EXISTS `offlineTask_singleimageidentifyinfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `offlineTask_singleimageidentifyinfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(120) CHARACTER SET utf8 NOT NULL,
  `singleImageId` int(11) NOT NULL,
  `is_confirm` tinyint(1) DEFAULT NULL,
  `is_identify` tinyint(1) NOT NULL,
  `is_show` tinyint(1) NOT NULL,
  `imagePreprocessPath` varchar(1000) CHARACTER SET utf8 NOT NULL,
  `imageIdentifyPath` varchar(1000) CHARACTER SET utf8 NOT NULL,
  `imageIdentifyResultPath` varchar(1000) CHARACTER SET utf8 NOT NULL,
  `overDate` varchar(45) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `offlineTask_singleimageidentifyinfo`
--

LOCK TABLES `offlineTask_singleimageidentifyinfo` WRITE;
/*!40000 ALTER TABLE `offlineTask_singleimageidentifyinfo` DISABLE KEYS */;
/*!40000 ALTER TABLE `offlineTask_singleimageidentifyinfo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `offlineTask_singleimageinfo`
--

DROP TABLE IF EXISTS `offlineTask_singleimageinfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `offlineTask_singleimageinfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `begin` datetime(6) DEFAULT NULL,
  `end` date DEFAULT NULL,
  `creator` varchar(20) DEFAULT NULL,
  `modifier` varchar(20) DEFAULT NULL,
  `creation` datetime(6) DEFAULT NULL,
  `modification` datetime(6) DEFAULT NULL,
  `title` varchar(120) CHARACTER SET utf8 NOT NULL,
  `is_show` tinyint(1) NOT NULL,
  `imageOriginPath` varchar(1000) CHARACTER SET utf8 NOT NULL,
  `imagePreprocessPath` varchar(1000) CHARACTER SET utf8 NOT NULL,
  `overDate` varchar(45) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `offlineTask_singleimageinfo`
--

LOCK TABLES `offlineTask_singleimageinfo` WRITE;
/*!40000 ALTER TABLE `offlineTask_singleimageinfo` DISABLE KEYS */;
/*!40000 ALTER TABLE `offlineTask_singleimageinfo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `offlineTask_singleimagespliceinfo`
--

DROP TABLE IF EXISTS `offlineTask_singleimagespliceinfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `offlineTask_singleimagespliceinfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(120) CHARACTER SET utf8 NOT NULL,
  `singleImageId` int(11) NOT NULL,
  `is_splice` tinyint(1) NOT NULL,
  `imagePreprocessPath` varchar(1000) CHARACTER SET utf8 NOT NULL,
  `imageSplicePath` varchar(1000) CHARACTER SET utf8 NOT NULL,
  `overDate` varchar(45) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `offlineTask_singleimagespliceinfo`
--

LOCK TABLES `offlineTask_singleimagespliceinfo` WRITE;
/*!40000 ALTER TABLE `offlineTask_singleimagespliceinfo` DISABLE KEYS */;
/*!40000 ALTER TABLE `offlineTask_singleimagespliceinfo` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-05-12 16:44:51
