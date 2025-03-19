/*
SQLyog Community v13.2.0 (64 bit)
MySQL - 8.0.12 : Database - db_lostfoundmgr_sys
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`db_lostfoundmgr_sys` /*!40100 DEFAULT CHARACTER SET utf8 */;

USE `db_lostfoundmgr_sys`;

/*Table structure for table `banner` */

DROP TABLE IF EXISTS `banner`;

CREATE TABLE `banner` (
  `id` INT(11) NOT NULL AUTO_INCREMENT COMMENT 'Slideshow number',
  `img` VARCHAR(200) DEFAULT NULL COMMENT 'picture',
  `url` VARCHAR(200) DEFAULT NULL COMMENT 'Link address',
  `index_radio` VARCHAR(20) DEFAULT NULL COMMENT 'Is it home page',
  PRIMARY KEY (`id`)
) ENGINE=MYISAM AUTO_INCREMENT=8 DEFAULT CHARSET=utf8 COMMENT='Slideshow';

/*Data for the table `banner` */

INSERT  INTO `banner`(`id`,`img`,`url`,`index_radio`) VALUES 
(5,'http://localhost:9090/media/8c588e95-0e0b-49a6-8ffe-75c6eb120a82.jpg',NULL,'YES'),
(6,'http://localhost:9090/media/226ea4d6-e3d8-489a-9189-884eee9fef72.jpg',NULL,'YES'),
(7,'http://localhost:9090/media/987e22aa-54c5-49f6-b00b-0189fe5360fb.jpg',NULL,'NO');

/*Table structure for table `cart` */

DROP TABLE IF EXISTS `cart`;

CREATE TABLE `cart` (
  `id` INT(11) NOT NULL AUTO_INCREMENT COMMENT 'Claim Number',
  `user_id` INT(11) DEFAULT NULL COMMENT 'Claim User',
  `name` VARCHAR(200) DEFAULT NULL COMMENT 'Claiming items',
  `img` VARCHAR(200) DEFAULT NULL COMMENT 'Item Image',
  `biz_user_id` INT(11) DEFAULT NULL COMMENT 'Pickup Person',
  `goodid` INT(11) DEFAULT NULL COMMENT 'Item Number',
  PRIMARY KEY (`id`)
) ENGINE=MYISAM AUTO_INCREMENT=5 DEFAULT CHARSET=utf8 COMMENT='Information to be claimed';

/*Data for the table `cart` */

/*Table structure for table `category` */

DROP TABLE IF EXISTS `category`;

CREATE TABLE `category` (
  `id` INT(11) NOT NULL AUTO_INCREMENT COMMENT 'number',
  `name` VARCHAR(200) DEFAULT NULL COMMENT 'Category Name',
  PRIMARY KEY (`id`)
) ENGINE=MYISAM AUTO_INCREMENT=5 DEFAULT CHARSET=utf8 COMMENT='Item Type';

/*Data for the table `category` */

INSERT  INTO `category`(`id`,`name`) VALUES 
(1,'Clothing'),
(2,'Digital Products'),
(3,'Daily necessities'),
(4,'books');

/*Table structure for table `dict` */

DROP TABLE IF EXISTS `dict`;

