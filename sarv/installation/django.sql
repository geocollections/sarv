-- phpMyAdmin SQL Dump
-- version 4.0.4.2
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Dec 30, 2015 at 03:55 PM
-- Server version: 5.5.34-0ubuntu0.13.04.1
-- PHP Version: 5.4.9-4ubuntu2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `django`
--
CREATE DATABASE IF NOT EXISTS `django` DEFAULT CHARACTER SET latin1 COLLATE latin1_swedish_ci;
USE `django`;

-- --------------------------------------------------------

--
-- Table structure for table `auth_group`
--

CREATE TABLE IF NOT EXISTS `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `auth_group_permissions`
--

CREATE TABLE IF NOT EXISTS `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `group_id` (`group_id`,`permission_id`),
  KEY `auth_group_permissions_0e939a4f` (`group_id`),
  KEY `auth_group_permissions_8373b171` (`permission_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `auth_permission`
--

CREATE TABLE IF NOT EXISTS `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `content_type_id` (`content_type_id`,`codename`),
  KEY `auth_permission_417f1b1c` (`content_type_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=58 ;

--
-- Dumping data for table `auth_permission`
--

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(1, 'Can add permission', 1, 'add_permission'),
(2, 'Can change permission', 1, 'change_permission'),
(3, 'Can delete permission', 1, 'delete_permission'),
(4, 'Can add group', 2, 'add_group'),
(5, 'Can change group', 2, 'change_group'),
(6, 'Can delete group', 2, 'delete_group'),
(7, 'Can add user', 3, 'add_user'),
(8, 'Can change user', 3, 'change_user'),
(9, 'Can delete user', 3, 'delete_user'),
(10, 'Can add content type', 4, 'add_contenttype'),
(11, 'Can change content type', 4, 'change_contenttype'),
(12, 'Can delete content type', 4, 'delete_contenttype'),
(13, 'Can add session', 5, 'add_session'),
(14, 'Can change session', 5, 'change_session'),
(15, 'Can delete session', 5, 'delete_session'),
(16, 'Can add site', 6, 'add_site'),
(17, 'Can change site', 6, 'change_site'),
(18, 'Can delete site', 6, 'delete_site'),
(19, 'Can add acl', 7, 'add_acl'),
(20, 'Can change acl', 7, 'change_acl'),
(21, 'Can delete acl', 7, 'delete_acl'),
(22, 'Can add acl destination', 8, 'add_acldestination'),
(23, 'Can change acl destination', 8, 'change_acldestination'),
(24, 'Can delete acl destination', 8, 'delete_acldestination'),
(25, 'Can add acl group', 9, 'add_aclgroup'),
(26, 'Can change acl group', 9, 'change_aclgroup'),
(27, 'Can delete acl group', 9, 'delete_aclgroup'),
(28, 'Can add acl permission type', 10, 'add_aclpermissiontype'),
(29, 'Can change acl permission type', 10, 'change_aclpermissiontype'),
(30, 'Can delete acl permission type', 10, 'delete_aclpermissiontype'),
(31, 'Can add acl rights group', 11, 'add_aclrightsgroup'),
(32, 'Can change acl rights group', 11, 'change_aclrightsgroup'),
(33, 'Can delete acl rights group', 11, 'delete_aclrightsgroup'),
(34, 'Can add acl rights group permission type', 12, 'add_aclrightsgrouppermissiontype'),
(35, 'Can change acl rights group permission type', 12, 'change_aclrightsgrouppermissiontype'),
(36, 'Can delete acl rights group permission type', 12, 'delete_aclrightsgrouppermissiontype'),
(37, 'Can add acl user group', 13, 'add_aclusergroup'),
(38, 'Can change acl user group', 13, 'change_aclusergroup'),
(39, 'Can delete acl user group', 13, 'delete_aclusergroup'),
(40, 'Can add database', 14, 'add_database'),
(41, 'Can change database', 14, 'change_database'),
(42, 'Can delete database', 14, 'delete_database'),
(43, 'Can add sarv custom dataset', 15, 'add_sarvcustomdataset'),
(44, 'Can change sarv custom dataset', 15, 'change_sarvcustomdataset'),
(45, 'Can delete sarv custom dataset', 15, 'delete_sarvcustomdataset'),
(46, 'Can add sarv menu', 16, 'add_sarvmenu'),
(47, 'Can change sarv menu', 16, 'change_sarvmenu'),
(48, 'Can delete sarv menu', 16, 'delete_sarvmenu'),
(49, 'Can add sarv page', 17, 'add_sarvpage'),
(50, 'Can change sarv page', 17, 'change_sarvpage'),
(51, 'Can delete sarv page', 17, 'delete_sarvpage'),
(52, 'Can add sarv session', 18, 'add_sarvsession'),
(53, 'Can change sarv session', 18, 'change_sarvsession'),
(54, 'Can delete sarv session', 18, 'delete_sarvsession'),
(55, 'Can add user', 19, 'add_user'),
(56, 'Can change user', 19, 'change_user'),
(57, 'Can delete user', 19, 'delete_user');

-- --------------------------------------------------------

--
-- Table structure for table `auth_user`
--

CREATE TABLE IF NOT EXISTS `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(30) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `email` varchar(75) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `auth_user_groups`
--

CREATE TABLE IF NOT EXISTS `auth_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`group_id`),
  KEY `auth_user_groups_e8701ad4` (`user_id`),
  KEY `auth_user_groups_0e939a4f` (`group_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `auth_user_user_permissions`
--

CREATE TABLE IF NOT EXISTS `auth_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`permission_id`),
  KEY `auth_user_user_permissions_e8701ad4` (`user_id`),
  KEY `auth_user_user_permissions_8373b171` (`permission_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `django_content_type`
--

CREATE TABLE IF NOT EXISTS `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_1b95736e6a361bd0_uniq` (`app_label`,`model`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=20 ;

--
-- Dumping data for table `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(7, 'acl', 'acl'),
(8, 'acl', 'acldestination'),
(9, 'acl', 'aclgroup'),
(10, 'acl', 'aclpermissiontype'),
(11, 'acl', 'aclrightsgroup'),
(12, 'acl', 'aclrightsgrouppermissiontype'),
(13, 'acl', 'aclusergroup'),
(2, 'auth', 'group'),
(1, 'auth', 'permission'),
(3, 'auth', 'user'),
(4, 'contenttypes', 'contenttype'),
(14, 'nextify', 'database'),
(15, 'nextify', 'sarvcustomdataset'),
(16, 'nextify', 'sarvmenu'),
(17, 'nextify', 'sarvpage'),
(18, 'nextify', 'sarvsession'),
(19, 'nextify', 'user'),
(5, 'sessions', 'session'),
(6, 'sites', 'site');

-- --------------------------------------------------------

--
-- Table structure for table `django_migrations`
--

CREATE TABLE IF NOT EXISTS `django_migrations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=16 ;

--
-- Dumping data for table `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'contenttypes', '0001_initial', '2015-12-30 15:29:18'),
(2, 'contenttypes', '0002_remove_content_type_name', '2015-12-30 15:29:18'),
(3, 'nextify', '0001_initial', '2015-12-30 15:29:18'),
(4, 'acl', '0001_initial', '2015-12-30 15:29:18'),
(5, 'acl', '0002_add_contenttypes_fk_field', '2015-12-30 15:29:18'),
(6, 'auth', '0001_initial', '2015-12-30 15:29:18'),
(7, 'auth', '0002_alter_permission_name_max_length', '2015-12-30 15:29:18'),
(8, 'auth', '0003_alter_user_email_max_length', '2015-12-30 15:29:18'),
(9, 'auth', '0004_alter_user_username_opts', '2015-12-30 15:29:18'),
(10, 'auth', '0005_alter_user_last_login_null', '2015-12-30 15:29:18'),
(11, 'auth', '0006_require_contenttypes_0002', '2015-12-30 15:29:18'),
(12, 'nextify', '0002_page_fk_to_acl', '2015-12-30 15:29:18'),
(13, 'nextify', '0003_merge', '2015-12-30 15:29:18'),
(14, 'sessions', '0001_initial', '2015-12-30 15:29:18'),
(15, 'sites', '0001_initial', '2015-12-30 15:29:18');

-- --------------------------------------------------------

--
-- Table structure for table `django_session`
--

CREATE TABLE IF NOT EXISTS `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_de54fa62` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `django_site`
--

CREATE TABLE IF NOT EXISTS `django_site` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `domain` varchar(100) NOT NULL,
  `name` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=2 ;

--
-- Dumping data for table `django_site`
--

INSERT INTO `django_site` (`id`, `domain`, `name`) VALUES
(1, 'example.com', 'example.com');

--
-- Constraints for dumped tables
--

--
-- Constraints for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD CONSTRAINT `auth_group__permission_id_5dda2f398d02dd3a_fk_auth_permission_id` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_group_permission_group_id_6987d2aa9d6e5e31_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

--
-- Constraints for table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD CONSTRAINT `auth__content_type_id_75468393a4755ec7_fk_django_content_type_id` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);

--
-- Constraints for table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD CONSTRAINT `auth_user_groups_group_id_1c57ce648edfd805_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  ADD CONSTRAINT `auth_user_groups_user_id_4ae0ee2ceed0edda_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD CONSTRAINT `auth_user_u_permission_id_35931e564e58947a_fk_auth_permission_id` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_user_user_permissio_user_id_3a6bd72d0dd27c4_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
