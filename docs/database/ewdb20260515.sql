
/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- 傾印 ewdb3 的資料庫結構
CREATE DATABASE IF NOT EXISTS `ewdb3` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci */;
USE `ewdb3`;

-- 傾印  資料表 ewdb3.aps_quantity 結構
CREATE TABLE IF NOT EXISTS `aps_quantity` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `no` varchar(60) NOT NULL,
  `product_order_no` varchar(60) NOT NULL,
  `oneProcess` int(11) NOT NULL,
  `secProcess` int(11) NOT NULL,
  `item_no` varchar(60) NOT NULL,
  `item_name` varchar(60) DEFAULT NULL,
  `itemCategory` int(11) DEFAULT NULL,
  `unit` int(11) DEFAULT NULL,
  `amount` float DEFAULT NULL,
  `minutes` int(11) DEFAULT NULL,
  `laborCount` int(11) DEFAULT NULL,
  `creationTime` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `product_order_no` (`product_order_no`,`oneProcess`,`secProcess`,`item_no`,`no`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=DYNAMIC;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb3.aps_quantity_item 結構
CREATE TABLE IF NOT EXISTS `aps_quantity_item` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `product_order_no` varchar(60) NOT NULL,
  `output_item_no` varchar(60) NOT NULL,
  `oneProcess` int(11) NOT NULL,
  `secProcess` int(11) NOT NULL,
  `item_no` varchar(60) NOT NULL,
  `item_name` varchar(60) DEFAULT NULL,
  `itemCategory` int(11) DEFAULT NULL,
  `unit` int(11) DEFAULT NULL,
  `count` float DEFAULT NULL,
  `creationTime` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `product_order_no` (`product_order_no`,`output_item_no`,`oneProcess`,`secProcess`,`item_no`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=DYNAMIC;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb3.bank_account 結構
CREATE TABLE IF NOT EXISTS `bank_account` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `displayName` varchar(60) DEFAULT NULL,
  `name` varchar(60) DEFAULT NULL,
  `branch` varchar(60) DEFAULT NULL,
  `account` varchar(60) DEFAULT NULL,
  `number` varchar(60) NOT NULL,
  `creationTime` int(11) DEFAULT NULL,
  `category` int(11) DEFAULT NULL,
  `currency` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `number` (`number`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb3.batchno_serialno 結構
CREATE TABLE IF NOT EXISTS `batchno_serialno` (
  `batch_number` varchar(60) NOT NULL,
  `serialNo` varchar(60) NOT NULL DEFAULT '',
  `ref_order_no_category` int(11) DEFAULT NULL,
  `ref_order_no` varchar(60) NOT NULL DEFAULT '',
  `warehouse_no` varchar(60) DEFAULT NULL,
  `time` int(11) DEFAULT NULL,
  `unit` int(11) DEFAULT NULL,
  `count` float DEFAULT NULL,
  `expectedCount` float DEFAULT 0,
  `validDate` int(11) DEFAULT NULL,
  `updatedTime` int(11) DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `batch_number` (`batch_number`,`serialNo`,`ref_order_no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=DYNAMIC;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb3.batch_number 結構
CREATE TABLE IF NOT EXISTS `batch_number` (
  `id` varchar(60) NOT NULL,
  `date` int(11) DEFAULT NULL,
  `no` varchar(60) NOT NULL,
  `creator_id` varchar(60) DEFAULT NULL,
  `ref_no` varchar(60) NOT NULL,
  `refCategory` int(11) DEFAULT NULL,
  `item_no` varchar(60) DEFAULT NULL,
  `item_name` varchar(60) DEFAULT NULL,
  `item_ref_no` varchar(60) DEFAULT NULL,
  `item_ref_displayName` varchar(60) DEFAULT NULL,
  `itemCategory` int(11) DEFAULT 0,
  `itemSubCategory` int(11) DEFAULT 0,
  `itemType` int(11) DEFAULT NULL,
  `unit` int(11) DEFAULT NULL,
  `expectedCount` float DEFAULT NULL,
  `checkedCount` float DEFAULT NULL,
  `validDate` int(11) DEFAULT NULL,
  `validDays` int(11) DEFAULT NULL,
  `validDateNo` varchar(60) DEFAULT NULL,
  `comment` varchar(128) DEFAULT NULL,
  `creationTime` int(11) DEFAULT NULL,
  PRIMARY KEY (`no`,`ref_no`) USING BTREE,
  KEY `idx_batch_number_ref_no` (`ref_no`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=DYNAMIC;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb3.bom 結構
CREATE TABLE IF NOT EXISTS `bom` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `no` varchar(60) NOT NULL,
  `version` float NOT NULL,
  `date` int(11) DEFAULT NULL,
  `displayName` varchar(60) DEFAULT NULL,
  `unit` int(11) DEFAULT NULL,
  `weight` float DEFAULT NULL,
  `comment` varchar(128) DEFAULT NULL,
  `creationTime` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `no` (`no`,`version`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=DYNAMIC;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb3.bom1 結構
CREATE TABLE IF NOT EXISTS `bom1` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `parent_no` varchar(60) NOT NULL,
  `parent_name` varchar(60) DEFAULT NULL,
  `child_category` int(11) DEFAULT NULL,
  `child_id` varchar(60) NOT NULL,
  `child_name` varchar(60) DEFAULT NULL,
  `childUnit` int(11) DEFAULT NULL,
  `weight` float NOT NULL DEFAULT 0,
  `expectedLoss` float NOT NULL DEFAULT 0,
  `actualLoss` float NOT NULL DEFAULT 0,
  `comment` varchar(128) DEFAULT NULL,
  `creationTime` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `parent_no` (`parent_no`,`child_id`,`weight`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb3.bom1_number 結構
CREATE TABLE IF NOT EXISTS `bom1_number` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `no` varchar(60) NOT NULL,
  `displayName` varchar(60) DEFAULT NULL,
  `unit` int(11) DEFAULT NULL,
  `weight` float DEFAULT NULL,
  `bom_no` varchar(60) DEFAULT NULL,
  `bom_version` int(11) DEFAULT NULL,
  `comment` varchar(128) DEFAULT NULL,
  `creationTime` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `no` (`no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb3.bom2 結構
CREATE TABLE IF NOT EXISTS `bom2` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `parent_no` varchar(60) DEFAULT NULL,
  `parent_name` varchar(60) DEFAULT NULL,
  `child_category` int(11) DEFAULT NULL,
  `child_id` varchar(60) DEFAULT NULL,
  `child_name` varchar(60) DEFAULT NULL,
  `childUnit` int(11) DEFAULT NULL,
  `weight` float DEFAULT NULL,
  `childUnit2` int(11) DEFAULT NULL,
  `length` float DEFAULT NULL,
  `expectedLoss` float DEFAULT 0,
  `actualLoss` float DEFAULT 0,
  `count` int(11) DEFAULT NULL,
  `comment` varchar(128) DEFAULT NULL,
  `creationTime` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb3.bom2_number 結構
CREATE TABLE IF NOT EXISTS `bom2_number` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `no` varchar(60) NOT NULL,
  `category` int(11) DEFAULT NULL,
  `displayName` varchar(60) DEFAULT NULL,
  `unit` int(11) DEFAULT NULL,
  `weight` float DEFAULT NULL,
  `bom_no` varchar(60) DEFAULT NULL,
  `bom_version` int(11) DEFAULT NULL,
  `comment` varchar(128) DEFAULT NULL,
  `creationTime` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `no` (`no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb3.bom_item 結構
CREATE TABLE IF NOT EXISTS `bom_item` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `bom_no` varchar(60) NOT NULL,
  `item_no` varchar(60) NOT NULL,
  `item_name` varchar(60) NOT NULL,
  `unit` int(11) DEFAULT NULL,
  `weight` double DEFAULT NULL,
  `creationTime` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `bom_no` (`bom_no`,`item_no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=DYNAMIC;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb3.company 結構
CREATE TABLE IF NOT EXISTS `company` (
  `no` varchar(20) NOT NULL,
  `businessNo` varchar(20) NOT NULL,
  `displayName` varchar(60) DEFAULT NULL,
  `name` varchar(60) DEFAULT NULL,
  `address` varchar(100) DEFAULT NULL,
  `phone` varchar(100) DEFAULT NULL,
  `fax` varchar(20) DEFAULT NULL,
  `contactName` varchar(60) DEFAULT NULL,
  `contactPhone` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
  `contactTitle` varchar(60) DEFAULT NULL,
  `contactEmail` varchar(60) DEFAULT NULL,
  `received_id` varchar(60) DEFAULT NULL,
  `paid_id` varchar(60) DEFAULT NULL,
  `bankCurrency` int(11) DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `bankDisplayName` varchar(60) DEFAULT NULL,
  `bankName` varchar(60) DEFAULT NULL,
  `bankBranch` varchar(60) DEFAULT NULL,
  `bankAccount` varchar(60) DEFAULT NULL,
  `bankNo` varchar(60) DEFAULT NULL,
  `comment` varchar(128) DEFAULT NULL,
  `creationTime` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `no` (`no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=DYNAMIC;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb3.contract 結構
CREATE TABLE IF NOT EXISTS `contract` (
  `no` varchar(20) NOT NULL,
  `date` int(11) NOT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ref_no` varchar(60) DEFAULT NULL,
  `creator_no` varchar(60) DEFAULT NULL,
  `displayName` varchar(60) DEFAULT NULL,
  `category` int(11) DEFAULT NULL,
  `type` int(11) DEFAULT NULL,
  `itemStyle` int(11) DEFAULT NULL,
  `item_no` varchar(60) DEFAULT NULL,
  `item_name` varchar(60) DEFAULT NULL,
  `item_ref_no` varchar(60) DEFAULT NULL,
  `item_ref_displayName` varchar(60) DEFAULT NULL,
  `unit` int(11) DEFAULT NULL,
  `itemCategory` int(11) DEFAULT NULL,
  `itemSubCategory` int(11) DEFAULT NULL,
  `payment_id` int(11) DEFAULT NULL,
  `price` double DEFAULT NULL,
  `shippingPrice` double DEFAULT NULL,
  `unitConversion` double DEFAULT NULL,
  `comment` varchar(128) DEFAULT '""',
  `creationTime` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `no` (`no`,`date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=DYNAMIC;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb3.employee 結構
CREATE TABLE IF NOT EXISTS `employee` (
  `no` varchar(20) NOT NULL,
  `name` varchar(60) DEFAULT NULL,
  `type` int(11) DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `category` int(11) DEFAULT NULL,
  `sex` int(11) DEFAULT NULL,
  `level` int(11) DEFAULT 0,
  `department` int(11) DEFAULT NULL,
  `jobTitle` varchar(60) DEFAULT NULL,
  `joinedDate` int(11) DEFAULT NULL,
  `leftDate` int(11) DEFAULT NULL,
  `identityId` varchar(60) DEFAULT NULL,
  `country` varchar(60) DEFAULT NULL,
  `birthday` int(11) DEFAULT NULL,
  `phone` varchar(60) DEFAULT NULL,
  `address` varchar(100) DEFAULT NULL,
  `comment` varchar(128) DEFAULT NULL,
  `creationTime` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `no` (`no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb3.enterprise 結構
CREATE TABLE IF NOT EXISTS `enterprise` (
  `no` varchar(60) NOT NULL,
  `businessNo` varchar(20) NOT NULL,
  `displayName` varchar(60) DEFAULT NULL,
  `name` varchar(60) DEFAULT NULL,
  `address` varchar(100) DEFAULT NULL,
  `phone` varchar(100) DEFAULT NULL,
  `fax` varchar(20) DEFAULT NULL,
  `department` int(11) DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `lar` varchar(60) DEFAULT NULL,
  `comment` varchar(128) DEFAULT NULL,
  `creationTime` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `no` (`no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=DYNAMIC;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb3.equipment 結構
CREATE TABLE IF NOT EXISTS `equipment` (
  `no` varchar(60) NOT NULL,
  `station_no` varchar(60) DEFAULT '',
  `name` varchar(60) DEFAULT '',
  `model` varchar(60) DEFAULT '',
  `manufacturer` varchar(60) DEFAULT '',
  `purchaseDate` int(11) DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `appearance` varchar(128) DEFAULT '',
  `comment` varchar(128) DEFAULT '',
  `creationTime` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `no` (`no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb3.factory 結構
CREATE TABLE IF NOT EXISTS `factory` (
  `no` varchar(60) NOT NULL,
  `region` varchar(60) DEFAULT NULL,
  `location` varchar(60) DEFAULT NULL,
  `comment` varchar(128) DEFAULT NULL,
  `creationTime` int(11) DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `no` (`no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=DYNAMIC;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb3.goods 結構
CREATE TABLE IF NOT EXISTS `goods` (
  `no` varchar(20) NOT NULL,
  `category` int(11) DEFAULT NULL,
  `subCategory` int(11) DEFAULT NULL,
  `name` varchar(100) NOT NULL,
  `unitShipping` int(11) DEFAULT NULL,
  `unitWarehouse` int(11) DEFAULT NULL,
  `unitProduct` int(11) DEFAULT NULL,
  `comment` varchar(128) DEFAULT NULL,
  `creationTime` int(11) DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `no` (`no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=DYNAMIC;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb3.goods_receipt_note 結構
CREATE TABLE IF NOT EXISTS `goods_receipt_note` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `no` varchar(20) NOT NULL,
  `creator_no` varchar(60) DEFAULT NULL,
  `purchase_order_no` varchar(60) DEFAULT NULL,
  `date` int(11) DEFAULT NULL,
  `category` int(11) DEFAULT NULL,
  `item_ref_no` varchar(60) DEFAULT NULL,
  `item_ref_displayName` varchar(60) DEFAULT NULL,
  `item_no` varchar(60) DEFAULT NULL,
  `item_name` varchar(60) DEFAULT NULL,
  `itemCategory` int(11) DEFAULT NULL,
  `itemSubCategory` int(11) DEFAULT NULL,
  `unit` int(11) DEFAULT NULL,
  `price` double DEFAULT NULL,
  `expectedCount` float DEFAULT NULL,
  `checkedCount` float DEFAULT NULL,
  `feeCount` float DEFAULT 0,
  `amount` int(11) DEFAULT NULL,
  `addDeleteAmount` int(11) DEFAULT NULL,
  `comment` varchar(128) DEFAULT NULL,
  `creationTime` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `no` (`no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb3.inproduct 結構
CREATE TABLE IF NOT EXISTS `inproduct` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `no` varchar(60) NOT NULL,
  `category` int(11) DEFAULT NULL,
  `name` varchar(100) DEFAULT NULL,
  `customer_no` varchar(60) DEFAULT NULL,
  `customer_displayName` varchar(60) DEFAULT NULL,
  `cost_no` varchar(60) DEFAULT NULL,
  `loss_no` varchar(60) DEFAULT NULL,
  `unitShipping` int(11) DEFAULT NULL,
  `unitWarehouse` int(11) DEFAULT NULL,
  `unitProduct` int(11) DEFAULT NULL,
  `comment` varchar(128) DEFAULT NULL,
  `creationTime` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `no` (`no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb3.inproduct_bom_spec 結構
CREATE TABLE IF NOT EXISTS `inproduct_bom_spec` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `inproduct_no` varchar(60) NOT NULL,
  `category` int(11) DEFAULT NULL,
  `item_no` varchar(60) NOT NULL,
  `item_version` int(11) NOT NULL DEFAULT 0,
  `bom12_no` varchar(60) NOT NULL,
  `count` int(11) DEFAULT NULL,
  `unit` int(11) DEFAULT NULL,
  `weight` float DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `item_no` (`item_no`,`inproduct_no`,`item_version`,`bom12_no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb3.inventory_delta 結構
CREATE TABLE IF NOT EXISTS `inventory_delta` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `warehouse_no` varchar(60) NOT NULL,
  `warehouse_displayName` varchar(60) DEFAULT NULL,
  `date` date NOT NULL,
  `timezone` varchar(60) NOT NULL,
  `kind` int(11) DEFAULT NULL,
  `category` int(11) DEFAULT NULL,
  `specified_no` varchar(60) NOT NULL,
  `specified_name` varchar(60) NOT NULL,
  `specified_ref_no` varchar(60) NOT NULL,
  `specified_ref_name` varchar(60) NOT NULL,
  `in_ref_id` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
  `out_ref_id` longtext DEFAULT NULL,
  `inCount` float DEFAULT NULL,
  `inPurchaseCount` float DEFAULT NULL,
  `inAmount` double DEFAULT NULL,
  `inPurchaseAmount` double DEFAULT NULL,
  `outCount` float DEFAULT NULL,
  `outAmount` double DEFAULT NULL,
  `creationTime` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `warehouse_no` (`warehouse_no`,`date`,`timezone`,`specified_no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=DYNAMIC;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb3.inventory_item_month_statistic 結構
CREATE TABLE IF NOT EXISTS `inventory_item_month_statistic` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `warehouse_no` varchar(60) NOT NULL,
  `warehouse_displayName` varchar(60) DEFAULT NULL,
  `date` date NOT NULL,
  `timezone` varchar(60) NOT NULL,
  `kind` int(11) DEFAULT NULL,
  `category` int(11) DEFAULT NULL,
  `specified_no` varchar(60) NOT NULL,
  `specified_name` varchar(60) NOT NULL,
  `specified_ref_no` varchar(60) NOT NULL,
  `specified_ref_name` varchar(60) NOT NULL,
  `unit` int(11) DEFAULT 0,
  `startCount` float DEFAULT NULL,
  `startAmount` double DEFAULT NULL,
  `inCount` float DEFAULT NULL,
  `inAmount` double DEFAULT NULL,
  `endCount` float DEFAULT NULL,
  `endAmount` double DEFAULT NULL,
  `creationTime` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `warehouse_no` (`warehouse_no`,`date`,`timezone`,`specified_no`,`specified_ref_no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=DYNAMIC;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb3.inventory_month_statistic 結構
CREATE TABLE IF NOT EXISTS `inventory_month_statistic` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `warehouse_no` varchar(60) NOT NULL,
  `warehouse_displayName` varchar(60) DEFAULT NULL,
  `date` date NOT NULL,
  `timezone` varchar(60) NOT NULL,
  `category` int(11) NOT NULL,
  `startAmount` double DEFAULT NULL,
  `inPurchaseAmount` double DEFAULT NULL,
  `inAmount` double DEFAULT NULL,
  `outAmount` double DEFAULT NULL,
  `endAmount` double DEFAULT NULL,
  `creationTime` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `warehouse_no` (`warehouse_no`,`date`,`timezone`,`category`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=DYNAMIC;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb3.inventory_order 結構
CREATE TABLE IF NOT EXISTS `inventory_order` (
  `no` varchar(60) NOT NULL,
  `creator_no` varchar(60) DEFAULT NULL,
  `date` int(11) DEFAULT NULL,
  `category` int(11) DEFAULT NULL,
  `subCategory` int(11) DEFAULT NULL,
  `item_no` varchar(60) DEFAULT NULL,
  `item_name` varchar(60) DEFAULT NULL,
  `item_ref_no` varchar(60) DEFAULT NULL,
  `item_ref_displayName` varchar(60) DEFAULT NULL,
  `itemType` int(11) DEFAULT NULL,
  `itemCategory` int(11) DEFAULT NULL,
  `unit` int(11) DEFAULT NULL,
  `price` float DEFAULT NULL,
  `checkedCount` float DEFAULT NULL,
  `expectedCount` float DEFAULT NULL,
  `amount` float DEFAULT NULL,
  `comment` varchar(128) DEFAULT NULL,
  `creationTime` int(11) DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`),
  UNIQUE KEY `no` (`no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb3.inventory_record 結構
CREATE TABLE IF NOT EXISTS `inventory_record` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group` varchar(60) DEFAULT NULL,
  `refCategory` int(11) DEFAULT NULL,
  `ref_no` varchar(60) DEFAULT NULL,
  `warehouse_no` varchar(60) DEFAULT NULL,
  `warehouse_displayName` varchar(60) DEFAULT NULL,
  `date` int(11) DEFAULT NULL,
  `category` int(11) DEFAULT NULL,
  `source` int(11) DEFAULT NULL,
  `batchNumber` varchar(20) DEFAULT NULL,
  `serialNo` varchar(20) DEFAULT NULL,
  `item_no` varchar(60) DEFAULT NULL,
  `item_name` varchar(60) DEFAULT NULL,
  `item_ref_no` varchar(60) DEFAULT NULL,
  `item_ref_displayName` varchar(60) DEFAULT NULL,
  `itemCategory` int(11) DEFAULT NULL,
  `itemType` int(11) DEFAULT NULL,
  `unit` int(11) DEFAULT NULL,
  `count` float DEFAULT NULL,
  `price` double DEFAULT NULL,
  `amount` double DEFAULT NULL,
  `comment` varchar(128) DEFAULT NULL,
  `registerDevId` varchar(60) DEFAULT NULL,
  `creationTime` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb3.item_hours 結構
CREATE TABLE IF NOT EXISTS `item_hours` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `item_no` varchar(60) NOT NULL,
  `itemCategory` int(11) DEFAULT NULL,
  `date` date NOT NULL,
  `unit` int(11) DEFAULT NULL,
  `estValue` double DEFAULT NULL,
  `value` double DEFAULT NULL,
  `creationTime` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `item_no` (`item_no`,`date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=DYNAMIC;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb3.item_loss 結構
CREATE TABLE IF NOT EXISTS `item_loss` (
  `item_no` varchar(60) NOT NULL,
  `itemCategory` int(11) DEFAULT NULL,
  `date` date NOT NULL,
  `unit` int(11) DEFAULT NULL,
  `estValue` double DEFAULT NULL,
  `value` double DEFAULT NULL,
  `creationTime` int(11) DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`),
  UNIQUE KEY `item_no` (`item_no`,`date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=DYNAMIC;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb3.item_price 結構
CREATE TABLE IF NOT EXISTS `item_price` (
  `no` varchar(60) NOT NULL DEFAULT '',
  `item_no` varchar(60) NOT NULL,
  `item_name` varchar(100) NOT NULL,
  `itemCategory` int(11) DEFAULT NULL,
  `date` date NOT NULL,
  `whUnitWeight` int(11) DEFAULT NULL,
  `whUnitLength` int(11) DEFAULT NULL,
  `costUnitWeight` int(11) DEFAULT NULL,
  `costUnitLength` int(11) DEFAULT NULL,
  `estWHPriceWeight` double DEFAULT NULL,
  `estWHPriceWeight1` double DEFAULT NULL,
  `estWHPriceWeight2` double DEFAULT NULL,
  `estWHPriceLength` double DEFAULT NULL,
  `estCostPriceWeight` double DEFAULT NULL,
  `estCostPriceWeight1` double DEFAULT NULL,
  `estCostPriceWeight2` double DEFAULT NULL,
  `estCostPriceLength` double DEFAULT NULL,
  `estLaborCost` double DEFAULT NULL,
  `whPriceWeight` double DEFAULT NULL,
  `whPriceWeight1` double DEFAULT NULL,
  `whPriceWeight2` double DEFAULT NULL,
  `whPriceLength` double DEFAULT NULL,
  `costPriceWeight` double DEFAULT NULL,
  `costPriceWeight1` double DEFAULT NULL,
  `costPriceWeight2` double DEFAULT NULL,
  `costPriceLength` double DEFAULT NULL,
  `laborCost` double DEFAULT NULL,
  `creationTime` int(11) DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`),
  UNIQUE KEY `item_no` (`item_no`,`date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=DYNAMIC;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb3.material 結構
CREATE TABLE IF NOT EXISTS `material` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `no` varchar(20) NOT NULL,
  `category` int(11) DEFAULT NULL,
  `subCategory` int(11) DEFAULT NULL,
  `type` int(11) DEFAULT NULL,
  `name` varchar(100) NOT NULL,
  `supplier_no` varchar(60) DEFAULT NULL,
  `supplier_displayName` varchar(60) DEFAULT NULL,
  `cost_no` varchar(60) DEFAULT NULL,
  `loss_no` varchar(60) DEFAULT NULL,
  `unitShipping` int(11) DEFAULT NULL,
  `unitWarehouse` int(11) DEFAULT NULL,
  `unitProduct` int(11) DEFAULT NULL,
  `comment` varchar(128) DEFAULT NULL,
  `creationTime` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `no` (`no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=DYNAMIC;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb3.member 結構
CREATE TABLE IF NOT EXISTS `member` (
  `user_no` varchar(60) NOT NULL,
  `account` varchar(60) NOT NULL,
  `password` varchar(100) DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_no` (`user_no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb3.order_item_month_statistic 結構
CREATE TABLE IF NOT EXISTS `order_item_month_statistic` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `date` date NOT NULL,
  `timezone` varchar(60) NOT NULL,
  `kind` int(11) NOT NULL,
  `category` int(11) NOT NULL,
  `subCategory` int(11) NOT NULL,
  `type` int(11) NOT NULL,
  `specified_no` varchar(60) NOT NULL,
  `specified_name` varchar(60) NOT NULL,
  `payment` int(11) DEFAULT NULL,
  `amount` int(11) DEFAULT NULL,
  `creationTime` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `date` (`date`,`category`,`subCategory`,`kind`,`specified_no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=DYNAMIC;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb3.order_payment 結構
CREATE TABLE IF NOT EXISTS `order_payment` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `no` varchar(60) NOT NULL,
  `group_no` varchar(60) NOT NULL,
  `arapType` int(11) NOT NULL,
  `date` int(11) NOT NULL,
  `refCategory` int(11) NOT NULL,
  `ref_no` varchar(60) NOT NULL,
  `ref_sub_no` varchar(60) NOT NULL,
  `item_ref_no` varchar(60) NOT NULL,
  `item_ref_displayName` varchar(60) NOT NULL,
  `itemCategory` int(11) NOT NULL,
  `itemSubCategory` int(11) NOT NULL,
  `paymentType` int(11) NOT NULL,
  `month` date NOT NULL,
  `price` double DEFAULT NULL,
  `count` float DEFAULT NULL,
  `amount` int(11) DEFAULT NULL,
  `addDeleteAmount` int(11) DEFAULT NULL,
  `totalAmount` int(11) DEFAULT NULL,
  `balance` int(11) DEFAULT NULL,
  `creationTime` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=DYNAMIC;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb3.payment 結構
CREATE TABLE IF NOT EXISTS `payment` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `type` int(11) DEFAULT NULL,
  `source` int(11) DEFAULT NULL,
  `date` int(11) NOT NULL,
  `period` int(11) NOT NULL,
  `creationTime` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `type` (`type`,`source`,`date`,`period`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb3.pl_item_capacity 結構
CREATE TABLE IF NOT EXISTS `pl_item_capacity` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `month` date NOT NULL,
  `pl_no` varchar(60) NOT NULL,
  `pl_name` varchar(60) NOT NULL,
  `item_no` varchar(60) NOT NULL,
  `item_name` varchar(60) NOT NULL,
  `assembly_no` varchar(60) NOT NULL,
  `assemblyVer` int(11) NOT NULL,
  `bomWeight` double DEFAULT NULL,
  `bomUnit` int(11) NOT NULL,
  `productCount` int(11) NOT NULL,
  `hours` float DEFAULT NULL,
  `count` float DEFAULT NULL,
  `unit` int(11) DEFAULT NULL,
  `hourlyOutput` double DEFAULT NULL,
  `price` double DEFAULT NULL,
  `rawMaterialCost` double DEFAULT NULL,
  `materialCost` double DEFAULT NULL,
  `laborCost` double DEFAULT NULL,
  `creationTime` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `pl_no` (`pl_no`,`month`,`item_no`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=DYNAMIC;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb3.pl_item_loss 結構
CREATE TABLE IF NOT EXISTS `pl_item_loss` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `month` date NOT NULL,
  `pl_item_capacity_no` varchar(60) NOT NULL,
  `item_no` varchar(60) DEFAULT NULL,
  `item_name` varchar(60) NOT NULL,
  `itemCategory` int(11) NOT NULL,
  `itemSubCategory` int(11) NOT NULL,
  `weightRatio` double DEFAULT NULL,
  `lossRate` double DEFAULT NULL,
  `creationTime` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `pl_item_capacity_no` (`pl_item_capacity_no`,`item_no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=DYNAMIC;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb3.pl_man_capacity 結構
CREATE TABLE IF NOT EXISTS `pl_man_capacity` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `month` date NOT NULL,
  `pl_no` varchar(60) NOT NULL,
  `pl_name` varchar(60) NOT NULL,
  `productCount` int(11) NOT NULL,
  `laborCount` int(11) NOT NULL,
  `unit` int(11) NOT NULL,
  `hourlyOutput` double NOT NULL,
  `creationTime` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `month` (`month`,`pl_no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=DYNAMIC;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb3.process 結構
CREATE TABLE IF NOT EXISTS `process` (
  `no` varchar(60) NOT NULL,
  `oneProcess` int(11) DEFAULT NULL,
  `secProcess` int(11) DEFAULT NULL,
  `comment` varchar(128) DEFAULT '',
  `creationTime` int(11) DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`),
  UNIQUE KEY `no` (`no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=DYNAMIC;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb3.process_capacity 結構
CREATE TABLE IF NOT EXISTS `process_capacity` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `date` date DEFAULT NULL,
  `oneProcess` int(11) DEFAULT NULL,
  `secProcess` int(11) DEFAULT NULL,
  `unit` int(11) DEFAULT NULL,
  `laborCount` int(11) DEFAULT NULL,
  `hourlyOutput` double DEFAULT NULL,
  `commnet` varchar(128) DEFAULT NULL,
  `creationTime` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `date` (`date`,`oneProcess`,`secProcess`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=DYNAMIC;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb3.process_flow 結構
CREATE TABLE IF NOT EXISTS `process_flow` (
  `no` varchar(60) NOT NULL,
  `product_process_no` varchar(60) DEFAULT NULL,
  `order` int(11) DEFAULT NULL,
  `oneProcess` int(11) DEFAULT NULL,
  `secProcess` int(11) DEFAULT NULL,
  PRIMARY KEY (`no`) USING BTREE,
  UNIQUE KEY `item_no` (`product_process_no`,`order`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=DYNAMIC;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb3.process_labor 結構
CREATE TABLE IF NOT EXISTS `process_labor` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `date` int(11) DEFAULT NULL,
  `creator_no` varchar(60) DEFAULT NULL,
  `work_order_no` varchar(60) NOT NULL,
  `employee_no` varchar(60) NOT NULL,
  `production_line_no` varchar(60) DEFAULT NULL,
  `station_no` varchar(60) DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `work_order_no` (`work_order_no`,`employee_no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=DYNAMIC;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb3.process_order 結構
CREATE TABLE IF NOT EXISTS `process_order` (
  `no` varchar(20) NOT NULL,
  `creator_no` varchar(60) DEFAULT NULL,
  `work_order_no` varchar(60) DEFAULT NULL,
  `refProcess` int(11) DEFAULT NULL,
  `date` int(11) DEFAULT NULL,
  `category` int(11) DEFAULT NULL,
  `item_no` varchar(60) DEFAULT NULL,
  `item_name` varchar(60) DEFAULT NULL,
  `itemCategory` int(11) DEFAULT NULL,
  `itemSubCategory` int(11) DEFAULT NULL,
  `item_ref_no` varchar(60) DEFAULT NULL,
  `item_ref_displayName` varchar(60) DEFAULT NULL,
  `unit` int(11) DEFAULT NULL,
  `count` float DEFAULT NULL,
  `expectedCount` float DEFAULT NULL,
  `comment` varchar(128) DEFAULT NULL,
  `creationTime` int(11) DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`),
  UNIQUE KEY `no` (`no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=DYNAMIC;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb3.product 結構
CREATE TABLE IF NOT EXISTS `product` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `no` varchar(20) NOT NULL,
  `category` int(11) DEFAULT NULL,
  `name` varchar(100) NOT NULL,
  `unitShipping` int(11) DEFAULT NULL,
  `unitWarehouse` int(11) DEFAULT NULL,
  `unitProduct` int(11) DEFAULT NULL,
  `version` int(11) DEFAULT NULL,
  `comment` varchar(128) DEFAULT NULL,
  `creationTime` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `no` (`no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb3.production_data 結構
CREATE TABLE IF NOT EXISTS `production_data` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `creator_no` varchar(60) DEFAULT NULL,
  `work_order_no` varchar(60) NOT NULL,
  `product_order_no` varchar(60) DEFAULT NULL,
  `customer_no` varchar(60) DEFAULT NULL,
  `customer_displayName` varchar(60) DEFAULT NULL,
  `product_no` varchar(60) DEFAULT NULL,
  `product_name` varchar(100) DEFAULT NULL,
  `date` int(11) DEFAULT NULL,
  `production_line_no` varchar(60) DEFAULT NULL,
  `oneProcess` int(11) DEFAULT NULL,
  `secProcess` int(11) DEFAULT NULL,
  `item_no` varchar(60) DEFAULT NULL,
  `item_name` varchar(100) DEFAULT NULL,
  `materialLoss` float DEFAULT NULL,
  `comment` varchar(128) DEFAULT NULL,
  `creationTime` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `work_order_no` (`work_order_no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=DYNAMIC;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb3.production_data_input 結構
CREATE TABLE IF NOT EXISTS `production_data_input` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `work_order_no` varchar(60) NOT NULL,
  `process_order_no` varchar(60) DEFAULT NULL,
  `group` varchar(60) NOT NULL,
  `action` int(11) NOT NULL,
  `time` int(11) DEFAULT NULL,
  `item_no` varchar(60) NOT NULL,
  `item_name` varchar(100) NOT NULL,
  `itemSubCategory` int(11) DEFAULT NULL,
  `category` int(11) DEFAULT NULL,
  `batch_number` varchar(60) NOT NULL,
  `serial_no` varchar(60) NOT NULL,
  `unit` int(11) DEFAULT NULL,
  `count` float NOT NULL,
  `comment` varchar(128) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `work_order_no` (`work_order_no`,`group`,`action`,`item_no`,`batch_number`,`serial_no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=DYNAMIC;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb3.production_data_labor 結構
CREATE TABLE IF NOT EXISTS `production_data_labor` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `work_order_no` varchar(60) NOT NULL,
  `employee_no` varchar(60) NOT NULL,
  `employee_name` varchar(100) DEFAULT NULL,
  `employee_type` int(11) DEFAULT NULL,
  `employee_jobTitle` int(11) DEFAULT NULL,
  `employee_level` int(11) DEFAULT 0,
  `station_no` varchar(60) DEFAULT NULL,
  `stationStage` int(11) NOT NULL,
  `action` int(11) NOT NULL,
  `startTime` int(11) NOT NULL,
  `endTime` int(11) NOT NULL,
  `hours` float NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`),
  UNIQUE KEY `work_order_no` (`work_order_no`,`employee_no`,`stationStage`,`action`,`startTime`,`endTime`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=DYNAMIC;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb3.production_data_machine 結構
CREATE TABLE IF NOT EXISTS `production_data_machine` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `work_order_no` varchar(60) NOT NULL,
  `equipment_no` varchar(60) NOT NULL,
  `equipment_name` varchar(100) DEFAULT NULL,
  `time` int(11) DEFAULT NULL,
  `action` int(11) NOT NULL,
  `temperature` float DEFAULT NULL,
  `speed` float DEFAULT NULL,
  `creationTime` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `work_order_no` (`work_order_no`,`equipment_no`,`action`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=DYNAMIC;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb3.production_data_output 結構
CREATE TABLE IF NOT EXISTS `production_data_output` (
  `id` varchar(60) NOT NULL,
  `work_order_no` varchar(60) NOT NULL,
  `process_order_no` varchar(60) DEFAULT NULL,
  `time` int(11) DEFAULT NULL,
  `action` int(11) NOT NULL,
  `item_no` varchar(60) NOT NULL,
  `group` varchar(60) NOT NULL,
  `item_name` varchar(100) NOT NULL,
  `category` int(11) DEFAULT NULL,
  `itemSubCategory` int(11) DEFAULT 0,
  `batch_number` varchar(60) NOT NULL,
  `serial_no` varchar(60) NOT NULL,
  `valid_date` int(11) DEFAULT NULL,
  `valid_date_no` varchar(60) DEFAULT NULL,
  `unit` int(11) DEFAULT NULL,
  `count` float NOT NULL,
  `comment` varchar(128) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `work_order_no` (`work_order_no`,`action`,`item_no`,`group`,`batch_number`,`serial_no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=DYNAMIC;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb3.production_data_reuse 結構
CREATE TABLE IF NOT EXISTS `production_data_reuse` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `work_order_no` varchar(60) NOT NULL,
  `process_order_no` varchar(60) DEFAULT NULL,
  `time` int(11) DEFAULT NULL,
  `action` int(11) NOT NULL,
  `item_no` varchar(60) NOT NULL,
  `item_name` varchar(100) DEFAULT NULL,
  `itemSubCategory` int(11) DEFAULT NULL,
  `category` int(11) NOT NULL,
  `batch_number` varchar(60) NOT NULL,
  `serial_no` varchar(60) NOT NULL,
  `unit` int(11) DEFAULT NULL,
  `count` float NOT NULL,
  `comment` varchar(128) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `work_order_no` (`work_order_no`,`process_order_no`,`action`,`item_no`,`category`,`batch_number`,`serial_no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=DYNAMIC;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb3.production_line 結構
CREATE TABLE IF NOT EXISTS `production_line` (
  `no` varchar(60) NOT NULL,
  `name` varchar(60) NOT NULL,
  `process_no` varchar(60) NOT NULL,
  `oneProcess` int(11) DEFAULT NULL,
  `secProcess` int(11) DEFAULT NULL,
  `factory_no` varchar(60) DEFAULT NULL,
  `location` varchar(60) DEFAULT NULL,
  `capacityUnit` int(11) DEFAULT NULL,
  `capacity` float DEFAULT NULL,
  `laborCount` int(11) DEFAULT NULL,
  `laborEfficiency` float DEFAULT NULL,
  `comment` varchar(128) DEFAULT NULL,
  `creationTime` int(11) DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`),
  UNIQUE KEY `no` (`no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=DYNAMIC;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb3.product_bom_spec 結構
CREATE TABLE IF NOT EXISTS `product_bom_spec` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `product_no` varchar(60) NOT NULL,
  `product_version` int(11) NOT NULL,
  `level` int(11) DEFAULT NULL,
  `bom2_no` varchar(60) NOT NULL,
  `count` int(11) DEFAULT NULL,
  `unit` int(11) DEFAULT NULL,
  `weight` float DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `product_no` (`product_no`,`product_version`,`bom2_no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=DYNAMIC;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb3.product_order 結構
CREATE TABLE IF NOT EXISTS `product_order` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `no` varchar(20) NOT NULL,
  `creator_no` varchar(60) DEFAULT NULL,
  `date` int(11) DEFAULT NULL,
  `ref_no` varchar(60) DEFAULT '',
  `item_ref_no` varchar(60) DEFAULT NULL,
  `item_ref_displayName` varchar(60) DEFAULT NULL,
  `item_no` varchar(60) DEFAULT NULL,
  `item_name` varchar(60) DEFAULT NULL,
  `unit` int(11) DEFAULT NULL,
  `count` float DEFAULT NULL,
  `preparedCount` float DEFAULT 0,
  `price` float DEFAULT NULL,
  `amount` int(11) DEFAULT NULL,
  `expectedDate` int(11) DEFAULT NULL,
  `address` varchar(100) DEFAULT NULL,
  `payment_type` int(11) DEFAULT NULL,
  `payment_source` int(11) DEFAULT NULL,
  `payment_date` int(11) DEFAULT NULL,
  `payment_period` int(11) DEFAULT NULL,
  `comment` varchar(128) DEFAULT NULL,
  `creationTime` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `no` (`no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=DYNAMIC;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb3.product_process 結構
CREATE TABLE IF NOT EXISTS `product_process` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `no` varchar(60) NOT NULL,
  `item_no` varchar(60) DEFAULT NULL,
  `version` int(11) DEFAULT NULL,
  `date` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `item_no` (`item_no`,`version`,`no`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb3.product_spec 結構
CREATE TABLE IF NOT EXISTS `product_spec` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `product_no` varchar(60) NOT NULL,
  `product_version` int(11) NOT NULL,
  `bom_no` varchar(60) DEFAULT NULL,
  `bom_version` int(11) NOT NULL,
  `level` int(11) DEFAULT NULL,
  `item_type` int(11) DEFAULT NULL,
  `item_no` varchar(60) NOT NULL,
  `count` int(11) DEFAULT NULL,
  `unit` int(11) DEFAULT NULL,
  `weight` float DEFAULT NULL,
  `expectedLoss` float DEFAULT 0,
  `actualLoss` float DEFAULT 0,
  PRIMARY KEY (`id`),
  UNIQUE KEY `product_no` (`product_no`,`product_version`,`item_no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb3.product_ver 結構
CREATE TABLE IF NOT EXISTS `product_ver` (
  `no` varchar(60) NOT NULL,
  `item_no` varchar(60) DEFAULT NULL,
  `version` float NOT NULL,
  `date` int(11) DEFAULT NULL,
  PRIMARY KEY (`no`) USING BTREE,
  UNIQUE KEY `version` (`version`,`item_no`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=DYNAMIC;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb3.purchase_order 結構
CREATE TABLE IF NOT EXISTS `purchase_order` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `no` varchar(20) NOT NULL,
  `creator_no` varchar(60) DEFAULT NULL,
  `purchase_request_no` varchar(60) DEFAULT NULL,
  `date` int(11) DEFAULT NULL,
  `ref_no` varchar(60) DEFAULT NULL,
  `item_ref_no` varchar(60) DEFAULT NULL,
  `item_ref_displayName` varchar(60) DEFAULT NULL,
  `item_no` varchar(60) DEFAULT NULL,
  `item_name` varchar(60) DEFAULT NULL,
  `unit` int(11) DEFAULT NULL,
  `price` double DEFAULT NULL,
  `count` float DEFAULT NULL,
  `amount` int(11) DEFAULT NULL,
  `expectedDate` int(11) DEFAULT NULL,
  `address` varchar(100) DEFAULT NULL,
  `payment_type` int(11) DEFAULT NULL,
  `payment_source` int(11) DEFAULT NULL,
  `payment_date` int(11) DEFAULT NULL,
  `payment_period` int(11) DEFAULT NULL,
  `comment` varchar(128) DEFAULT NULL,
  `creationTime` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `no` (`no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb3.purchase_request 結構
CREATE TABLE IF NOT EXISTS `purchase_request` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `no` varchar(20) DEFAULT NULL,
  `creator_no` varchar(60) DEFAULT NULL,
  `product_order_no` varchar(60) DEFAULT NULL,
  `date` int(11) DEFAULT NULL,
  `comment` varchar(128) DEFAULT NULL,
  `creationTime` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `no` (`no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb3.purchase_request_item 結構
CREATE TABLE IF NOT EXISTS `purchase_request_item` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `purchase_request_no` varchar(60) DEFAULT NULL,
  `item_no` varchar(60) DEFAULT NULL,
  `unit` int(11) DEFAULT NULL,
  `count` float DEFAULT NULL,
  `expectedDate` int(11) DEFAULT NULL,
  `comment` varchar(128) DEFAULT NULL,
  `creationTime` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `purchase_request_no` (`purchase_request_no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb3.quotation 結構
CREATE TABLE IF NOT EXISTS `quotation` (
  `no` varchar(20) NOT NULL,
  `creator_no` varchar(60) DEFAULT NULL,
  `date` int(11) DEFAULT NULL,
  `category` int(11) DEFAULT NULL,
  `type` int(11) DEFAULT NULL,
  `itemStyle` int(11) DEFAULT NULL,
  `item_no` varchar(60) DEFAULT NULL,
  `item_name` varchar(60) DEFAULT NULL,
  `item_ref_no` varchar(60) DEFAULT NULL,
  `item_ref_displayName` varchar(60) DEFAULT NULL,
  `unit` int(11) DEFAULT NULL,
  `price` double DEFAULT NULL,
  `unitConversion` double DEFAULT NULL,
  `comment` varchar(128) DEFAULT NULL,
  `creationTime` int(11) DEFAULT NULL,
  PRIMARY KEY (`no`) USING BTREE,
  KEY `customer_id` (`item_ref_no`) USING BTREE,
  KEY `product_id` (`item_no`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb3.sample_price 結構
CREATE TABLE IF NOT EXISTS `sample_price` (
  `item_no` varchar(60) NOT NULL,
  `date` date NOT NULL,
  `estWHUnitWeight` int(11) DEFAULT NULL,
  `estWHPriceWeight` double DEFAULT NULL,
  `estCostUnitWeight` int(11) DEFAULT NULL,
  `estCostPriceWeight` double DEFAULT NULL,
  `estLaborCost` double DEFAULT NULL,
  `whUnitWeight` int(11) DEFAULT NULL,
  `whPriceWeight` double DEFAULT NULL,
  `costUnitWeight` int(11) DEFAULT NULL,
  `costPriceWeight` double DEFAULT NULL,
  `laborCost` double DEFAULT NULL,
  `creationTime` int(11) DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`),
  UNIQUE KEY `item_no` (`item_no`,`date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=DYNAMIC;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb3.session 結構
CREATE TABLE IF NOT EXISTS `session` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `token` varchar(60) DEFAULT NULL,
  `user_no` varchar(60) DEFAULT NULL,
  `expiredTime` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb3.shipping_order 結構
CREATE TABLE IF NOT EXISTS `shipping_order` (
  `id` varchar(60) NOT NULL,
  `no` varchar(20) NOT NULL,
  `creator_no` varchar(60) DEFAULT NULL,
  `product_order_no` varchar(60) DEFAULT NULL,
  `date` int(11) DEFAULT NULL,
  `category` int(11) DEFAULT NULL,
  `item_ref_no` varchar(60) DEFAULT NULL,
  `item_ref_displayName` varchar(60) DEFAULT NULL,
  `item_no` varchar(60) DEFAULT NULL,
  `item_name` varchar(60) DEFAULT NULL,
  `itemCategory` int(11) DEFAULT NULL,
  `itemSubCategory` int(11) DEFAULT NULL,
  `unit` int(11) DEFAULT NULL,
  `expectedCount` float DEFAULT NULL,
  `checkedCount` float DEFAULT NULL,
  `feeCount` float DEFAULT 0,
  `price` double DEFAULT NULL,
  `amount` int(11) DEFAULT NULL,
  `addDeleteAmount` int(11) DEFAULT NULL,
  `comment` varchar(128) DEFAULT NULL,
  `creationTime` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `no` (`no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb3.shipping_payment 結構
CREATE TABLE IF NOT EXISTS `shipping_payment` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `no` varchar(60) NOT NULL,
  `group_no` varchar(60) NOT NULL,
  `arapType` int(11) NOT NULL,
  `date` int(11) NOT NULL,
  `refCategory` int(11) NOT NULL,
  `record_no` varchar(60) NOT NULL,
  `ref_no` varchar(60) NOT NULL,
  `ref_sub_no` varchar(60) NOT NULL,
  `item_ref_no` varchar(60) NOT NULL,
  `item_ref_displayName` varchar(60) NOT NULL,
  `paymentType` int(11) NOT NULL,
  `month` date NOT NULL,
  `price` double DEFAULT NULL,
  `count` int(11) DEFAULT NULL,
  `amount` int(11) DEFAULT NULL,
  `addDeleteAmount` int(11) DEFAULT NULL,
  `totalAmount` int(11) DEFAULT NULL,
  `balance` int(11) DEFAULT NULL,
  `creationTime` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `no` (`no`,`date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=DYNAMIC;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb3.shipping_record 結構
CREATE TABLE IF NOT EXISTS `shipping_record` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `date` int(11) DEFAULT NULL,
  `refCategory` int(11) DEFAULT NULL,
  `ref_no` varchar(60) DEFAULT NULL,
  `ref_parent_no` varchar(60) DEFAULT NULL,
  `sw_alias_no` varchar(60) DEFAULT NULL,
  `sw_alias_name` varchar(60) DEFAULT NULL,
  `item_no` varchar(60) DEFAULT NULL,
  `item_name` varchar(60) DEFAULT NULL,
  `item_ref_no` varchar(60) DEFAULT NULL,
  `item_ref_displayName` varchar(60) DEFAULT NULL,
  `contract_no` varchar(60) DEFAULT NULL,
  `unit` int(11) DEFAULT NULL,
  `price` double DEFAULT NULL,
  `checkedCount` int(11) DEFAULT NULL,
  `expectedCount` int(11) DEFAULT NULL,
  `comment` varchar(128) DEFAULT NULL,
  `creationTime` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=DYNAMIC;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb3.ship_wh 結構
CREATE TABLE IF NOT EXISTS `ship_wh` (
  `no` varchar(60) NOT NULL,
  `company_no` varchar(60) NOT NULL,
  `company_displayName` varchar(60) DEFAULT NULL,
  `name` varchar(60) DEFAULT NULL,
  `category` int(11) NOT NULL,
  `attribute` int(11) NOT NULL,
  `unit` int(11) DEFAULT NULL,
  `maxCapacity` int(11) DEFAULT NULL,
  `comment` varchar(128) DEFAULT NULL,
  `creationTime` int(11) DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`),
  UNIQUE KEY `no` (`no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=DYNAMIC;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb3.ship_wh_alias 結構
CREATE TABLE IF NOT EXISTS `ship_wh_alias` (
  `no` varchar(60) NOT NULL,
  `name` varchar(60) DEFAULT NULL,
  `category` int(11) NOT NULL,
  `type` int(11) NOT NULL,
  `creationTime` int(11) DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`),
  UNIQUE KEY `no` (`no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=DYNAMIC;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb3.ship_wh_contract 結構
CREATE TABLE IF NOT EXISTS `ship_wh_contract` (
  `no` varchar(60) NOT NULL,
  `date` int(11) NOT NULL,
  `ref_no` varchar(60) DEFAULT NULL,
  `sw_alias_no` varchar(60) DEFAULT NULL,
  `displayName` varchar(60) DEFAULT NULL,
  `item_no` varchar(60) NOT NULL,
  `item_name` varchar(60) NOT NULL,
  `item_ref_no` varchar(60) NOT NULL,
  `item_ref_displayName` varchar(60) NOT NULL,
  `category` int(11) DEFAULT NULL,
  `type` int(11) DEFAULT NULL,
  `itemStyle` int(11) DEFAULT NULL,
  `region` int(11) DEFAULT NULL,
  `unit` int(11) DEFAULT NULL,
  `price` double DEFAULT NULL,
  `fee` double DEFAULT NULL,
  `comment` varchar(128) DEFAULT NULL,
  `creationTime` int(11) DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`),
  UNIQUE KEY `no` (`no`,`date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=DYNAMIC;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb3.ship_wh_quotation 結構
CREATE TABLE IF NOT EXISTS `ship_wh_quotation` (
  `no` varchar(60) NOT NULL,
  `date` int(11) NOT NULL,
  `item_no` varchar(60) NOT NULL,
  `item_name` varchar(60) NOT NULL,
  `item_ref_no` varchar(60) NOT NULL,
  `item_ref_displayName` varchar(60) NOT NULL,
  `category` int(11) DEFAULT NULL,
  `type` int(11) DEFAULT NULL,
  `itemStyle` int(11) DEFAULT NULL,
  `region` int(11) DEFAULT NULL,
  `unit` int(11) DEFAULT NULL,
  `price` float DEFAULT NULL,
  `fee` float DEFAULT NULL,
  `comment` varchar(128) DEFAULT NULL,
  `creationTime` int(11) DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`),
  UNIQUE KEY `no` (`no`,`date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=DYNAMIC;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb3.station 結構
CREATE TABLE IF NOT EXISTS `station` (
  `no` varchar(60) NOT NULL,
  `production_line_no` varchar(60) DEFAULT NULL,
  `name` varchar(60) DEFAULT NULL,
  `stage` int(11) DEFAULT NULL,
  `comment` varchar(128) DEFAULT '',
  `creationTime` int(11) DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`),
  UNIQUE KEY `no` (`no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=DYNAMIC;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb3.trans_items 結構
CREATE TABLE IF NOT EXISTS `trans_items` (
  `no` varchar(20) NOT NULL,
  `name` varchar(100) NOT NULL,
  `category` int(11) DEFAULT NULL,
  `attribute` int(11) DEFAULT 0,
  `company_no` varchar(60) NOT NULL,
  `company_displayName` varchar(60) DEFAULT NULL,
  `item_no` varchar(60) DEFAULT NULL,
  `item_name` varchar(60) DEFAULT NULL,
  `comment` varchar(128) DEFAULT NULL,
  `creationTime` int(11) DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`),
  UNIQUE KEY `no` (`no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=DYNAMIC;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb3.trans_items2 結構
CREATE TABLE IF NOT EXISTS `trans_items2` (
  `no` varchar(20) NOT NULL,
  `name` varchar(100) NOT NULL,
  `category` int(11) DEFAULT NULL,
  `attribute` int(11) DEFAULT 0,
  `company_no` varchar(60) NOT NULL,
  `company_displayName` varchar(60) DEFAULT NULL,
  `comment` varchar(128) DEFAULT NULL,
  `creationTime` int(11) DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`),
  UNIQUE KEY `no` (`no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=DYNAMIC;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb3.user_group 結構
CREATE TABLE IF NOT EXISTS `user_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(60) NOT NULL,
  `role` int(11) DEFAULT NULL,
  `users` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`users`)),
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=DYNAMIC;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb3.warehouse_payment 結構
CREATE TABLE IF NOT EXISTS `warehouse_payment` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `no` varchar(60) NOT NULL,
  `group_no` varchar(60) NOT NULL,
  `arapType` int(11) NOT NULL,
  `date` int(11) NOT NULL,
  `record_no` varchar(60) NOT NULL,
  `batch_no` varchar(60) NOT NULL,
  `item_ref_no` varchar(60) NOT NULL,
  `item_ref_displayName` varchar(60) NOT NULL,
  `paymentType` int(11) NOT NULL,
  `month` date NOT NULL,
  `price` double DEFAULT NULL,
  `count` int(11) DEFAULT NULL,
  `days` float DEFAULT NULL,
  `amount` int(11) DEFAULT NULL,
  `addDeleteAmount` int(11) DEFAULT NULL,
  `totalAmount` int(11) DEFAULT NULL,
  `balance` int(11) DEFAULT NULL,
  `creationTime` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `no` (`no`,`date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=DYNAMIC;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb3.warehouse_record 結構
CREATE TABLE IF NOT EXISTS `warehouse_record` (
  `no` varchar(60) NOT NULL,
  `date` int(11) DEFAULT NULL,
  `ref_no` int(11) DEFAULT NULL,
  `batch_no` varchar(60) DEFAULT NULL,
  `sw_alias_no` varchar(20) DEFAULT NULL,
  `sw_alias_name` varchar(60) DEFAULT NULL,
  `item_no` varchar(60) DEFAULT NULL,
  `item_name` varchar(60) DEFAULT NULL,
  `item_ref_no` varchar(60) DEFAULT NULL,
  `item_ref_displayName` varchar(60) DEFAULT NULL,
  `contract_no` varchar(60) DEFAULT NULL,
  `unit` int(11) DEFAULT NULL,
  `inboundTime` int(11) DEFAULT NULL,
  `price` double DEFAULT NULL,
  `count` float DEFAULT NULL,
  `days` float DEFAULT NULL,
  `comment` varchar(128) DEFAULT NULL,
  `creationTime` int(11) DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`),
  UNIQUE KEY `no` (`no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=DYNAMIC;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb3.work_order 結構
CREATE TABLE IF NOT EXISTS `work_order` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `date` int(11) DEFAULT NULL,
  `no` varchar(20) NOT NULL,
  `creator_id` varchar(60) DEFAULT NULL,
  `product_order_no` varchar(60) DEFAULT NULL,
  `aps_no` varchar(60) DEFAULT '',
  `product_no` varchar(60) DEFAULT NULL,
  `product_name` varchar(100) DEFAULT NULL,
  `customer_no` varchar(60) DEFAULT NULL,
  `customer_displayName` varchar(60) DEFAULT NULL,
  `output_item_no` varchar(60) DEFAULT NULL,
  `output_item_name` varchar(100) DEFAULT NULL,
  `production_line_no` varchar(60) DEFAULT NULL,
  `oneProcess` int(11) DEFAULT NULL,
  `secProcess` int(11) DEFAULT NULL,
  `startTime` int(11) DEFAULT NULL,
  `endTime` int(11) DEFAULT NULL,
  `processUnit` int(11) DEFAULT NULL,
  `processTime` int(11) DEFAULT NULL,
  `processCount` float DEFAULT NULL,
  `laborCount` int(11) DEFAULT NULL,
  `laborList` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
  `comment` varchar(128) DEFAULT NULL,
  `creationTime` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `no` (`no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=DYNAMIC;

-- 取消選取資料匯出。

-- 傾印  觸發器 ewdb3.set_time_trigger 結構
SET @OLDTMP_SQL_MODE=@@SQL_MODE, SQL_MODE='STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION';
DELIMITER //
CREATE TRIGGER set_time_trigger
BEFORE INSERT ON payment
FOR EACH ROW
BEGIN
    SET NEW.creationTime = UNIX_TIMESTAMP();
END//
DELIMITER ;
SET SQL_MODE=@OLDTMP_SQL_MODE;

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
