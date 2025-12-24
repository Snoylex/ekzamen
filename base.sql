CREATE DATABASE  IF NOT EXISTS `georgian_restaurant` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `georgian_restaurant`;
-- MySQL dump 10.13  Distrib 8.0.43, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: georgian_restaurant
-- ------------------------------------------------------
-- Server version	8.0.40

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
-- Table structure for table `categories`
--

DROP TABLE IF EXISTS `categories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `categories` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `categories`
--

LOCK TABLES `categories` WRITE;
/*!40000 ALTER TABLE `categories` DISABLE KEYS */;
INSERT INTO `categories` VALUES (1,'Алкоголь'),(9,'Гарниры'),(2,'Горячие блюда'),(6,'Десерты'),(7,'Напитки'),(3,'Салаты'),(5,'Супы'),(8,'Хлеб и выпечка'),(4,'Холодные закуски');
/*!40000 ALTER TABLE `categories` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dishes`
--

DROP TABLE IF EXISTS `dishes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dishes` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `price` decimal(10,2) NOT NULL,
  `description` text COLLATE utf8mb4_unicode_ci,
  `image_path` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `category_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `category_id` (`category_id`),
  CONSTRAINT `dishes_ibfk_1` FOREIGN KEY (`category_id`) REFERENCES `categories` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dishes`
--

LOCK TABLES `dishes` WRITE;
/*!40000 ALTER TABLE `dishes` DISABLE KEYS */;
INSERT INTO `dishes` VALUES (1,'Вино красное (0.75л)',1500.00,'Грузинское красное сухое вино Саперави','images/wine_red.jpg',1),(2,'Вино белое (0.75л)',1200.00,'Грузинское белое полусладкое Ркацители','images/wine_white.jpg',1),(3,'Чача (0.5л)',800.00,'Грузинский самогон из винограда','images/chacha.jpg',1),(4,'Хачапури по-аджарски',450.00,'Лодочка из теста с сыром, яйцом и маслом','images/khachapuri.jpg',2),(5,'Хинкали (5 шт)',500.00,'Сочные пельмени с мясом и бульоном','images/khinkali.jpg',2),(6,'Шашлык из баранины',750.00,'Нежное мясо на углях с кавказскими специями','images/shashlyk.jpg',2),(7,'Грузинский салат',300.00,'С помидорами, огурцами, орехами и специями','images/georgian_salad.jpg',3),(8,'Салат с баклажанами',350.00,'Запечённые баклажаны с орехами','images/eggplant_salad.jpg',3),(9,'Пхали ассорти',350.00,'Овощные паштеты из шпината, свёклы и фасоли','images/phali.jpg',4),(10,'Сыры ассорти',400.00,'Грузинские сыры с мёдом','images/cheese_plate.jpg',4),(11,'Харчо',300.00,'Острый суп с говядиной и рисом','images/kharcho.jpg',5),(12,'Чихиртма',280.00,'Куриный суп с яйцом и зеленью','images/chikhirtma.jpg',5),(13,'Чурчхела',200.00,'Ореховая конфета в виноградном соке','images/churchkhela.jpg',6),(14,'Гозинаки',250.00,'Орехи в меду','images/gozinaki.jpg',6),(15,'Лимонад Тархун',150.00,'Грузинский газированный лимонад','images/tarkhun.jpg',7),(16,'Минеральная вода Боржоми (0.5л)',100.00,'Газированная','images/borjomi.jpg',7),(17,'Лаваш',100.00,'Свежий грузинский хлеб','images/lavash.jpg',8),(18,'Пури',120.00,'Традиционный грузинский хлеб','images/puri.jpg',8),(19,'Картофель по-деревенски',200.00,'Запечённый с травами','images/potato.jpg',9),(20,'Рис с овощами',180.00,'Ароматный рис','images/rice.jpg',9);
/*!40000 ALTER TABLE `dishes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reviews`
--

DROP TABLE IF EXISTS `reviews`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `reviews` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `rating` int NOT NULL,
  `text` text COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `reviews_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  CONSTRAINT `reviews_chk_1` CHECK ((`rating` between 1 and 5))
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reviews`
--

LOCK TABLES `reviews` WRITE;
/*!40000 ALTER TABLE `reviews` DISABLE KEYS */;
INSERT INTO `reviews` VALUES (1,1,5,'их чача огонь!','2025-12-22 10:10:54'),(7,1,5,'ыаыцувкеанпгршщзд','2025-12-23 18:06:26'),(8,3,5,'Вай-вай какой щикарный кухня. ','2025-12-23 19:13:43');
/*!40000 ALTER TABLE `reviews` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `password_hash` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `registered_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `is_admin` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'вася','asfdjs@gmail.com','scrypt:32768:8:1$6wtLAZYz40BazW87$31cc519d321a0f8a62c852fc97da002087485b88941dfccc2ec5cc2c2f53e59e4d08271c52f981e86ccdb3068a13c6d186d149bbd2f98ae0326b44fcfaeea667','2025-12-22 10:10:01',0),(2,'admin','admin@gmail.com','scrypt:32768:8:1$uumpc1goZzCrWhsG$9ac00de616e3e029373bb3fa15d991f3b0c05986005294d49440e034da567f15b9298f4eea5749154627ec42e52900bf12743ae974e92fefe4bed38a0451fba1','2025-12-23 15:35:52',1),(3,'Гога','gogatop@gmail.com','scrypt:32768:8:1$PpfNwuuKljZG5ruF$585e021f1d56da6a1742132cbcb9cc287053275e46544593de394f27092e540d3159c275a1c3ee64d635278f29c36d44a573dee23822014b65fc2fc026d09315','2025-12-23 19:12:49',0);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping events for database 'georgian_restaurant'
--

--
-- Dumping routines for database 'georgian_restaurant'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-12-24 13:50:08
