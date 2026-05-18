-- --------------------------------------------------------
-- 主機:                           127.0.0.1
-- 伺服器版本:                        11.4.10-MariaDB - MariaDB Server
-- 伺服器作業系統:                      Win64
-- HeidiSQL 版本:                  12.6.0.6765
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- 傾印 ewdb 的資料庫結構
CREATE DATABASE IF NOT EXISTS `ewdb` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci */;
USE `ewdb`;

-- 傾印  資料表 ewdb.aps_quantity 結構
CREATE TABLE IF NOT EXISTS `aps_quantity` (
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
  PRIMARY KEY (`no`) USING BTREE,
  UNIQUE KEY `product_order_no` (`product_order_no`,`oneProcess`,`secProcess`,`item_no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=DYNAMIC;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb.aps_quantity_item 結構
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

-- 傾印  資料表 ewdb.arap 結構
CREATE TABLE IF NOT EXISTS `arap` (
  `no` varchar(60) NOT NULL,
  `type` int(11) NOT NULL,
  `refCategory` int(11) NOT NULL,
  `ref_no` varchar(60) NOT NULL,
  `ref_sub_no` varchar(60) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '',
  `itemRefCategory` int(11) NOT NULL,
  `item_ref_no` varchar(60) NOT NULL,
  `item_ref_displayName` varchar(60) NOT NULL,
  `paymentType` int(11) NOT NULL,
  `month` date NOT NULL DEFAULT '0000-00-00',
  `amount` double DEFAULT NULL,
  `pendingAmount` double DEFAULT NULL,
  `balance` double DEFAULT NULL,
  `arap_nos` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL,
  `arapAmount` double DEFAULT NULL,
  `invoice` longtext NOT NULL,
  `comment` varchar(128) NOT NULL,
  `creationTime` int(11) DEFAULT NULL,
  PRIMARY KEY (`no`,`type`,`ref_sub_no`,`month`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=DYNAMIC;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb.arap_shipping 結構
CREATE TABLE IF NOT EXISTS `arap_shipping` (
  `no` varchar(60) NOT NULL,
  `type` int(11) NOT NULL,
  `refCategory` int(11) NOT NULL,
  `ref_no` varchar(60) NOT NULL,
  `ref_sub_no` varchar(60) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '',
  `itemRefCategory` int(11) NOT NULL,
  `item_ref_no` varchar(60) NOT NULL,
  `item_ref_displayName` varchar(60) NOT NULL,
  `paymentType` int(11) NOT NULL,
  `month` date NOT NULL DEFAULT '0000-00-00',
  `amount` double DEFAULT NULL,
  `pendingAmount` double DEFAULT NULL,
  `balance` double DEFAULT NULL,
  `arap_nos` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL,
  `arapAmount` double DEFAULT NULL,
  `invoice` longtext NOT NULL,
  `comment` varchar(128) NOT NULL,
  `creationTime` int(11) DEFAULT NULL,
  PRIMARY KEY (`no`,`type`,`ref_sub_no`,`month`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=DYNAMIC;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb.bank_account 結構
CREATE TABLE IF NOT EXISTS `bank_account` (
  `id` varchar(60) DEFAULT NULL,
  `displayName` varchar(60) DEFAULT NULL,
  `name` varchar(60) DEFAULT NULL,
  `branch` varchar(60) DEFAULT NULL,
  `account` varchar(60) DEFAULT NULL,
  `number` varchar(60) NOT NULL,
  `creationTime` int(11) DEFAULT NULL,
  PRIMARY KEY (`number`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb.basic_history 結構
CREATE TABLE IF NOT EXISTS `basic_history` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ref_no` varchar(20) NOT NULL,
  `fieldName` varchar(60) NOT NULL,
  `oldValue` text DEFAULT NULL,
  `newValue` text DEFAULT NULL,
  `modifiedBy` varchar(60) DEFAULT NULL,
  `modifiedAt` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=35 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb.batchno_history 結構
CREATE TABLE IF NOT EXISTS `batchno_history` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ref_no` varchar(20) NOT NULL,
  `fieldName` varchar(60) NOT NULL,
  `oldValue` text DEFAULT NULL,
  `newValue` text DEFAULT NULL,
  `modifiedBy` varchar(60) DEFAULT NULL,
  `modifiedAt` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=DYNAMIC;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb.batchno_serialno 結構
CREATE TABLE IF NOT EXISTS `batchno_serialno` (
  `batch_number` varchar(60) NOT NULL,
  `serialNo` varchar(60) NOT NULL DEFAULT '',
  `ref_order_no` varchar(60) NOT NULL DEFAULT '',
  `warehouse_no` varchar(60) DEFAULT NULL,
  `ref_order_no_category` int(11) DEFAULT NULL,
  `time` int(11) DEFAULT NULL,
  `unit` int(11) DEFAULT NULL,
  `count` float DEFAULT NULL,
  `expectedCount` float DEFAULT 0,
  `validDate` int(11) DEFAULT NULL,
  `updatedTime` int(11) DEFAULT NULL,
  PRIMARY KEY (`serialNo`,`batch_number`,`ref_order_no`) USING BTREE,
  KEY `ref_order_no` (`ref_order_no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=DYNAMIC;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb.batchno_serialno_group 結構
CREATE TABLE IF NOT EXISTS `batchno_serialno_group` (
  `time` int(11) DEFAULT NULL,
  `warehouse_no` varchar(60) DEFAULT NULL,
  `group` varchar(60) NOT NULL,
  `batch_number` varchar(60) NOT NULL,
  `serialNo` varchar(60) NOT NULL,
  `count` float DEFAULT NULL,
  `comment` varchar(60) DEFAULT NULL,
  PRIMARY KEY (`group`,`batch_number`,`serialNo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb.batch_number 結構
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

-- 傾印  資料表 ewdb.bom 結構
CREATE TABLE IF NOT EXISTS `bom` (
  `id` varchar(60) DEFAULT NULL,
  `no` varchar(60) NOT NULL,
  `version` float NOT NULL,
  `date` int(11) DEFAULT NULL,
  `displayName` varchar(60) DEFAULT NULL,
  `unit` int(11) DEFAULT NULL,
  `weight` float DEFAULT NULL,
  `comment` varchar(128) DEFAULT NULL,
  `creationTime` int(11) DEFAULT NULL,
  PRIMARY KEY (`no`,`version`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=DYNAMIC;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb.bom1 結構
CREATE TABLE IF NOT EXISTS `bom1` (
  `id` varchar(60) NOT NULL,
  `parent_no` varchar(60) NOT NULL,
  `parent_name` varchar(60) DEFAULT NULL,
  `child_category` int(11) DEFAULT NULL,
  `child_id` varchar(60) NOT NULL,
  `child_name` varchar(60) DEFAULT NULL,
  `childUnit` int(11) DEFAULT NULL,
  `weight` float NOT NULL DEFAULT 0,
  `expectedLoss` float NOT NULL DEFAULT 0,
  `actualLoss` float NOT NULL DEFAULT 0,
  `processWeight` double DEFAULT NULL,
  `comment` varchar(128) DEFAULT NULL,
  `creationTime` int(11) DEFAULT NULL,
  PRIMARY KEY (`parent_no`,`child_id`,`weight`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb.bom1_number 結構
CREATE TABLE IF NOT EXISTS `bom1_number` (
  `id` varchar(60) DEFAULT NULL,
  `no` varchar(60) NOT NULL,
  `category` int(11) DEFAULT NULL,
  `displayName` varchar(60) DEFAULT NULL,
  `unit` int(11) DEFAULT NULL,
  `weight` float DEFAULT NULL,
  `bom_id` varchar(60) DEFAULT NULL,
  `bom_version` int(11) DEFAULT NULL,
  `comment` varchar(128) DEFAULT NULL,
  `creationTime` int(11) DEFAULT NULL,
  PRIMARY KEY (`no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb.bom2 結構
CREATE TABLE IF NOT EXISTS `bom2` (
  `id` varchar(60) NOT NULL,
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
  `processCount` float DEFAULT NULL,
  `comment` varchar(128) DEFAULT NULL,
  `creationTime` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb.bom2_number 結構
CREATE TABLE IF NOT EXISTS `bom2_number` (
  `id` varchar(60) DEFAULT NULL,
  `no` varchar(60) NOT NULL,
  `category` int(11) DEFAULT NULL,
  `displayName` varchar(60) DEFAULT NULL,
  `unit` int(11) DEFAULT NULL,
  `weight` float DEFAULT NULL,
  `bom_id` varchar(60) DEFAULT NULL,
  `bom_version` int(11) DEFAULT NULL,
  `comment` varchar(128) DEFAULT NULL,
  `creationTime` int(11) DEFAULT NULL,
  PRIMARY KEY (`no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb.bom_copy 結構
CREATE TABLE IF NOT EXISTS `bom_copy` (
  `id` varchar(60) DEFAULT NULL,
  `no` varchar(60) NOT NULL,
  `version` float NOT NULL,
  `date` int(11) DEFAULT NULL,
  `displayName` varchar(60) DEFAULT NULL,
  `unit` int(11) DEFAULT NULL,
  `weight` float DEFAULT NULL,
  `comment` varchar(128) DEFAULT NULL,
  `creationTime` int(11) DEFAULT NULL,
  PRIMARY KEY (`no`,`version`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=DYNAMIC;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb.bom_item 結構
CREATE TABLE IF NOT EXISTS `bom_item` (
  `bom_id` varchar(60) NOT NULL,
  `item_no` varchar(60) NOT NULL,
  `item_name` varchar(60) NOT NULL,
  `unit` int(11) DEFAULT NULL,
  `weight` double DEFAULT NULL,
  `creationTime` int(11) DEFAULT NULL,
  PRIMARY KEY (`item_no`,`bom_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=DYNAMIC;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb.borrower 結構
CREATE TABLE IF NOT EXISTS `borrower` (
  `id` varchar(60) DEFAULT NULL,
  `category` int(11) DEFAULT NULL,
  `name` varchar(100) NOT NULL,
  `payment_id` varchar(60) NOT NULL,
  `comment` varchar(128) DEFAULT NULL,
  `creationTime` int(11) DEFAULT NULL,
  PRIMARY KEY (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb.building 結構
CREATE TABLE IF NOT EXISTS `building` (
  `id` varchar(60) NOT NULL,
  `name` varchar(60) DEFAULT NULL,
  `no` int(11) DEFAULT NULL,
  `floor` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb.company 結構
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
  `bankDisplayName` varchar(60) DEFAULT NULL,
  `bankName` varchar(60) DEFAULT NULL,
  `bankBranch` varchar(60) DEFAULT NULL,
  `bankAccount` varchar(60) DEFAULT NULL,
  `bankNo` varchar(60) DEFAULT NULL,
  `comment` varchar(128) DEFAULT NULL,
  `creationTime` int(11) DEFAULT NULL,
  PRIMARY KEY (`no`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=DYNAMIC;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb.complaints 結構
CREATE TABLE IF NOT EXISTS `complaints` (
  `id` varchar(60) NOT NULL,
  `creator_id` varchar(60) DEFAULT NULL,
  `projectCode` varchar(20) DEFAULT NULL,
  `date` int(11) DEFAULT NULL,
  `customer_id` varchar(60) DEFAULT NULL,
  `customer_displayName` varchar(60) DEFAULT NULL,
  `customer_contactName` varchar(60) DEFAULT NULL,
  `product_id` varchar(60) DEFAULT NULL,
  `product_name` varchar(60) DEFAULT NULL,
  `batch_number` varchar(60) DEFAULT NULL,
  `content` varchar(128) DEFAULT NULL,
  `sales_id` varchar(60) DEFAULT NULL,
  `analysis` varchar(128) DEFAULT NULL,
  `QA_id` varchar(60) DEFAULT NULL,
  `date1` int(11) DEFAULT NULL,
  `reason` varchar(128) DEFAULT NULL,
  `operator1_id` varchar(60) DEFAULT NULL,
  `date2` int(11) DEFAULT NULL,
  `plan` varchar(128) DEFAULT NULL,
  `operator2_id` varchar(60) DEFAULT NULL,
  `date3` int(11) DEFAULT NULL,
  `solution` varchar(128) DEFAULT NULL,
  `response` varchar(128) DEFAULT NULL,
  `processor_id` varchar(60) DEFAULT NULL,
  `date4` int(11) DEFAULT NULL,
  `result` int(11) DEFAULT NULL,
  `resultTime` int(11) DEFAULT NULL,
  `comment` varchar(128) DEFAULT NULL,
  `creationTime` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb.contract 結構
CREATE TABLE IF NOT EXISTS `contract` (
  `no` varchar(20) NOT NULL,
  `date` int(11) NOT NULL,
  `ref_no` varchar(60) DEFAULT NULL,
  `creator_id` varchar(60) DEFAULT NULL,
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
  `payment_id` varchar(60) DEFAULT NULL,
  `price` double DEFAULT NULL,
  `shippingPrice` double DEFAULT NULL,
  `unitConversion` double DEFAULT NULL,
  `comment` varchar(128) DEFAULT '""',
  `creationTime` int(11) DEFAULT NULL,
  PRIMARY KEY (`no`,`date`) USING BTREE,
  KEY `customer_id` (`item_ref_no`) USING BTREE,
  KEY `product_id` (`item_no`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=DYNAMIC;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb.customer 結構
CREATE TABLE IF NOT EXISTS `customer` (
  `id` varchar(60) DEFAULT NULL,
  `no` varchar(60) NOT NULL,
  `category` int(11) DEFAULT NULL,
  `businessNo` varchar(20) NOT NULL,
  `displayName` varchar(60) DEFAULT NULL,
  `name` varchar(60) DEFAULT NULL,
  `address` varchar(100) DEFAULT NULL,
  `phone` varchar(100) DEFAULT NULL,
  `fax` varchar(20) DEFAULT NULL,
  `contactName` varchar(60) DEFAULT NULL,
  `contactPhone` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`contactPhone`)),
  `contactTitle` varchar(60) DEFAULT NULL,
  `contactEmail` varchar(60) DEFAULT NULL,
  `payment_id` varchar(60) DEFAULT NULL,
  `bank_account_id` varchar(60) DEFAULT NULL,
  `comment` varchar(128) DEFAULT NULL,
  `creationTime` int(11) DEFAULT NULL,
  PRIMARY KEY (`no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb.device 結構
CREATE TABLE IF NOT EXISTS `device` (
  `no` varchar(60) NOT NULL,
  `hardwareId` varchar(128) NOT NULL,
  `name` varchar(60) NOT NULL,
  `role` int(11) DEFAULT NULL,
  `comment` varchar(128) NOT NULL,
  `creationTime` int(11) DEFAULT NULL,
  PRIMARY KEY (`hardwareId`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=DYNAMIC;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb.device_log 結構
CREATE TABLE IF NOT EXISTS `device_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `hardwareId` varchar(128) NOT NULL,
  `role` int(11) DEFAULT NULL,
  `action` int(11) DEFAULT NULL,
  `data` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL,
  `creationTime` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=77 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=DYNAMIC;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb.employee 結構
CREATE TABLE IF NOT EXISTS `employee` (
  `no` varchar(20) NOT NULL,
  `name` varchar(60) DEFAULT NULL,
  `type` int(11) DEFAULT NULL,
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
  PRIMARY KEY (`no`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb.employee_delta 結構
CREATE TABLE IF NOT EXISTS `employee_delta` (
  `id` varchar(60) NOT NULL,
  `date` int(11) DEFAULT NULL,
  `employee_id` varchar(60) DEFAULT NULL,
  `data` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`data`)),
  `creationTime` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb.enterprise 結構
CREATE TABLE IF NOT EXISTS `enterprise` (
  `no` varchar(60) NOT NULL,
  `businessNo` varchar(20) NOT NULL,
  `displayName` varchar(60) DEFAULT NULL,
  `name` varchar(60) DEFAULT NULL,
  `address` varchar(100) DEFAULT NULL,
  `phone` varchar(100) DEFAULT NULL,
  `fax` varchar(20) DEFAULT NULL,
  `department` int(11) DEFAULT NULL,
  `lar` varchar(60) DEFAULT NULL,
  `comment` varchar(128) DEFAULT NULL,
  `creationTime` int(11) DEFAULT NULL,
  PRIMARY KEY (`no`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=DYNAMIC;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb.equipment 結構
CREATE TABLE IF NOT EXISTS `equipment` (
  `no` varchar(60) NOT NULL,
  `station_no` varchar(60) DEFAULT '',
  `name` varchar(60) DEFAULT '',
  `model` varchar(60) DEFAULT '',
  `manufacturer` varchar(60) DEFAULT '',
  `purchaseDate` int(11) DEFAULT NULL,
  `appearance` varchar(128) DEFAULT '',
  `comment` varchar(128) DEFAULT '',
  `creationTime` int(11) DEFAULT NULL,
  PRIMARY KEY (`no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb.expense 結構
CREATE TABLE IF NOT EXISTS `expense` (
  `id` varchar(60) DEFAULT NULL,
  `no` varchar(20) DEFAULT NULL,
  `category` int(11) DEFAULT NULL,
  `type` int(11) DEFAULT NULL,
  `name` varchar(100) NOT NULL,
  `unit` int(11) DEFAULT NULL,
  `vendor_id` varchar(60) NOT NULL,
  `vendor_displayName` varchar(60) DEFAULT NULL,
  `comment` varchar(128) DEFAULT NULL,
  `creationTime` int(11) DEFAULT NULL,
  PRIMARY KEY (`name`,`vendor_id`),
  KEY `idx_expense_id` (`id`),
  KEY `vendor_id` (`vendor_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb.expense_order 結構
CREATE TABLE IF NOT EXISTS `expense_order` (
  `id` varchar(60) NOT NULL,
  `no` varchar(20) DEFAULT NULL,
  `creator_id` varchar(60) DEFAULT NULL,
  `category` int(11) DEFAULT NULL,
  `date` int(11) DEFAULT NULL,
  `vendor_id` varchar(20) DEFAULT NULL,
  `vendor_displayName` varchar(60) DEFAULT NULL,
  `expense_id` varchar(60) DEFAULT NULL,
  `expense_name` varchar(60) DEFAULT NULL,
  `unit` int(11) DEFAULT NULL,
  `price` float DEFAULT NULL,
  `purchaseCount` float DEFAULT NULL,
  `receivedCount` float DEFAULT NULL,
  `count` float DEFAULT NULL,
  `amount` double DEFAULT NULL,
  `expectedDate` int(11) DEFAULT NULL,
  `result` int(11) DEFAULT NULL,
  `result_time` int(11) DEFAULT NULL,
  `comment` varchar(128) DEFAULT NULL,
  `creationTime` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `no` (`no`),
  KEY `vendor_id` (`vendor_id`),
  KEY `expense_id` (`expense_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb.factory 結構
CREATE TABLE IF NOT EXISTS `factory` (
  `no` varchar(60) NOT NULL,
  `region` varchar(60) DEFAULT NULL,
  `location` varchar(60) DEFAULT NULL,
  `comment` varchar(60) DEFAULT NULL,
  `creationTime` int(11) DEFAULT NULL,
  PRIMARY KEY (`no`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=DYNAMIC;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb.goods 結構
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
  PRIMARY KEY (`no`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=DYNAMIC;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb.goods_receipt_note 結構
CREATE TABLE IF NOT EXISTS `goods_receipt_note` (
  `id` varchar(60) NOT NULL,
  `no` varchar(20) NOT NULL,
  `creator_id` varchar(60) DEFAULT NULL,
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
  `result` int(11) DEFAULT NULL,
  `resultTime` int(11) DEFAULT NULL,
  `comment` varchar(128) DEFAULT NULL,
  `creationTime` int(11) DEFAULT NULL,
  PRIMARY KEY (`no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb.hourly_wage 結構
CREATE TABLE IF NOT EXISTS `hourly_wage` (
  `id` varchar(60) DEFAULT NULL,
  `date` int(11) NOT NULL AUTO_INCREMENT,
  `monthly` int(11) DEFAULT NULL,
  `hourly` int(11) DEFAULT NULL,
  `creationTime` int(11) DEFAULT NULL,
  PRIMARY KEY (`date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb.inproduct 結構
CREATE TABLE IF NOT EXISTS `inproduct` (
  `id` varchar(60) DEFAULT NULL,
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
  `package3Unit` int(11) DEFAULT NULL,
  `package34Count` float DEFAULT NULL,
  `package4Unit` int(11) DEFAULT NULL,
  `version` varchar(60) DEFAULT NULL,
  `version_history` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`version_history`)),
  `comment` varchar(128) DEFAULT NULL,
  `creationTime` int(11) DEFAULT NULL,
  PRIMARY KEY (`no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb.inproduct_bom_spec 結構
CREATE TABLE IF NOT EXISTS `inproduct_bom_spec` (
  `id` varchar(60) DEFAULT NULL,
  `inproduct_id` varchar(60) NOT NULL,
  `inproduct_no` varchar(60) NOT NULL,
  `category` int(11) DEFAULT NULL,
  `item_no` varchar(60) NOT NULL,
  `item_version` int(11) NOT NULL DEFAULT 0,
  `bom12_no` varchar(60) NOT NULL,
  `count` int(11) DEFAULT NULL,
  `unit` int(11) DEFAULT NULL,
  `weight` float DEFAULT NULL,
  PRIMARY KEY (`item_no`,`inproduct_no`,`item_version`,`bom12_no`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb.inproduct_price 結構
CREATE TABLE IF NOT EXISTS `inproduct_price` (
  `id` varchar(60) DEFAULT NULL,
  `item_no` varchar(60) NOT NULL,
  `date` int(11) NOT NULL,
  `warehouseUnit` int(11) DEFAULT NULL,
  `warehousePrice` double DEFAULT NULL,
  `costUnit` int(11) DEFAULT NULL,
  `costPrice` double DEFAULT NULL,
  `comment` varchar(128) DEFAULT NULL,
  `creationTime` int(11) DEFAULT NULL,
  PRIMARY KEY (`date`,`item_no`) USING BTREE,
  KEY `item_id` (`item_no`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb.insurance 結構
CREATE TABLE IF NOT EXISTS `insurance` (
  `id` varchar(60) DEFAULT NULL,
  `employee_id` varchar(60) NOT NULL,
  `date` int(11) NOT NULL,
  `laborGrade` int(11) DEFAULT NULL,
  `laborEmployeePay` int(11) DEFAULT NULL,
  `laborEmployerPay` int(11) DEFAULT NULL,
  `laborPension` int(11) DEFAULT NULL,
  `healthGrade` int(11) DEFAULT NULL,
  `healthEmployeePay` int(11) DEFAULT NULL,
  `healthEmployerPay` int(11) DEFAULT NULL,
  `accident` int(11) DEFAULT NULL,
  `creationTime` int(11) DEFAULT NULL,
  PRIMARY KEY (`employee_id`,`date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb.inventory_delta 結構
CREATE TABLE IF NOT EXISTS `inventory_delta` (
  `id` varchar(60) NOT NULL,
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
  PRIMARY KEY (`warehouse_no`,`date`,`timezone`,`specified_no`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=DYNAMIC;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb.inventory_item_month_statistic 結構
CREATE TABLE IF NOT EXISTS `inventory_item_month_statistic` (
  `id` varchar(60) NOT NULL,
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
  PRIMARY KEY (`warehouse_no`,`date`,`timezone`,`specified_no`,`specified_ref_no`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=DYNAMIC;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb.inventory_month_statistic 結構
CREATE TABLE IF NOT EXISTS `inventory_month_statistic` (
  `id` varchar(60) NOT NULL,
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
  PRIMARY KEY (`warehouse_no`,`date`,`timezone`,`category`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=DYNAMIC;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb.inventory_order 結構
CREATE TABLE IF NOT EXISTS `inventory_order` (
  `no` varchar(60) NOT NULL,
  `creator_id` varchar(60) DEFAULT NULL,
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
  `result` int(11) DEFAULT NULL,
  `resultTime` int(11) DEFAULT NULL,
  `comment` varchar(128) DEFAULT NULL,
  `creationTime` int(11) DEFAULT NULL,
  PRIMARY KEY (`no`) USING BTREE,
  KEY `inventory_order_ibfk_3` (`item_no`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb.inventory_record 結構
CREATE TABLE IF NOT EXISTS `inventory_record` (
  `id` varchar(60) NOT NULL,
  `creator_id` varchar(60) DEFAULT NULL,
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
  PRIMARY KEY (`id`) USING BTREE,
  KEY `inventory_record_ibfk_1` (`warehouse_no`,`ref_no`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb.item_expense 結構
CREATE TABLE IF NOT EXISTS `item_expense` (
  `id` varchar(60) DEFAULT NULL,
  `item_id` varchar(60) NOT NULL,
  `date` int(11) DEFAULT NULL,
  `quantity` float DEFAULT NULL,
  `unit` int(11) DEFAULT NULL,
  `price` double DEFAULT NULL,
  `creationTime` int(11) DEFAULT NULL,
  PRIMARY KEY (`item_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb.item_history 結構
CREATE TABLE IF NOT EXISTS `item_history` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ref_no` varchar(20) NOT NULL,
  `fieldName` varchar(60) NOT NULL,
  `oldValue` text DEFAULT NULL,
  `newValue` text DEFAULT NULL,
  `modifiedBy` varchar(60) DEFAULT NULL,
  `modifiedAt` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=DYNAMIC;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb.item_hours 結構
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

-- 傾印  資料表 ewdb.item_loss 結構
CREATE TABLE IF NOT EXISTS `item_loss` (
  `item_no` varchar(60) NOT NULL,
  `itemCategory` int(11) DEFAULT NULL,
  `date` date NOT NULL,
  `unit` int(11) DEFAULT NULL,
  `estValue` double DEFAULT NULL,
  `value` double DEFAULT NULL,
  `creationTime` int(11) DEFAULT NULL,
  PRIMARY KEY (`item_no`,`date`) USING BTREE,
  KEY `item_no` (`item_no`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=DYNAMIC;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb.item_price 結構
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
  PRIMARY KEY (`item_no`,`date`) USING BTREE,
  KEY `item_no` (`item_no`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=DYNAMIC;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb.item_shipping 結構
CREATE TABLE IF NOT EXISTS `item_shipping` (
  `id` varchar(60) DEFAULT NULL,
  `item_id` varchar(60) NOT NULL,
  `shipping_price_id` varchar(20) NOT NULL,
  `unitConversion1` float DEFAULT NULL,
  `unitConversion2` float DEFAULT NULL,
  `creationTime` int(11) DEFAULT NULL,
  PRIMARY KEY (`item_id`,`shipping_price_id`),
  KEY `shipping_price_id` (`shipping_price_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb.item_warehouse 結構
CREATE TABLE IF NOT EXISTS `item_warehouse` (
  `id` varchar(60) DEFAULT NULL,
  `item_id` varchar(60) NOT NULL,
  `warehouse_price_id` varchar(60) NOT NULL,
  `unitConversion1` float DEFAULT NULL,
  `unitConversion2` float DEFAULT NULL,
  `creationTime` int(11) DEFAULT NULL,
  PRIMARY KEY (`item_id`,`warehouse_price_id`),
  KEY `warehouse_price_id` (`warehouse_price_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb.labor_wage 結構
CREATE TABLE IF NOT EXISTS `labor_wage` (
  `id` varchar(60) DEFAULT NULL,
  `date` int(11) NOT NULL,
  `type` int(11) NOT NULL,
  `level` int(11) NOT NULL,
  `hourly` int(11) DEFAULT NULL,
  `creationTime` int(11) DEFAULT NULL,
  PRIMARY KEY (`date`,`type`,`level`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=DYNAMIC;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb.leave_ 結構
CREATE TABLE IF NOT EXISTS `leave_` (
  `id` varchar(60) DEFAULT NULL,
  `employee_id` varchar(60) NOT NULL,
  `date` int(11) NOT NULL,
  `type` int(11) DEFAULT NULL,
  `annual` int(11) DEFAULT NULL,
  `makeup` int(11) DEFAULT NULL,
  `creationTime` int(11) DEFAULT NULL,
  PRIMARY KEY (`employee_id`,`date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb.leave_delta 結構
CREATE TABLE IF NOT EXISTS `leave_delta` (
  `id` varchar(60) NOT NULL,
  `employee_id` varchar(60) DEFAULT NULL,
  `date` int(11) DEFAULT NULL,
  `type` int(11) DEFAULT NULL,
  `hours` int(11) DEFAULT NULL,
  `comment` varchar(128) DEFAULT NULL,
  `creationTime` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb.material 結構
CREATE TABLE IF NOT EXISTS `material` (
  `id` varchar(60) DEFAULT NULL,
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
  `package1Unit` int(11) DEFAULT NULL,
  `package12Count` float DEFAULT NULL,
  `package2Unit` int(11) DEFAULT NULL,
  `package23Count` float DEFAULT NULL,
  `package3Unit` int(11) DEFAULT NULL,
  `package34Count` float DEFAULT NULL,
  `package4Unit` int(11) DEFAULT NULL,
  `specUnitType` int(11) DEFAULT NULL,
  `specUnit` int(11) DEFAULT NULL,
  `specValue` float DEFAULT NULL,
  `comment` varchar(128) DEFAULT NULL,
  `creationTime` int(11) DEFAULT NULL,
  PRIMARY KEY (`no`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=DYNAMIC;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb.material_price 結構
CREATE TABLE IF NOT EXISTS `material_price` (
  `id` varchar(60) DEFAULT NULL,
  `item_no` varchar(60) NOT NULL,
  `date` int(11) NOT NULL,
  `purchaseCount` float NOT NULL,
  `purchaseUnit` int(11) DEFAULT NULL,
  `purchasePrice` double DEFAULT NULL,
  `purchaseWeightUnit` float DEFAULT NULL,
  `purchaseLengthUnit` float DEFAULT NULL,
  `purchaseCountUnit` float DEFAULT NULL,
  `warehouseUnitWeight` int(11) DEFAULT NULL,
  `warehouseUnitLength` int(11) DEFAULT NULL,
  `warehouseUnitCount` int(11) DEFAULT NULL,
  `warehousePriceWeight` double DEFAULT NULL,
  `warehousePriceLength` double DEFAULT NULL,
  `warehousePriceCount` double DEFAULT NULL,
  `costUnitWeight` int(11) DEFAULT NULL,
  `costUnitLength` int(11) DEFAULT NULL,
  `costUnitCount` int(11) DEFAULT NULL,
  `costPriceWeight` double DEFAULT NULL,
  `costPriceLength` double DEFAULT NULL,
  `costPriceCount` double DEFAULT NULL,
  `creationTime` int(11) DEFAULT NULL,
  PRIMARY KEY (`item_no`,`date`) USING BTREE,
  KEY `item_no` (`item_no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb.member 結構
CREATE TABLE IF NOT EXISTS `member` (
  `user_no` varchar(60) NOT NULL,
  `account` varchar(60) NOT NULL,
  `password` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`user_no`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb.order_item_month_statistic 結構
CREATE TABLE IF NOT EXISTS `order_item_month_statistic` (
  `id` varchar(60) NOT NULL,
  `date` date NOT NULL,
  `timezone` varchar(60) NOT NULL,
  `kind` int(11) NOT NULL,
  `category` int(11) NOT NULL,
  `subCategory` int(11) NOT NULL,
  `type` int(11) NOT NULL,
  `specified_no` varchar(60) NOT NULL,
  `specified_name` varchar(60) NOT NULL,
  `payment` double DEFAULT NULL,
  `amount` double DEFAULT NULL,
  `creationTime` int(11) DEFAULT NULL,
  PRIMARY KEY (`date`,`specified_no`,`kind`,`category`,`subCategory`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=DYNAMIC;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb.order_payment 結構
CREATE TABLE IF NOT EXISTS `order_payment` (
  `id` varchar(60) NOT NULL,
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
  `count` double DEFAULT NULL,
  `amount` double DEFAULT NULL,
  `addDeleteAmount` int(11) DEFAULT NULL,
  `totalAmount` double DEFAULT NULL,
  `balance` double DEFAULT NULL,
  `creationTime` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=DYNAMIC;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb.output_product_order 結構
CREATE TABLE IF NOT EXISTS `output_product_order` (
  `id` varchar(60) NOT NULL,
  `no` varchar(20) DEFAULT NULL,
  `creator_id` varchar(60) DEFAULT NULL,
  `work_order_id` varchar(60) DEFAULT NULL,
  `date` int(11) DEFAULT NULL,
  `item_id` varchar(60) DEFAULT NULL,
  `item_name` varchar(60) DEFAULT NULL,
  `batch_number` varchar(60) DEFAULT NULL,
  `unit` int(11) DEFAULT NULL,
  `count` float DEFAULT NULL,
  `comment` varchar(128) DEFAULT NULL,
  `creationTime` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb.overtime 結構
CREATE TABLE IF NOT EXISTS `overtime` (
  `id` varchar(60) DEFAULT NULL,
  `employee_id` varchar(60) NOT NULL,
  `date` int(11) NOT NULL,
  `type` int(11) DEFAULT NULL,
  `hours` int(11) DEFAULT NULL,
  `comment` varchar(128) DEFAULT NULL,
  `creationTime` int(11) DEFAULT NULL,
  PRIMARY KEY (`employee_id`,`date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb.payment 結構
CREATE TABLE IF NOT EXISTS `payment` (
  `id` varchar(60) NOT NULL,
  `type` int(11) DEFAULT NULL,
  `source` int(11) DEFAULT NULL,
  `date` int(11) NOT NULL,
  `period` int(11) NOT NULL,
  `creationTime` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb.payment_history 結構
CREATE TABLE IF NOT EXISTS `payment_history` (
  `id` varchar(60) NOT NULL,
  `reference_id` varchar(60) DEFAULT NULL,
  `payment_id` varchar(60) DEFAULT NULL,
  `creationTime` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `payment_id` (`payment_id`),
  KEY `reference_id` (`reference_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb.pl_item_capacity 結構
CREATE TABLE IF NOT EXISTS `pl_item_capacity` (
  `no` varchar(60) NOT NULL,
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
  `hours` double DEFAULT NULL,
  `count` double DEFAULT NULL,
  `unit` int(11) DEFAULT NULL,
  `hourlyOutput` double DEFAULT NULL,
  `price` double DEFAULT NULL,
  `rawMaterialCost` double DEFAULT NULL,
  `materialCost` double DEFAULT NULL,
  `laborCost` double DEFAULT NULL,
  `creationTime` int(11) DEFAULT NULL,
  PRIMARY KEY (`no`) USING BTREE,
  UNIQUE KEY `pl_no` (`pl_no`,`month`,`item_no`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=DYNAMIC;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb.pl_item_loss 結構
CREATE TABLE IF NOT EXISTS `pl_item_loss` (
  `no` varchar(60) NOT NULL,
  `month` date NOT NULL,
  `pl_item_capacity_no` varchar(60) NOT NULL,
  `item_no` varchar(60) DEFAULT NULL,
  `item_name` varchar(60) NOT NULL,
  `itemCategory` int(11) NOT NULL,
  `itemSubCategory` int(11) NOT NULL,
  `weightRatio` double DEFAULT NULL,
  `lossRate` double DEFAULT NULL,
  `creationTime` int(11) DEFAULT NULL,
  PRIMARY KEY (`no`) USING BTREE,
  UNIQUE KEY `pl_item_capacity_no` (`pl_item_capacity_no`,`item_no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=DYNAMIC;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb.pl_man_capacity 結構
CREATE TABLE IF NOT EXISTS `pl_man_capacity` (
  `no` varchar(60) NOT NULL,
  `month` date NOT NULL,
  `pl_no` varchar(60) NOT NULL,
  `pl_name` varchar(60) NOT NULL,
  `productCount` int(11) NOT NULL,
  `laborCount` int(11) NOT NULL,
  `unit` int(11) NOT NULL,
  `hourlyOutput` double NOT NULL,
  `creationTime` int(11) DEFAULT NULL,
  PRIMARY KEY (`no`) USING BTREE,
  UNIQUE KEY `month` (`month`,`pl_no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=DYNAMIC;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb.process 結構
CREATE TABLE IF NOT EXISTS `process` (
  `no` varchar(60) NOT NULL,
  `oneProcess` int(11) DEFAULT NULL,
  `secProcess` int(11) DEFAULT NULL,
  `comment` varchar(128) DEFAULT '',
  `creationTime` int(11) DEFAULT NULL,
  PRIMARY KEY (`no`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=DYNAMIC;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb.process_capacity 結構
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

-- 傾印  資料表 ewdb.process_flow 結構
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

-- 傾印  資料表 ewdb.process_labor 結構
CREATE TABLE IF NOT EXISTS `process_labor` (
  `date` int(11) DEFAULT NULL,
  `creator_id` varchar(60) DEFAULT NULL,
  `work_order_no` varchar(60) NOT NULL,
  `employee_no` varchar(60) NOT NULL,
  `production_line_no` varchar(60) DEFAULT NULL,
  `station_no` varchar(60) DEFAULT NULL,
  PRIMARY KEY (`work_order_no`,`employee_no`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=DYNAMIC;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb.process_order 結構
CREATE TABLE IF NOT EXISTS `process_order` (
  `no` varchar(20) NOT NULL,
  `creator_id` varchar(60) DEFAULT NULL,
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
  PRIMARY KEY (`no`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=DYNAMIC;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb.process_price 結構
CREATE TABLE IF NOT EXISTS `process_price` (
  `id` varchar(60) DEFAULT NULL,
  `oneProcess` int(11) NOT NULL,
  `secProcess` int(11) NOT NULL,
  `displayName` varchar(60) NOT NULL,
  `process_price_record_id` varchar(60) DEFAULT NULL,
  `comment` varchar(128) DEFAULT NULL,
  `creationTime` int(11) DEFAULT NULL,
  PRIMARY KEY (`oneProcess`,`secProcess`,`displayName`),
  KEY `idx_process_price_id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb.process_price_record 結構
CREATE TABLE IF NOT EXISTS `process_price_record` (
  `id` varchar(60) NOT NULL,
  `process_price_id` varchar(60) DEFAULT NULL,
  `date` int(11) DEFAULT NULL,
  `processQuantity` float DEFAULT NULL,
  `processUnit` int(11) DEFAULT NULL,
  `processPrice` double DEFAULT NULL,
  `creationTime` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_process_price_item_id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb.product 結構
CREATE TABLE IF NOT EXISTS `product` (
  `id` varchar(60) DEFAULT NULL,
  `no` varchar(20) NOT NULL,
  `category` int(11) DEFAULT NULL,
  `name` varchar(100) NOT NULL,
  `customer_no` varchar(60) NOT NULL,
  `customer_displayName` varchar(60) DEFAULT NULL,
  `cost_no` varchar(60) DEFAULT NULL,
  `loss_no` varchar(60) DEFAULT NULL,
  `unitShipping` int(11) DEFAULT NULL,
  `unitWarehouse` int(11) DEFAULT NULL,
  `unitProduct` int(11) DEFAULT NULL,
  `package1Unit` int(11) DEFAULT NULL,
  `package12Count` float DEFAULT NULL,
  `package2Unit` int(11) DEFAULT NULL,
  `package23Count` float DEFAULT NULL,
  `version` int(11) DEFAULT NULL,
  `comment` varchar(128) DEFAULT NULL,
  `creationTime` int(11) DEFAULT NULL,
  PRIMARY KEY (`no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb.production_data 結構
CREATE TABLE IF NOT EXISTS `production_data` (
  `id` varchar(60) DEFAULT NULL,
  `creator_id` varchar(60) DEFAULT NULL,
  `work_order_no` varchar(60) NOT NULL,
  `product_order_no` varchar(60) DEFAULT NULL,
  `customer_no` varchar(60) DEFAULT NULL,
  `customer_displayName` varchar(60) DEFAULT NULL,
  `product_no` varchar(60) DEFAULT NULL,
  `product_name` varchar(100) DEFAULT NULL,
  `date` int(11) DEFAULT NULL,
  `product_line_no` varchar(60) DEFAULT NULL,
  `oneProcess` int(11) DEFAULT NULL,
  `secProcess` int(11) DEFAULT NULL,
  `preStartTime` int(11) NOT NULL,
  `preEndTime` int(11) NOT NULL,
  `postStartTime` int(11) NOT NULL,
  `postEndTime` int(11) NOT NULL,
  `item_no` varchar(60) DEFAULT NULL,
  `item_name` varchar(100) DEFAULT NULL,
  `unit` int(11) DEFAULT NULL,
  `count` float DEFAULT NULL,
  `materialLoss` float DEFAULT NULL,
  `grossWeight` float DEFAULT NULL,
  `comment` varchar(128) DEFAULT NULL,
  `creationTime` int(11) DEFAULT NULL,
  PRIMARY KEY (`work_order_no`,`preStartTime`,`preEndTime`,`postStartTime`,`postEndTime`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=DYNAMIC;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb.production_data_input 結構
CREATE TABLE IF NOT EXISTS `production_data_input` (
  `id` varchar(60) NOT NULL,
  `production_data_id` varchar(60) NOT NULL,
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
  `avgLoss` float DEFAULT NULL,
  `comment` varchar(128) DEFAULT NULL,
  PRIMARY KEY (`batch_number`,`action`,`serial_no`,`group`,`work_order_no`,`item_no`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=DYNAMIC;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb.production_data_labor 結構
CREATE TABLE IF NOT EXISTS `production_data_labor` (
  `id` varchar(60) NOT NULL,
  `production_data_id` varchar(60) NOT NULL,
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
  PRIMARY KEY (`work_order_no`,`employee_no`,`startTime`,`endTime`,`action`,`stationStage`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=DYNAMIC;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb.production_data_machine 結構
CREATE TABLE IF NOT EXISTS `production_data_machine` (
  `id` varchar(60) NOT NULL,
  `production_data_id` varchar(60) NOT NULL,
  `work_order_no` varchar(60) NOT NULL,
  `equipment_no` varchar(60) NOT NULL,
  `equipment_name` varchar(100) DEFAULT NULL,
  `time` int(11) DEFAULT NULL,
  `action` int(11) NOT NULL,
  `temperature` float DEFAULT NULL,
  `speed` float DEFAULT NULL,
  `creationTime` int(11) DEFAULT NULL,
  PRIMARY KEY (`work_order_no`,`equipment_no`,`action`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=DYNAMIC;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb.production_data_output 結構
CREATE TABLE IF NOT EXISTS `production_data_output` (
  `id` varchar(60) NOT NULL,
  `production_data_id` varchar(60) NOT NULL,
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
  PRIMARY KEY (`batch_number`,`serial_no`,`group`,`work_order_no`,`item_no`,`action`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=DYNAMIC;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb.production_data_reuse 結構
CREATE TABLE IF NOT EXISTS `production_data_reuse` (
  `id` varchar(60) NOT NULL,
  `production_data_id` varchar(60) NOT NULL,
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
  PRIMARY KEY (`batch_number`,`serial_no`,`work_order_no`,`item_no`,`category`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=DYNAMIC;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb.production_line 結構
CREATE TABLE IF NOT EXISTS `production_line` (
  `no` varchar(60) NOT NULL,
  `name` varchar(60) NOT NULL,
  `process_no` varchar(60) NOT NULL,
  `oneProcess` int(11) DEFAULT NULL,
  `secProcess` int(11) DEFAULT NULL,
  `factory_no` varchar(60) DEFAULT NULL,
  `location` varchar(60) DEFAULT NULL,
  `equipment_id` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
  `capacityUnit` int(11) DEFAULT NULL,
  `capacity` float DEFAULT NULL,
  `laborCount` int(11) DEFAULT NULL,
  `laborEfficiency` float DEFAULT NULL,
  `comment` varchar(128) DEFAULT NULL,
  `creationTime` int(11) DEFAULT NULL,
  PRIMARY KEY (`no`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=DYNAMIC;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb.production_schedule 結構
CREATE TABLE IF NOT EXISTS `production_schedule` (
  `id` varchar(60) NOT NULL,
  `groupNo` varchar(60) DEFAULT NULL,
  `product_order_id` varchar(60) DEFAULT NULL,
  `production_line_id` varchar(60) DEFAULT NULL,
  `work_order_id` varchar(60) DEFAULT NULL,
  `date` int(11) DEFAULT NULL,
  `type` int(11) DEFAULT NULL,
  `startTime` int(11) DEFAULT NULL,
  `endTime` int(11) DEFAULT NULL,
  `unit` int(11) DEFAULT NULL,
  `count` float DEFAULT NULL,
  `creationTime` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `product_order_id` (`product_order_id`),
  KEY `production_line_id` (`production_line_id`),
  KEY `work_order_id` (`work_order_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb.product_bom_spec 結構
CREATE TABLE IF NOT EXISTS `product_bom_spec` (
  `id` varchar(60) NOT NULL,
  `product_id` varchar(60) NOT NULL,
  `product_no` varchar(60) NOT NULL,
  `product_version` int(11) NOT NULL,
  `level` int(11) DEFAULT NULL,
  `bom2_no` varchar(60) NOT NULL,
  `count` int(11) DEFAULT NULL,
  `unit` int(11) DEFAULT NULL,
  `weight` float DEFAULT NULL,
  PRIMARY KEY (`bom2_no`,`product_no`,`product_version`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=DYNAMIC;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb.product_order 結構
CREATE TABLE IF NOT EXISTS `product_order` (
  `id` varchar(60) DEFAULT NULL,
  `no` varchar(20) NOT NULL,
  `creator_id` varchar(60) DEFAULT NULL,
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
  `result` int(11) DEFAULT NULL,
  `resultTime` int(11) DEFAULT NULL,
  `comment` varchar(128) DEFAULT NULL,
  `creationTime` int(11) DEFAULT NULL,
  PRIMARY KEY (`no`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=DYNAMIC;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb.product_price 結構
CREATE TABLE IF NOT EXISTS `product_price` (
  `id` varchar(60) DEFAULT NULL,
  `item_no` varchar(60) NOT NULL,
  `date` int(11) NOT NULL,
  `warehouseUnit` int(11) DEFAULT NULL,
  `warehousePrice` double DEFAULT NULL,
  `costUnit` int(11) DEFAULT NULL,
  `costPrice` double DEFAULT NULL,
  `comment` varchar(128) DEFAULT NULL,
  `creationTime` int(11) DEFAULT NULL,
  PRIMARY KEY (`item_no`,`date`) USING BTREE,
  KEY `item_id` (`item_no`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb.product_process 結構
CREATE TABLE IF NOT EXISTS `product_process` (
  `no` varchar(60) NOT NULL,
  `item_no` varchar(60) DEFAULT NULL,
  `version` int(11) DEFAULT NULL,
  `date` int(11) DEFAULT NULL,
  PRIMARY KEY (`no`) USING BTREE,
  UNIQUE KEY `item_no` (`item_no`,`version`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb.product_process_price 結構
CREATE TABLE IF NOT EXISTS `product_process_price` (
  `id` varchar(60) NOT NULL,
  `item_id` varchar(60) DEFAULT NULL,
  `process_price_id` varchar(60) DEFAULT NULL,
  `creationTime` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_product_process_price_id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb.product_sellprice 結構
CREATE TABLE IF NOT EXISTS `product_sellprice` (
  `id` varchar(60) DEFAULT NULL,
  `item_no` varchar(20) NOT NULL,
  `quotation_no` varchar(20) NOT NULL,
  `date` int(11) DEFAULT NULL,
  `quantity` int(11) DEFAULT NULL,
  `unit` int(11) DEFAULT NULL,
  `price` float DEFAULT NULL,
  `comment` varchar(128) DEFAULT NULL,
  `creationTime` int(11) DEFAULT NULL,
  PRIMARY KEY (`item_no`,`quotation_no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb.product_spec 結構
CREATE TABLE IF NOT EXISTS `product_spec` (
  `id` varchar(60) NOT NULL,
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
  PRIMARY KEY (`product_no`,`product_version`,`item_no`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb.product_ver 結構
CREATE TABLE IF NOT EXISTS `product_ver` (
  `no` varchar(60) NOT NULL,
  `item_no` varchar(60) DEFAULT NULL,
  `version` float NOT NULL,
  `date` int(11) DEFAULT NULL,
  PRIMARY KEY (`no`) USING BTREE,
  UNIQUE KEY `version` (`version`,`item_no`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=DYNAMIC;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb.ps_month_statistic 結構
CREATE TABLE IF NOT EXISTS `ps_month_statistic` (
  `id` varchar(60) NOT NULL,
  `year` int(11) NOT NULL,
  `month` int(11) NOT NULL,
  `kind` int(11) NOT NULL,
  `category` int(11) NOT NULL,
  `specified_no` varchar(60) NOT NULL,
  `specified_name` varchar(60) DEFAULT NULL,
  `amount` float DEFAULT NULL,
  `creationTime` int(11) DEFAULT NULL,
  PRIMARY KEY (`year`,`month`,`specified_no`,`kind`,`category`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=DYNAMIC;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb.purchase_order 結構
CREATE TABLE IF NOT EXISTS `purchase_order` (
  `id` varchar(60) NOT NULL,
  `no` varchar(20) NOT NULL,
  `creator_id` varchar(60) DEFAULT NULL,
  `purchase_request_id` varchar(60) DEFAULT NULL,
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
  `result` int(11) DEFAULT NULL,
  `resultTime` int(11) DEFAULT NULL,
  `comment` varchar(128) DEFAULT NULL,
  `creationTime` int(11) DEFAULT NULL,
  PRIMARY KEY (`no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb.purchase_request 結構
CREATE TABLE IF NOT EXISTS `purchase_request` (
  `id` varchar(60) NOT NULL,
  `no` varchar(20) DEFAULT NULL,
  `creator_id` varchar(60) DEFAULT NULL,
  `product_order_id` varchar(60) DEFAULT NULL,
  `date` int(11) DEFAULT NULL,
  `result` int(11) DEFAULT NULL,
  `result_time` int(11) DEFAULT NULL,
  `comment` varchar(128) DEFAULT NULL,
  `creationTime` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `product_order_id` (`product_order_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb.purchase_request_item 結構
CREATE TABLE IF NOT EXISTS `purchase_request_item` (
  `id` varchar(60) NOT NULL,
  `purchase_request_id` varchar(60) DEFAULT NULL,
  `material_id` varchar(60) DEFAULT NULL,
  `unit` int(11) DEFAULT NULL,
  `count` float DEFAULT NULL,
  `expectedDate` int(11) DEFAULT NULL,
  `comment` varchar(128) DEFAULT NULL,
  `creationTime` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `purchase_request_id` (`purchase_request_id`),
  KEY `material_id` (`material_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb.quotation 結構
CREATE TABLE IF NOT EXISTS `quotation` (
  `no` varchar(20) NOT NULL,
  `creator_id` varchar(60) DEFAULT NULL,
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

-- 傾印  資料表 ewdb.rw_items 結構
CREATE TABLE IF NOT EXISTS `rw_items` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `item_no` varchar(60) DEFAULT NULL,
  `item_name` varchar(60) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=DYNAMIC;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb.salary 結構
CREATE TABLE IF NOT EXISTS `salary` (
  `id` varchar(60) DEFAULT NULL,
  `employee_id` varchar(60) NOT NULL,
  `date` int(11) NOT NULL,
  `type` int(11) DEFAULT NULL,
  `monthly` int(11) DEFAULT NULL,
  `hourly` int(11) DEFAULT NULL,
  `bouns` int(11) DEFAULT NULL,
  `performanceBonus` int(11) DEFAULT NULL,
  `attendanceBonus` int(11) DEFAULT NULL,
  `creationTime` int(11) DEFAULT NULL,
  PRIMARY KEY (`employee_id`,`date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb.salary_delta 結構
CREATE TABLE IF NOT EXISTS `salary_delta` (
  `id` varchar(60) NOT NULL,
  `employee_id` varchar(60) DEFAULT NULL,
  `date` int(11) DEFAULT NULL,
  `type` int(11) DEFAULT NULL,
  `monthly` int(11) DEFAULT NULL,
  `hourly` int(11) DEFAULT NULL,
  `bouns` int(11) DEFAULT NULL,
  `performanceBonus` int(11) DEFAULT NULL,
  `attendanceBonus` int(11) DEFAULT NULL,
  `comment` varchar(128) DEFAULT NULL,
  `creationTime` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb.sample 結構
CREATE TABLE IF NOT EXISTS `sample` (
  `id` varchar(60) NOT NULL,
  `creator_id` varchar(60) DEFAULT NULL,
  `projectCode` varchar(20) DEFAULT NULL,
  `date` int(11) DEFAULT NULL,
  `finishDate` int(11) DEFAULT NULL,
  `customer_id` varchar(60) DEFAULT NULL,
  `proposer_id` varchar(60) DEFAULT NULL,
  `name` varchar(60) DEFAULT NULL,
  `count` float DEFAULT NULL,
  `specification` varchar(128) DEFAULT NULL,
  `description` varchar(128) DEFAULT NULL,
  `productionRequest` varchar(128) DEFAULT NULL,
  `speciaRequest` varchar(128) DEFAULT NULL,
  `productionBudget` varchar(128) DEFAULT NULL,
  `comment` varchar(128) DEFAULT NULL,
  `creationTime` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `customer_id` (`customer_id`),
  KEY `proposer_id` (`proposer_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb.sample_price 結構
CREATE TABLE IF NOT EXISTS `sample_price` (
  `item_no` varchar(60) NOT NULL,
  `itemVer` int(11) DEFAULT NULL,
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
  PRIMARY KEY (`item_no`,`date`) USING BTREE,
  KEY `item_no` (`item_no`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=DYNAMIC;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb.server 結構
CREATE TABLE IF NOT EXISTS `server` (
  `timezone` varchar(60) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb.server_info 結構
CREATE TABLE IF NOT EXISTS `server_info` (
  `id` varchar(60) NOT NULL,
  `timezone` varchar(60) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb.session 結構
CREATE TABLE IF NOT EXISTS `session` (
  `id` varchar(60) NOT NULL,
  `token` varchar(60) DEFAULT NULL,
  `user_no` varchar(60) DEFAULT NULL,
  `expiredTime` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb.shipping_order 結構
CREATE TABLE IF NOT EXISTS `shipping_order` (
  `id` varchar(60) NOT NULL,
  `no` varchar(20) NOT NULL,
  `creator_id` varchar(60) DEFAULT NULL,
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
  `result` int(11) DEFAULT NULL,
  `resultTime` int(11) DEFAULT NULL,
  `comment` varchar(128) DEFAULT NULL,
  `creationTime` int(11) DEFAULT NULL,
  PRIMARY KEY (`no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb.shipping_payment 結構
CREATE TABLE IF NOT EXISTS `shipping_payment` (
  `id` varchar(60) NOT NULL,
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
  `count` double DEFAULT NULL,
  `amount` double DEFAULT NULL,
  `addDeleteAmount` int(11) DEFAULT NULL,
  `totalAmount` double DEFAULT NULL,
  `balance` double DEFAULT NULL,
  `creationTime` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=DYNAMIC;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb.shipping_price 結構
CREATE TABLE IF NOT EXISTS `shipping_price` (
  `id` varchar(60) DEFAULT NULL,
  `vendor_id` varchar(60) NOT NULL,
  `vendor_displayName` varchar(60) DEFAULT NULL,
  `displayName` varchar(60) DEFAULT NULL,
  `region` int(11) NOT NULL,
  `category` int(11) NOT NULL,
  `unitPrice` int(11) DEFAULT NULL,
  `maxCapacity` int(11) DEFAULT NULL,
  `price` double DEFAULT NULL,
  `creationTime` int(11) DEFAULT NULL,
  PRIMARY KEY (`vendor_id`,`region`,`category`),
  KEY `idx_shipping` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb.shipping_record 結構
CREATE TABLE IF NOT EXISTS `shipping_record` (
  `no` varchar(60) NOT NULL,
  `date` int(11) DEFAULT NULL,
  `refCategory` int(11) DEFAULT NULL,
  `ref_no` varchar(60) DEFAULT NULL,
  `ref_parent_no` varchar(60) DEFAULT NULL,
  `sw_alias_no` varchar(20) DEFAULT NULL,
  `sw_alias_name` varchar(60) DEFAULT NULL,
  `item_no` varchar(60) DEFAULT NULL,
  `item_name` varchar(60) DEFAULT NULL,
  `item_ref_no` varchar(60) DEFAULT NULL,
  `item_ref_displayName` varchar(60) DEFAULT NULL,
  `contract_no` varchar(60) DEFAULT NULL,
  `unit` int(11) DEFAULT NULL,
  `price` float DEFAULT NULL,
  `checkedCount` float DEFAULT NULL,
  `expectedCount` float DEFAULT NULL,
  `comment` varchar(128) DEFAULT NULL,
  `creationTime` int(11) DEFAULT NULL,
  PRIMARY KEY (`no`) USING BTREE,
  KEY `reference_id` (`ref_no`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=DYNAMIC;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb.ship_wh 結構
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
  PRIMARY KEY (`no`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=DYNAMIC;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb.ship_wh_alias 結構
CREATE TABLE IF NOT EXISTS `ship_wh_alias` (
  `no` varchar(60) NOT NULL,
  `name` varchar(60) DEFAULT NULL,
  `category` int(11) NOT NULL,
  `type` int(11) NOT NULL,
  `creationTime` int(11) DEFAULT NULL,
  PRIMARY KEY (`no`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=DYNAMIC;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb.ship_wh_contract 結構
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
  PRIMARY KEY (`no`,`date`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=DYNAMIC;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb.ship_wh_quotation 結構
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
  `price` double DEFAULT NULL,
  `fee` double DEFAULT NULL,
  `comment` varchar(128) DEFAULT NULL,
  `creationTime` int(11) DEFAULT NULL,
  PRIMARY KEY (`no`,`date`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=DYNAMIC;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb.station 結構
CREATE TABLE IF NOT EXISTS `station` (
  `no` varchar(60) NOT NULL,
  `production_line_no` varchar(60) DEFAULT NULL,
  `name` varchar(60) DEFAULT NULL,
  `stage` int(11) DEFAULT NULL,
  `comment` varchar(128) DEFAULT '',
  `creationTime` int(11) DEFAULT NULL,
  PRIMARY KEY (`no`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=DYNAMIC;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb.supplier 結構
CREATE TABLE IF NOT EXISTS `supplier` (
  `id` varchar(60) DEFAULT NULL,
  `no` varchar(20) NOT NULL,
  `category` int(11) DEFAULT NULL,
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
  `payment_id` varchar(60) DEFAULT NULL,
  `bankDisplayName` varchar(60) DEFAULT NULL,
  `bankName` varchar(60) DEFAULT NULL,
  `bankBranch` varchar(60) DEFAULT NULL,
  `bankAccount` varchar(60) DEFAULT NULL,
  `bankNo` varchar(60) DEFAULT NULL,
  `comment` varchar(128) DEFAULT NULL,
  `creationTime` int(11) DEFAULT NULL,
  PRIMARY KEY (`no`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=DYNAMIC;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb.temp 結構
CREATE TABLE IF NOT EXISTS `temp` (
  `work_order_no` varchar(60) DEFAULT NULL,
  `date` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb.trans_items 結構
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
  PRIMARY KEY (`no`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=DYNAMIC;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb.trans_items2 結構
CREATE TABLE IF NOT EXISTS `trans_items2` (
  `no` varchar(20) NOT NULL,
  `name` varchar(100) NOT NULL,
  `category` int(11) DEFAULT NULL,
  `attribute` int(11) DEFAULT 0,
  `company_no` varchar(60) NOT NULL,
  `company_displayName` varchar(60) DEFAULT NULL,
  `comment` varchar(128) DEFAULT NULL,
  `creationTime` int(11) DEFAULT NULL,
  PRIMARY KEY (`no`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=DYNAMIC;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb.user_group 結構
CREATE TABLE IF NOT EXISTS `user_group` (
  `id` varchar(60) NOT NULL,
  `name` varchar(60) NOT NULL,
  `role` int(11) DEFAULT NULL,
  `users` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`users`)),
  `privileges` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`privileges`)),
  PRIMARY KEY (`name`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=DYNAMIC;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb.vendor 結構
CREATE TABLE IF NOT EXISTS `vendor` (
  `id` varchar(60) NOT NULL,
  `no` varchar(20) NOT NULL,
  `category` int(11) DEFAULT NULL,
  `businessNo` varchar(20) NOT NULL,
  `displayName` varchar(60) DEFAULT NULL,
  `name` varchar(60) DEFAULT NULL,
  `address` varchar(100) DEFAULT NULL,
  `phone` varchar(100) DEFAULT NULL,
  `fax` varchar(20) DEFAULT NULL,
  `contactName` varchar(60) DEFAULT NULL,
  `contactPhone` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`contactPhone`)),
  `contactTitle` varchar(60) DEFAULT NULL,
  `contactEmail` varchar(60) DEFAULT NULL,
  `payment_id` varchar(60) DEFAULT NULL,
  `bankDisplayName` varchar(60) DEFAULT NULL,
  `bankName` varchar(60) DEFAULT NULL,
  `bankBranch` varchar(60) DEFAULT NULL,
  `bankAccount` varchar(60) DEFAULT NULL,
  `bankNo` varchar(60) DEFAULT NULL,
  `comment` varchar(128) DEFAULT NULL,
  `creationTime` int(11) DEFAULT NULL,
  PRIMARY KEY (`no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb.warehouse 結構
CREATE TABLE IF NOT EXISTS `warehouse` (
  `no` varchar(60) NOT NULL,
  `vendor_no` varchar(60) NOT NULL,
  `vendor_displayName` varchar(60) DEFAULT NULL,
  `displayName` varchar(60) DEFAULT NULL,
  `category` int(11) NOT NULL,
  `unit` int(11) DEFAULT NULL,
  `maxCapacity` int(11) DEFAULT NULL,
  `comment` varchar(128) DEFAULT NULL,
  `creationTime` int(11) DEFAULT NULL,
  PRIMARY KEY (`no`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=DYNAMIC;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb.warehouse_history 結構
CREATE TABLE IF NOT EXISTS `warehouse_history` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ref_no` varchar(20) NOT NULL,
  `fieldName` varchar(60) NOT NULL,
  `oldValue` text DEFAULT NULL,
  `newValue` text DEFAULT NULL,
  `modifiedBy` varchar(60) DEFAULT NULL,
  `modifiedAt` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=40 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=DYNAMIC;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb.warehouse_payment 結構
CREATE TABLE IF NOT EXISTS `warehouse_payment` (
  `id` varchar(60) NOT NULL,
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
  `count` double DEFAULT NULL,
  `days` double DEFAULT NULL,
  `amount` double DEFAULT NULL,
  `addDeleteAmount` int(11) DEFAULT NULL,
  `totalAmount` double DEFAULT NULL,
  `balance` double DEFAULT NULL,
  `creationTime` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=DYNAMIC;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb.warehouse_price 結構
CREATE TABLE IF NOT EXISTS `warehouse_price` (
  `no` varchar(60) NOT NULL,
  `version` int(11) NOT NULL DEFAULT 0,
  `date` int(11) DEFAULT NULL,
  `displayName` varchar(60) DEFAULT NULL,
  `warehouse_no` varchar(60) NOT NULL,
  `category` int(11) DEFAULT NULL,
  `region` int(11) DEFAULT NULL,
  `type` int(11) DEFAULT NULL,
  `unit` int(11) DEFAULT NULL,
  `price` double DEFAULT NULL,
  `fee` double DEFAULT NULL,
  `comment` varchar(128) DEFAULT NULL,
  `creationTime` int(11) DEFAULT NULL,
  PRIMARY KEY (`no`,`version`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb.warehouse_record 結構
CREATE TABLE IF NOT EXISTS `warehouse_record` (
  `no` varchar(60) NOT NULL,
  `date` int(11) DEFAULT NULL,
  `ref_no` varchar(60) DEFAULT NULL,
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
  `price` float DEFAULT NULL,
  `count` float DEFAULT NULL,
  `days` float DEFAULT NULL,
  `comment` varchar(128) DEFAULT NULL,
  `creationTime` int(11) DEFAULT NULL,
  PRIMARY KEY (`no`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=DYNAMIC;

-- 取消選取資料匯出。

-- 傾印  資料表 ewdb.work_order 結構
CREATE TABLE IF NOT EXISTS `work_order` (
  `id` varchar(60) NOT NULL,
  `date` int(11) DEFAULT NULL,
  `no` varchar(20) NOT NULL,
  `creator_id` varchar(60) DEFAULT NULL,
  `product_order_no` varchar(60) DEFAULT NULL,
  `aps_no` varchar(60) DEFAULT '',
  `customer_no` varchar(60) DEFAULT NULL,
  `customer_displayName` varchar(60) DEFAULT NULL,
  `product_no` varchar(60) DEFAULT NULL,
  `product_name` varchar(100) DEFAULT NULL,
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
  `result` int(11) DEFAULT NULL,
  `resultTime` int(11) DEFAULT NULL,
  `comment` varchar(128) DEFAULT NULL,
  `creationTime` int(11) DEFAULT NULL,
  PRIMARY KEY (`no`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=DYNAMIC;

-- 取消選取資料匯出。

-- 傾印  觸發器 ewdb.aps_quantity_item_trigger 結構
SET @OLDTMP_SQL_MODE=@@SQL_MODE, SQL_MODE='STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION';
DELIMITER //
CREATE TRIGGER `aps_quantity_item_trigger` BEFORE INSERT ON `aps_quantity_item` FOR EACH ROW BEGIN
	SET NEW.id =  REPLACE(UUID(),"-","");
END//
DELIMITER ;
SET SQL_MODE=@OLDTMP_SQL_MODE;

-- 傾印  觸發器 ewdb.bankaccount_trigger 結構
SET @OLDTMP_SQL_MODE=@@SQL_MODE, SQL_MODE='STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION';
DELIMITER //
CREATE TRIGGER bankaccount_trigger
BEFORE INSERT ON bank_account
FOR EACH ROW
BEGIN
	SET NEW.id =  REPLACE(UUID(),"-","");
   SET NEW.creationTime = UNIX_TIMESTAMP();
END//
DELIMITER ;
SET SQL_MODE=@OLDTMP_SQL_MODE;

-- 傾印  觸發器 ewdb.gen_uuid_trigger 結構
SET @OLDTMP_SQL_MODE=@@SQL_MODE, SQL_MODE='IGNORE_SPACE,STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION';
DELIMITER //
CREATE TRIGGER gen_uuid_trigger
BEFORE INSERT ON payment
FOR EACH ROW
BEGIN
    -- 只有當 NEW.id 為 NULL 或空值時才生成 UUID
    IF NEW.id IS NULL OR NEW.id = '' THEN
        SET NEW.id = REPLACE(UUID(), "-", "");
    END IF;
END//
DELIMITER ;
SET SQL_MODE=@OLDTMP_SQL_MODE;

-- 傾印  觸發器 ewdb.id_trigger 結構
SET @OLDTMP_SQL_MODE=@@SQL_MODE, SQL_MODE='STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION';
DELIMITER //
CREATE TRIGGER id_trigger
BEFORE INSERT ON server_info
FOR EACH ROW
BEGIN
	SET NEW.id =  REPLACE(UUID(),"-","");
END//
DELIMITER ;
SET SQL_MODE=@OLDTMP_SQL_MODE;

-- 傾印  觸發器 ewdb.set_time_trigger 結構
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

-- 傾印  觸發器 ewdb.trg_station_no 結構
SET @OLDTMP_SQL_MODE=@@SQL_MODE, SQL_MODE='STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION';
DELIMITER //
CREATE TRIGGER trg_station_no BEFORE INSERT ON station
FOR EACH ROW
BEGIN
    -- 前綴：ST
    SET @prefix := 'ST';

    -- 產生 10 碼英數 (A-Z0-9)
    SET @rand10 := UPPER(SUBSTRING(MD5(RAND()), 1, 10));
	
    -- 組合成 12 碼 ID
    SET NEW.no = CONCAT(@prefix, @rand10);

    -- 建立 timestamp
    SET NEW.creationTime = UNIX_TIMESTAMP();
END//
DELIMITER ;
SET SQL_MODE=@OLDTMP_SQL_MODE;

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
