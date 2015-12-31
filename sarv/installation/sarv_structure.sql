-- phpMyAdmin SQL Dump
-- version 4.0.4.2
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Dec 30, 2015 at 06:55 PM
-- Server version: 5.5.34-0ubuntu0.13.04.1
-- PHP Version: 5.4.9-4ubuntu2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `sarv`
--
CREATE DATABASE IF NOT EXISTS `sarv` DEFAULT CHARACTER SET latin1 COLLATE latin1_swedish_ci;
USE `sarv`;

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
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=6 ;


--
-- Table structure for table `sarv_acl`
--

CREATE TABLE IF NOT EXISTS `sarv_acl` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `id_tested` int(10) unsigned NOT NULL,
  `type` varchar(50) NOT NULL,
  `id_destination_row` int(10) unsigned NOT NULL,
  `id_destination` int(11),
  `id_permission` int(11),
  `rights_group_id` int(11),
  `destination_type` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `sarv_acl_6018a06a` (`id_destination`),
  KEY `sarv_acl_dc4f4ac7` (`id_permission`),
  KEY `sarv_acl_10adf4ea` (`rights_group_id`),
  KEY `sarv_acl_6268b8fa` (`destination_type`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `sarv_acl_destination`
--

CREATE TABLE IF NOT EXISTS `sarv_acl_destination` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `keyword` varchar(50) DEFAULT NULL,
  `model` varchar(50) DEFAULT NULL,
  `id_ct` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `sarv_acl_group`
--

CREATE TABLE IF NOT EXISTS `sarv_acl_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `keyword` varchar(20) NOT NULL,
  `name` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `sarv_acl_permission_type`
--

CREATE TABLE IF NOT EXISTS `sarv_acl_permission_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `type_name` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `sarv_acl_rights_group`
--

CREATE TABLE IF NOT EXISTS `sarv_acl_rights_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(20) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `sarv_acl_rights_group_permission_type`
--

CREATE TABLE IF NOT EXISTS `sarv_acl_rights_group_permission_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `scope` varchar(10) NOT NULL,
  `rights_group_id` int(11) NOT NULL,
  `permission_type_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `sar_rights_group_id_341e09529b18a41a_fk_sarv_acl_rights_group_id` (`rights_group_id`),
  KEY `D81460e8d9f1d88af6f13f9f4f1161a9` (`permission_type_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `sarv_acl_user_group`
--

CREATE TABLE IF NOT EXISTS `sarv_acl_user_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `id_group` int(11) DEFAULT NULL,
  `id_user` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `sarv_acl_user_gro_id_group_1f7f683cddc968e6_fk_sarv_acl_group_id` (`id_group`),
  KEY `sarv_acl_user_group_id_user_46dabfbed0538e9_fk_user_id` (`id_user`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `sarv_custom_datasets`
--

CREATE TABLE IF NOT EXISTS `sarv_custom_datasets` (
  `name` varchar(100) NOT NULL,
  `user` varchar(50) NOT NULL,
  `params` longtext NOT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `sarv_database`
--

CREATE TABLE IF NOT EXISTS `sarv_database` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `acronym` varchar(5) NOT NULL,
  `name` varchar(50) NOT NULL,
  `name_en` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `acronym` (`acronym`),
  UNIQUE KEY `name` (`name`),
  UNIQUE KEY `name_en` (`name_en`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `sarv_issue`
--

CREATE TABLE IF NOT EXISTS `sarv_issue` (
  `title` varchar(150) NOT NULL,
  `description` longtext NOT NULL,
  `response` longtext NOT NULL,
  `url` longtext NOT NULL,
  `issue_type` int(11) DEFAULT NULL,
  `reported_by` int(11) DEFAULT NULL,
  `reported_to` int(11) DEFAULT NULL,
  `database_id` int(11) NOT NULL,
  `resolved` tinyint(1) NOT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_added` varchar(10) NOT NULL,
  `date_added` datetime DEFAULT NULL,
  `user_changed` varchar(10) NOT NULL,
  `date_changed` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `sarv_issue_issue_type_54c821ae3c798011_fk_sarv_issue_type_id` (`issue_type`),
  KEY `sarv_issue_reported_by_52608e5cc12ece53_fk_user_id` (`reported_by`),
  KEY `sarv_issue_reported_to_5260980449a3a933_fk_user_id` (`reported_to`),
  KEY `sarv_issue_database_id_5e40aee0c99ed873_fk_sarv_database_id` (`database_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `sarv_issue_type`
--

CREATE TABLE IF NOT EXISTS `sarv_issue_type` (
  `issue_type` varchar(25) NOT NULL,
  `user_created_id` int(11) DEFAULT NULL,
  `timestamp_created` datetime DEFAULT NULL,
  `user_modified_id` int(11) DEFAULT NULL,
  `timestamp_modified` datetime DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`),
  KEY `sarv_issue_type_user_created_id_5577eb4137b922fe_fk_user_id` (`user_created_id`),
  KEY `sarv_issue_type_user_modified_id_3475839f8bbfadcc_fk_user_id` (`user_modified_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `sarv_menu`
--

CREATE TABLE IF NOT EXISTS `sarv_menu` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `column` int(11) DEFAULT NULL,
  `row` int(11) DEFAULT NULL,
  `page_id` int(11),
  `usergroup_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `sarv_menu_1a63c800` (`page_id`),
  KEY `sarv_menu_50ce08ac` (`usergroup_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `sarv_page`
--

CREATE TABLE IF NOT EXISTS `sarv_page` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(400) NOT NULL,
  `url` varchar(400) DEFAULT NULL,
  `language` varchar(6) NOT NULL,
  `visibility` varchar(10) NOT NULL,
  `settings` longtext,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `sarv_session`
--

CREATE TABLE IF NOT EXISTS `sarv_session` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user` varchar(30) NOT NULL,
  `active` int(11) NOT NULL,
  `session_start` datetime NOT NULL,
  `session_end` datetime DEFAULT NULL,
  `database_id` int(11) NOT NULL,
  `timestamp` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE IF NOT EXISTS `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(10) NOT NULL,
  `forename` varchar(50) NOT NULL,
  `surename` varchar(50) NOT NULL,
  `email` varchar(100) NOT NULL,
  `remarks` longtext NOT NULL,
  `isikukood` bigint(20) DEFAULT NULL,
  `priv` int(11) DEFAULT NULL,
  `dbs` varchar(50) NOT NULL,
  `db` varchar(20) NOT NULL,
  `user_added` varchar(10) NOT NULL,
  `date_added` datetime DEFAULT NULL,
  `user_changed` varchar(10) NOT NULL,
  `date_changed` datetime DEFAULT NULL,
  `timestamp` datetime DEFAULT NULL,
  `database_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  KEY `user_database_id_51d8e70c6d6c31d2_fk_sarv_database_id` (`database_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `sarv_acl`
--
ALTER TABLE `sarv_acl`
  ADD CONSTRAINT `sarv__id_destination_4fcd061abc6fe5fa_fk_sarv_acl_destination_id` FOREIGN KEY (`id_destination`) REFERENCES `sarv_acl_destination` (`id`),
  ADD CONSTRAINT `sar_rights_group_id_6a5357e878899a88_fk_sarv_acl_rights_group_id` FOREIGN KEY (`rights_group_id`) REFERENCES `sarv_acl_rights_group` (`id`),
  ADD CONSTRAINT `sa_id_permission_6e76fa7e57da9a9a_fk_sarv_acl_permission_type_id` FOREIGN KEY (`id_permission`) REFERENCES `sarv_acl_permission_type` (`id`);

--
-- Constraints for table `sarv_acl_rights_group_permission_type`
--
ALTER TABLE `sarv_acl_rights_group_permission_type`
  ADD CONSTRAINT `D81460e8d9f1d88af6f13f9f4f1161a9` FOREIGN KEY (`permission_type_id`) REFERENCES `sarv_acl_permission_type` (`id`),
  ADD CONSTRAINT `sar_rights_group_id_341e09529b18a41a_fk_sarv_acl_rights_group_id` FOREIGN KEY (`rights_group_id`) REFERENCES `sarv_acl_rights_group` (`id`);

--
-- Constraints for table `sarv_acl_user_group`
--
ALTER TABLE `sarv_acl_user_group`
  ADD CONSTRAINT `sarv_acl_user_group_id_user_46dabfbed0538e9_fk_user_id` FOREIGN KEY (`id_user`) REFERENCES `user` (`id`),
  ADD CONSTRAINT `sarv_acl_user_gro_id_group_1f7f683cddc968e6_fk_sarv_acl_group_id` FOREIGN KEY (`id_group`) REFERENCES `sarv_acl_group` (`id`);

--
-- Constraints for table `sarv_issue`
--
ALTER TABLE `sarv_issue`
  ADD CONSTRAINT `sarv_issue_database_id_5e40aee0c99ed873_fk_sarv_database_id` FOREIGN KEY (`database_id`) REFERENCES `sarv_database` (`id`),
  ADD CONSTRAINT `sarv_issue_issue_type_54c821ae3c798011_fk_sarv_issue_type_id` FOREIGN KEY (`issue_type`) REFERENCES `sarv_issue_type` (`id`),
  ADD CONSTRAINT `sarv_issue_reported_by_52608e5cc12ece53_fk_user_id` FOREIGN KEY (`reported_by`) REFERENCES `user` (`id`),
  ADD CONSTRAINT `sarv_issue_reported_to_5260980449a3a933_fk_user_id` FOREIGN KEY (`reported_to`) REFERENCES `user` (`id`);

--
-- Constraints for table `sarv_issue_type`
--
ALTER TABLE `sarv_issue_type`
  ADD CONSTRAINT `sarv_issue_type_user_modified_id_3475839f8bbfadcc_fk_user_id` FOREIGN KEY (`user_modified_id`) REFERENCES `user` (`id`),
  ADD CONSTRAINT `sarv_issue_type_user_created_id_5577eb4137b922fe_fk_user_id` FOREIGN KEY (`user_created_id`) REFERENCES `user` (`id`);

--
-- Constraints for table `sarv_menu`
--
ALTER TABLE `sarv_menu`
  ADD CONSTRAINT `sarv_men_usergroup_id_19867d9ff5b2f890_fk_sarv_acl_user_group_id` FOREIGN KEY (`usergroup_id`) REFERENCES `sarv_acl_user_group` (`id`),
  ADD CONSTRAINT `sarv_menu_page_id_ae776b8846ace28_fk_sarv_page_id` FOREIGN KEY (`page_id`) REFERENCES `sarv_page` (`id`);

--
-- Constraints for table `user`
--
ALTER TABLE `user`
  ADD CONSTRAINT `user_database_id_51d8e70c6d6c31d2_fk_sarv_database_id` FOREIGN KEY (`database_id`) REFERENCES `sarv_database` (`id`);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
