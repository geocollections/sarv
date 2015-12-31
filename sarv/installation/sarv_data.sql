-- phpMyAdmin SQL Dump
-- version 4.0.4.2
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Dec 31, 2015 at 01:18 PM
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

--
-- Dumping data for table `sarv_acl`
--

INSERT INTO `sarv_acl` (`id`, `id_tested`, `type`, `id_destination_row`, `id_destination`, `id_permission`, `rights_group_id`, `destination_type`) VALUES
(1, 1, 'group', 1, NULL, 1, 5, 17),
(2, 1, 'group', 2, NULL, 1, 5, 17),
(3, 1, 'group', 3, NULL, 1, 5, 17);

--
-- Dumping data for table `sarv_acl_group`
--

INSERT INTO `sarv_acl_group` (`id`, `keyword`, `name`) VALUES
(1, 'tes', 'test');

--
-- Dumping data for table `sarv_acl_permission_type`
--

INSERT INTO `sarv_acl_permission_type` (`id`, `type_name`) VALUES
(1, 'read'),
(2, 'create'),
(3, 'update'),
(4, 'delete');

--
-- Dumping data for table `sarv_acl_rights_group`
--

INSERT INTO `sarv_acl_rights_group` (`id`, `name`) VALUES
(1, 'guest'),
(2, 'viewer'),
(3, 'user'),
(4, 'editor'),
(5, 'admin');

--
-- Dumping data for table `sarv_acl_user_group`
--

INSERT INTO `sarv_acl_user_group` (`id`, `id_group`, `id_user`) VALUES
(1, 1, 1);

--
-- Dumping data for table `sarv_database`
--

INSERT INTO `sarv_database` (`id`, `acronym`, `name`, `name_en`) VALUES
(1, 'tes', 'test', '');

--
-- Dumping data for table `sarv_menu`
--

INSERT INTO `sarv_menu` (`id`, `column`, `row`, `page_id`, `usergroup_id`) VALUES
(1, 1, 0, 1, NULL),
(2, 1, 1, 2, NULL),
(3, 1, 2, 3, NULL);

--
-- Dumping data for table `sarv_page`
--

INSERT INTO `sarv_page` (`id`, `name`, `url`, `language`, `visibility`, `settings`) VALUES
(1, 'Administration', '', 'en-us', 'acl', NULL),
(2, 'Pages administration', 'admin/menu', 'en-us', 'acl', NULL),
(3, 'User right administration', 'admin/acl', 'en-us', 'acl', NULL);

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`id`, `username`, `forename`, `surename`, `email`, `remarks`, `isikukood`, `priv`, `dbs`, `db`, `user_added`, `date_added`, `user_changed`, `date_changed`, `timestamp`, `database_id`) VALUES
(1, 'admin', '', '', '', '', 0, NULL, '', 'tes', 'admin', '2015-12-31 13:17:15', '', '2015-12-31 13:17:15', '2015-12-31 13:17:15', 1);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