CREATE TABLE `dict` (
  `id` INT(11) NOT NULL AUTO_INCREMENT COMMENT 'number',
  `code` VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT 'coding',
  `value` VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT 'content',
  `type` VARCHAR(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT 'type',
  `deleted` INT(11) DEFAULT '0' COMMENT 'delete',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `c_d` (`code`,`deleted`) USING BTREE
) ENGINE=INNODB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=DYNAMIC COMMENT='Data dictionary';

/*Data for the table `dict` */

INSERT  INTO `dict`(`id`,`code`,`value`,`type`,`deleted`) VALUES 
(2,'message','message','icon',0),
(3,'menu','menu','icon',0),
(4,'grid','grid','icon',0),
(5,'house','house','icon',0),
(6,'user','user','icon',0),
(7,'file','files','icon',0),
(8,'money','money','icon',0),
(9,'school','school','icon',0),
(10,'notebook','notebook','icon',0),
(11,'coin','coin','icon',0),
(12,'set-up','set-up','icon',0),
(13,'postcard','postcard','icon',0),
(14,'food','food','icon',0),
(15,'position','position','icon',0),
(16,'chat-line-round','chat-line-round','icon',0),
(17,'chat-dot-round','chat-dot-round','icon',0),
(18,'setting','setting','icon',0),
(19,'comment','comment','icon',0);

/*Table structure for table `lost` */

DROP TABLE IF EXISTS `lost`;

CREATE TABLE `lost` (
  `id` INT(11) NOT NULL AUTO_INCREMENT COMMENT 'number',
  `category_id` INT(11) DEFAULT NULL COMMENT 'Item Classification',
  `name` VARCHAR(200) DEFAULT NULL COMMENT 'Item Name',
  `img` VARCHAR(200) DEFAULT NULL COMMENT 'Item Image',
  `content` TEXT COMMENT 'Item Description',
  `address` VARCHAR(200) DEFAULT NULL COMMENT 'Lost location',
  `time` VARCHAR(200) DEFAULT NULL COMMENT 'Lost time',
  `phone` VARCHAR(200) DEFAULT NULL COMMENT 'Contact Details',
  `user_id` INT(11) DEFAULT NULL COMMENT 'Publisher',
  `create_time` DATETIME DEFAULT NULL COMMENT 'Release time',
  PRIMARY KEY (`id`)
) ENGINE=MYISAM AUTO_INCREMENT=2 DEFAULT CHARSET=utf8 COMMENT='Lost property information';

/*Data for the table `lost` */

INSERT  INTO `lost`(`id`,`category_id`,`name`,`img`,`content`,`address`,`time`,`phone`,`user_id`,`create_time`) VALUES 
(1,1,'I lost a Li Ning sportswear','http://localhost:9090/media/b8bcd7e9-4f77-4cb2-ad1c-6fe6fcada0b9.png','<p>I lost a Li Ning sportswear</p>','Second Canteen 2nd Floor','2025-2-31 00:00:00','13233334444',38,'2025-2-31 17:56:30');

/*Table structure for table `member` */

DROP TABLE IF EXISTS `member`;

CREATE TABLE `member` (
  `id` INT(11) NOT NULL AUTO_INCREMENT COMMENT 'number',
  `username` VARCHAR(200) DEFAULT NULL COMMENT 'Log in to your account',
  `name` VARCHAR(200) DEFAULT NULL COMMENT 'Name',
  `user_id` INT(11) DEFAULT NULL COMMENT 'User',
  `phone` VARCHAR(200) DEFAULT NULL COMMENT 'phone number',
  PRIMARY KEY (`id`)
) ENGINE=MYISAM AUTO_INCREMENT=3 DEFAULT CHARSET=utf8 COMMENT='user';

/*Data for the table `member` */

INSERT  INTO `member`(`id`,`username`,`name`,`user_id`,`phone`) VALUES 
(1,'zhangsan','zhangsan',38,'13211112222'),
(2,'lisi','lisi',39,'13566667777');

/*Table structure for table `notice` */

DROP TABLE IF EXISTS `notice`;

CREATE TABLE `notice` (
  `id` INT(11) NOT NULL AUTO_INCREMENT COMMENT 'number',
  `name` VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT 'name',
  `content` TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci COMMENT 'content',
  `create_time` DATETIME DEFAULT NULL COMMENT 'Creation time',
  `user_id` INT(11) DEFAULT NULL COMMENT 'Creator ID',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=INNODB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=DYNAMIC COMMENT='System announcement';

/*Data for the table `notice` */

INSERT  INTO `notice`(`id`,`name`,`content`,`create_time`,`user_id`) VALUES 
(16,'Lost and Found System is officially established','<p>Lost and Found System is officially established</p>','2025-02-31 17:52:15',1);

/*Table structure for table `orders` */

DROP TABLE IF EXISTS `orders`;

CREATE TABLE `orders` (
  `id` INT(11) NOT NULL AUTO_INCREMENT COMMENT 'Claim Number',
  `name` VARCHAR(100) DEFAULT NULL COMMENT 'Claim number',
  `content` TEXT COMMENT 'Claim details',
  `state_radio` VARCHAR(20) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT 'Applying' COMMENT 'Order status, claiming|confirmed as lost|returned|cancelled',
  `user_id` INT(11) DEFAULT NULL COMMENT 'Claim User',
  `create_time` DATETIME DEFAULT NULL COMMENT 'Application period',
  `update_time` DATETIME DEFAULT NULL COMMENT 'Update time',
  `biz_user_id` INT(11) DEFAULT NULL COMMENT 'Lost and found person',
  `goodids` VARCHAR(100) DEFAULT NULL COMMENT 'Item Number',
  PRIMARY KEY (`id`)
) ENGINE=MYISAM AUTO_INCREMENT=5 DEFAULT CHARSET=utf8 COMMENT='Lost and found records';

/*Data for the table `orders` */

INSERT  INTO `orders`(`id`,`name`,`content`,`state_radio`,`user_id`,`create_time`,`update_time`,`biz_user_id`,`goodids`) VALUES 
(3,'20250231232428','User lost property claim information：<br/><ul><li>Name of claimant：zhangsan</li><li>Claimant mobile phone：13211112222</li><li>Description of lost items: There is a Cai Xukun on the phone case</li></ul>Lost items details:<br/><ul><li>Item Name：Picked up a brand new Huawei Mate60</li></ul>','Applying',39,'2025-2-31 23:24:29','2025-2-31 23:24:29',38,'2'),
(4,'20250231234801','User lost property claim information：<br/><ul><li>Name of claimant：zhangsan</li><li>Claimant mobile phone：1321112222</li><li>Description of lost item: My name is on the first page of the book. Name: xxxx</li></ul>Lost items details:<br/><ul><li>Item Name：I found a math book for postgraduate entrance examination</li></ul>','Confirmed as the owner',38,'2025-2-31 23:48:02','2025-2-31 23:48:31',39,'3');

/*Table structure for table `recruit` */

DROP TABLE IF EXISTS `recruit`;

CREATE TABLE `recruit` (
  `id` INT(11) NOT NULL AUTO_INCREMENT COMMENT 'number',
  `category_id` INT(11) DEFAULT NULL COMMENT 'Item Classification',
  `name` VARCHAR(200) DEFAULT NULL COMMENT 'Item Name',
  `img` VARCHAR(200) DEFAULT NULL COMMENT 'Item Image',
  `content` TEXT COMMENT 'Item Description',
  `address` VARCHAR(200) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT 'Pickup Location',
  `time` VARCHAR(200) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT 'Pickup time',
  `user_id` INT(11) DEFAULT NULL COMMENT 'Publisher',
  `create_time` DATETIME DEFAULT NULL COMMENT 'Release time',
  PRIMARY KEY (`id`)
) ENGINE=MYISAM AUTO_INCREMENT=4 DEFAULT CHARSET=utf8 COMMENT='Lost and Foundinformation';

/*Data for the table `recruit` */

INSERT  INTO `recruit`(`id`,`category_id`,`name`,`img`,`content`,`address`,`time`,`user_id`,`create_time`) VALUES 
(1,1,'Found a men clothing','http://localhost:9090/media/d4207df9-a9a4-42f0-b009-2735d95ed18f.png','<p>Found a men clothing</p>','Classroom 101, Second Teaching Building','2025-2-31 17:51:38',38,'2025-2-31 17:51:39'),
(2,2,'Picked up a brand new Huawei Mate60','http://localhost:9090/media/b9feb215-57f7-4ac2-987c-8817afb4d8cc.png','<p>Picked up a brand new Huawei Mate60</p>','First Canteen 1st Floor','2025-2-31 17:53:45',38,'2025-2-31 17:53:46'),
(3,4,'I found a math book for postgraduate entrance examination','http://localhost:9090/media/ac5fa446-b42f-48fa-954a-2609293b3f3e.jpg','<p>I found a math book for postgraduate entrance examinationI found a math book for postgraduate entrance examinationI found a math book for postgraduate entrance examination</p>','Second Canteen, 2nd Floor','2025-2-26 10:00:00',39,'2025-2-31 23:46:37');

/*Table structure for table `sys_permission` */

DROP TABLE IF EXISTS `sys_permission`;

CREATE TABLE `sys_permission` (
  `id` INT(11) NOT NULL AUTO_INCREMENT COMMENT 'number',
  `name` VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT 'name',
  `path` VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT 'path',
  `orders` INT(11) DEFAULT '1' COMMENT 'Order',
  `icon` VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT 'grid' COMMENT 'icon',
  `page` VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT 'Page Path',
  `auth` VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT 'Permissions',
  `p_id` INT(11) DEFAULT NULL COMMENT 'Parent ID',
  `deleted` INT(11) DEFAULT '0' COMMENT 'Logical deletion',
  `create_time` DATETIME DEFAULT NULL COMMENT 'Creation time',
  `update_time` DATETIME DEFAULT NULL COMMENT 'Update time',
  `type` INT(11) DEFAULT NULL COMMENT 'type',
  `hide` TINYINT(1) DEFAULT '0' COMMENT 'Is it hidden',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `a_d_index` (`auth`,`deleted`) USING BTREE,
  UNIQUE KEY `p_p_d_index` (`path`,`page`,`deleted`) USING BTREE
) ENGINE=INNODB AUTO_INCREMENT=579 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=DYNAMIC COMMENT='Permissions';

/*Data for the table `sys_permission` */

INSERT  INTO `sys_permission`(`id`,`name`,`path`,`orders`,`icon`,`page`,`auth`,`p_id`,`deleted`,`create_time`,`update_time`,`type`,`hide`) VALUES 
(1,'System Management','',2,'menu',NULL,NULL,NULL,0,'2023-01-16 20:45:51','2023-01-16 20:45:51',1,0),
(3,'User Management','user',1,'user','User','user.list',1,0,'2023-01-16 20:45:51','2023-08-16 23:06:21',2,0),
(4,'userAdded','',1,NULL,'','user.add',3,0,'2023-01-16 20:45:51','2023-01-16 20:45:51',3,0),
(8,'User Edit','',1,NULL,NULL,'user.edit',3,0,NULL,'2023-01-28 11:45:21',3,0),
(9,'User Deletion',NULL,1,NULL,NULL,'user.delete',3,0,'2023-01-29 11:04:15','2023-01-29 11:04:15',3,0),
(10,'Role Management','role',1,'grid','Role','role.list',1,0,'2023-01-31 20:32:59','2023-01-31 20:32:59',2,0),
(11,'Permission Management','permission',1,'position','Permission','permission.list',1,0,'2023-01-31 20:33:25','2023-08-16 23:05:29',2,0),
(12,'Front page','home',1,'house','Home',NULL,NULL,0,'2023-01-31 21:03:00','2023-01-31 21:03:00',2,0),
(13,'Data dictionarymanage','dict',1,'set-up','Dict','dict.list',1,0,'2023-02-02 20:41:32','2023-08-16 23:32:18',2,0),
(14,'Batch Deletion',NULL,1,'',NULL,'user.deleteBatch',3,0,'2023-02-02 22:32:22','2023-02-02 22:32:22',3,0),
(16,'userExport',NULL,1,NULL,NULL,'user.export',3,0,'2023-02-02 22:33:08','2023-02-02 22:33:08',3,0),
(21,'RoleAdded',NULL,1,NULL,'','role.add',10,0,'2023-01-16 20:45:51','2023-01-16 20:45:51',3,0),
(22,'Roleedit',NULL,1,NULL,NULL,'role.edit',10,0,NULL,'2023-01-28 11:45:21',3,0),
(23,'Roledelete',NULL,1,NULL,NULL,'role.delete',10,0,'2023-01-29 11:04:15','2023-01-29 11:04:15',3,0),
(25,'Batch Deletion',NULL,1,NULL,NULL,'role.deleteBatch',10,0,'2023-02-02 22:32:22','2023-02-02 22:32:22',3,0),
(27,'RoleExport',NULL,1,NULL,NULL,'role.export',10,0,'2023-02-02 22:33:08','2023-02-02 22:33:08',3,0),
(30,'PermissionsAdded',NULL,1,NULL,'','permission.add',11,0,'2023-01-16 20:45:51','2023-01-16 20:45:51',3,0),
(31,'Permissionsedit',NULL,1,NULL,NULL,'permission.edit',11,0,NULL,'2023-01-28 11:45:21',3,0),
(32,'Permissionsdelete',NULL,1,NULL,NULL,'permission.delete',11,0,'2023-01-29 11:04:15','2023-01-29 11:04:15',3,0),
(35,'PermissionsExport',NULL,1,NULL,NULL,'permission.export',11,0,'2023-02-02 22:33:08','2023-02-02 22:33:08',3,0),
(37,'Data dictionaryAdded',NULL,1,NULL,'','dict.add',13,0,'2023-01-16 20:45:51','2023-01-16 20:45:51',3,0),
(38,'Data dictionaryedit',NULL,1,NULL,NULL,'dict.edit',13,0,NULL,'2023-01-28 11:45:21',3,0),
(39,'Data dictionarydelete',NULL,1,NULL,NULL,'dict.delete',13,0,'2023-01-29 11:04:15','2023-01-29 11:04:15',3,0),
(40,'Batch Deletion',NULL,1,NULL,NULL,'dict.deleteBatch',13,0,'2023-02-02 22:32:22','2023-02-02 22:32:22',3,0),
(42,'Data dictionaryExport',NULL,1,NULL,NULL,'dict.export',13,0,'2023-02-02 22:33:08','2023-02-02 22:33:08',3,0),
(505,'Announcement Management','notice',1,'comment','Notice',NULL,NULL,0,NULL,'2023-08-16 23:04:04',2,0),
(506,'announcementQuery',NULL,1,'grid',NULL,'notice.list',505,0,NULL,'2023-08-14 16:28:13',3,0),
(507,'announcementAdded',NULL,1,'grid',NULL,'notice.add',505,0,NULL,'2023-08-14 16:28:16',3,0),
(509,'announcementExport',NULL,1,'grid',NULL,'notice.export',505,0,NULL,NULL,3,0),
(510,'Batch Deletion',NULL,1,'grid',NULL,'notice.deleteBatch',505,0,NULL,NULL,3,0),
(511,'announcementedit',NULL,1,'grid',NULL,'notice.edit',505,0,NULL,NULL,3,0),
(512,'announcementdelete',NULL,1,'grid',NULL,'notice.delete',505,0,NULL,NULL,3,0),
(530,'User Management','member',1,'grid','Member',NULL,NULL,0,NULL,NULL,2,0),
(531,'userQuery',NULL,1,'grid',NULL,'member.list',530,0,NULL,NULL,3,0),
(532,'userAdded',NULL,1,'grid',NULL,'member.add',530,0,NULL,NULL,3,0),
(533,'userExport',NULL,1,'grid',NULL,'member.export',530,0,NULL,NULL,3,0),
(534,'Batch Deletion',NULL,1,'grid',NULL,'member.deleteBatch',530,0,NULL,NULL,3,0),
(535,'User Edit',NULL,1,'grid',NULL,'member.edit',530,0,NULL,NULL,3,0),
(536,'User Deletion',NULL,1,'grid',NULL,'member.delete',530,0,NULL,NULL,3,0),
(537,'Lost and found management','recruit',1,'grid','Recruit',NULL,NULL,0,NULL,NULL,2,0),
(538,'Lost and Found Enquiry',NULL,1,'grid',NULL,'recruit.list',537,0,NULL,NULL,3,0),
(539,'Lost and Found New',NULL,1,'grid',NULL,'recruit.add',537,0,NULL,NULL,3,0),
(540,'Lost and FoundExport',NULL,1,'grid',NULL,'recruit.export',537,0,NULL,NULL,3,0),
(541,'Batch Deletion',NULL,1,'grid',NULL,'recruit.deleteBatch',537,0,NULL,NULL,3,0),
(542,'Lost and Found Edit',NULL,1,'grid',NULL,'recruit.edit',537,0,NULL,NULL,3,0),
(543,'Lost and Founddelete',NULL,1,'grid',NULL,'recruit.delete',537,0,NULL,NULL,3,0),
(544,'Report lost itemsmanage','lost',1,'grid','Lost',NULL,NULL,0,NULL,NULL,2,0),
(545,'Report lost itemsQuery',NULL,1,'grid',NULL,'lost.list',544,0,NULL,NULL,3,0),
(546,'Report lost itemsAdded',NULL,1,'grid',NULL,'lost.add',544,0,NULL,NULL,3,0),
(547,'Report lost itemsExport',NULL,1,'grid',NULL,'lost.export',544,0,NULL,NULL,3,0),
(548,'Batch Deletion',NULL,1,'grid',NULL,'lost.deleteBatch',544,0,NULL,NULL,3,0),
(549,'Report lost itemsedit',NULL,1,'grid',NULL,'lost.edit',544,0,NULL,NULL,3,0),
(550,'Report lost itemsdelete',NULL,1,'grid',NULL,'lost.delete',544,0,NULL,NULL,3,0),
(551,'Item Typemanage','category',1,'grid','Category',NULL,NULL,0,NULL,NULL,2,0),
(552,'Item TypeQuery',NULL,1,'grid',NULL,'category.list',551,0,NULL,NULL,3,0),
(553,'Item TypeAdded',NULL,1,'grid',NULL,'category.add',551,0,NULL,NULL,3,0),
(554,'Item TypeExport',NULL,1,'grid',NULL,'category.export',551,0,NULL,NULL,3,0),
(555,'Batch Deletion',NULL,1,'grid',NULL,'category.deleteBatch',551,0,NULL,NULL,3,0),
(556,'Item Typeedit',NULL,1,'grid',NULL,'category.edit',551,0,NULL,NULL,3,0),
(557,'Item Typedelete',NULL,1,'grid',NULL,'category.delete',551,0,NULL,NULL,3,0),
(558,'Information to be claimedmanage','cart',1,'grid','Cart',NULL,NULL,0,NULL,'2024-05-31 08:58:38',2,1),
(559,'Information to be claimedQuery',NULL,1,'grid',NULL,'cart.list',558,0,NULL,NULL,3,0),
(560,'Information to be claimedAdded',NULL,1,'grid',NULL,'cart.add',558,0,NULL,NULL,3,0),
(561,'Information to be claimedExport',NULL,1,'grid',NULL,'cart.export',558,0,NULL,NULL,3,0),
(562,'Batch Deletion',NULL,1,'grid',NULL,'cart.deleteBatch',558,0,NULL,NULL,3,0),
(563,'Information to be claimededit',NULL,1,'grid',NULL,'cart.edit',558,0,NULL,NULL,3,0),
(564,'Information to be claimeddelete',NULL,1,'grid',NULL,'cart.delete',558,0,NULL,NULL,3,0),
(565,'Lost and found recordsmanage','orders',1,'grid','Orders',NULL,NULL,0,NULL,NULL,2,0),
(566,'Lost and found recordsQuery',NULL,1,'grid',NULL,'orders.list',565,0,NULL,NULL,3,0),
(567,'Lost and found recordsAdded',NULL,1,'grid',NULL,'orders.add',565,0,NULL,NULL,3,0),
(568,'Lost and found recordsExport',NULL,1,'grid',NULL,'orders.export',565,0,NULL,NULL,3,0),
(569,'Batch Deletion',NULL,1,'grid',NULL,'orders.deleteBatch',565,0,NULL,NULL,3,0),
(570,'Lost and found recordsedit',NULL,1,'grid',NULL,'orders.edit',565,0,NULL,NULL,3,0),
(571,'Lost and found recordsdelete',NULL,1,'grid',NULL,'orders.delete',565,0,NULL,NULL,3,0),
(572,'Slideshowmanage','banner',1,'grid','Banner',NULL,NULL,0,NULL,NULL,2,0),
(573,'SlideshowQuery',NULL,1,'grid',NULL,'banner.list',572,0,NULL,NULL,3,0),
(574,'SlideshowAdded',NULL,1,'grid',NULL,'banner.add',572,0,NULL,NULL,3,0),
(575,'SlideshowExport',NULL,1,'grid',NULL,'banner.export',572,0,NULL,NULL,3,0),
(576,'Batch Deletion',NULL,1,'grid',NULL,'banner.deleteBatch',572,0,NULL,NULL,3,0),
(577,'Slideshowedit',NULL,1,'grid',NULL,'banner.edit',572,0,NULL,NULL,3,0),
(578,'Slideshowdelete',NULL,1,'grid',NULL,'banner.delete',572,0,NULL,NULL,3,0);

/*Table structure for table `sys_role` */

DROP TABLE IF EXISTS `sys_role`;

CREATE TABLE `sys_role` (
  `id` INT(11) NOT NULL AUTO_INCREMENT COMMENT 'number',
  `name` VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT 'name',
  `flag` VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT 'Unique ID',
  `deleted` INT(11) DEFAULT '0' COMMENT 'Logical deletion',
  `create_time` DATETIME DEFAULT NULL COMMENT 'Creation time',
  `update_time` DATETIME DEFAULT NULL COMMENT 'Update time',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `flag_deleted_idnex` (`flag`,`deleted`) USING BTREE
) ENGINE=INNODB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=DYNAMIC COMMENT='Role';

/*Data for the table `sys_role` */

INSERT  INTO `sys_role`(`id`,`name`,`flag`,`deleted`,`create_time`,`update_time`) VALUES 
(1,'manager','ADMIN',0,'2023-01-16 19:49:44','2023-08-16 05:17:54'),
(9,'user','MEMBER',0,'2025-2-31 14:54:09','2025-2-31 23:46:56');

/*Table structure for table `sys_role_permission` */

DROP TABLE IF EXISTS `sys_role_permission`;

CREATE TABLE `sys_role_permission` (
  `id` INT(11) NOT NULL AUTO_INCREMENT COMMENT 'number',
  `role_id` INT(11) NOT NULL COMMENT 'Rolenumber',
  `permission_id` INT(11) NOT NULL COMMENT 'Permissionsnumber',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `role_id` (`role_id`,`permission_id`) USING BTREE
) ENGINE=INNODB AUTO_INCREMENT=5475 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=DYNAMIC COMMENT='RolePermissions';

/*Data for the table `sys_role_permission` */

INSERT  INTO `sys_role_permission`(`id`,`role_id`,`permission_id`) VALUES 
(5375,1,1),
(5376,1,3),
(5377,1,4),
(5378,1,8),
(5379,1,9),
(5380,1,10),
(5381,1,11),
(5382,1,12),
(5383,1,13),
(5384,1,14),
(5385,1,16),
(5386,1,21),
(5387,1,22),
(5388,1,23),
(5389,1,25),
(5390,1,27),
(5391,1,30),
(5392,1,31),
(5393,1,32),
(5394,1,35),
(5395,1,37),
(5396,1,38),
(5397,1,39),
(5398,1,40),
(5399,1,42),
(5400,1,505),
(5401,1,506),
(5402,1,507),
(5403,1,509),
(5404,1,510),
(5405,1,511),
(5406,1,512),
(5407,1,530),
(5408,1,531),
(5409,1,532),
(5410,1,533),
(5411,1,534),
(5412,1,535),
(5413,1,536),
(5414,1,537),
(5415,1,538),
(5416,1,539),
(5417,1,540),
(5418,1,541),
(5419,1,542),
(5420,1,543),
(5421,1,544),
(5422,1,545),
(5423,1,546),
(5424,1,547),
(5425,1,548),
(5426,1,549),
(5427,1,550),
(5428,1,551),
(5429,1,552),
(5430,1,553),
(5431,1,554),
(5432,1,555),
(5433,1,556),
(5434,1,557),
(5435,1,558),
(5436,1,559),
(5437,1,560),
(5438,1,561),
(5439,1,562),
(5440,1,563),
(5441,1,564),
(5442,1,565),
(5443,1,566),
(5444,1,567),
(5445,1,568),
(5446,1,569),
(5447,1,570),
(5448,1,571),
(5449,1,572),
(5450,1,573),
(5451,1,574),
(5452,1,575),
(5453,1,576),
(5454,1,577),
(5455,1,578),
(5456,9,12),
(5457,9,505),
(5458,9,506),
(5464,9,530),
(5465,9,531),
(5468,9,535),
(5469,9,537),
(5470,9,538),
(5471,9,539),
(5473,9,542),
(5474,9,543),
(5459,9,544),
(5460,9,545),
(5461,9,546),
(5462,9,549),
(5463,9,550),
(5466,9,565),
(5467,9,566),
(5472,9,570);

/*Table structure for table `sys_user` */

DROP TABLE IF EXISTS `sys_user`;

CREATE TABLE `sys_user` (
  `id` INT(11) NOT NULL AUTO_INCREMENT COMMENT 'number',
  `username` VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'username',
  `password` VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'password',
  `name` VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT 'Nick name',
  `email` VARCHAR(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT 'Mail',
  `address` VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT 'address',
  `uid` VARCHAR(40) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'User unique id',
  `deleted` INT(11) NOT NULL DEFAULT '0' COMMENT 'Logical deletion',
  `create_time` DATETIME DEFAULT NULL COMMENT 'Add time',
  `update_time` DATETIME DEFAULT NULL COMMENT 'Update time',
  `avatar` VARCHAR(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT 'avatar',
  `role` VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT 'Role',
  `score` INT(11) DEFAULT '0' COMMENT 'integral',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `uid_index` (`uid`) USING BTREE,
  UNIQUE KEY `username_index` (`username`,`deleted`) USING BTREE,
  UNIQUE KEY `email_index` (`email`,`deleted`) USING BTREE
) ENGINE=INNODB AUTO_INCREMENT=40 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=DYNAMIC COMMENT='user';

/*Data for the table `sys_user` */

INSERT  INTO `sys_user`(`id`,`username`,`password`,`name`,`email`,`address`,`uid`,`deleted`,`create_time`,`update_time`,`avatar`,`role`,`score`) VALUES 
(1,'admin','21232f297a57a5a743894a0e4a801fc3','manager','admin@126.com','England','4918ea50c06a458f94878abe741b4f51',0,'2022-12-09 20:08:17','2023-08-16 15:46:27','http://localhost:9090/media/c96e2606-44a3-4a6c-afdc-e32b76710d66.png','ADMIN',0),
(38,'zhangsan','e10adc3949ba59abbe56e057f20f883e','zhangsan','zhangsan@qq.com',NULL,'b692fb8a-a7c1-11ee-99b9-94e70b2ad9be',0,'2025-2-31 17:48:13','2025-2-31 17:49:18','http://localhost:9090/media/c96e2606-44a3-4a6c-afdc-e32b76710d66.png','MEMBER',0),
(39,'lisi','e10adc3949ba59abbe56e057f20f883e','lisi','lisi@qq.com',NULL,'0753c2db-a7c3-11ee-8ea7-94e70b2ad9be',0,'2025-2-31 17:57:38','2025-2-31 17:58:18','http://localhost:9090/media/9867db96-0328-49b7-80e4-b4cd2036473c.jpg','MEMBER',0);

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
