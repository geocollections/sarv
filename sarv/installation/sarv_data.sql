-- phpMyAdmin SQL Dump
-- version 4.0.4.2
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Dec 31, 2015 at 12:39 AM
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
-- Dumping data for table `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'nextify', '0001_initial', '2015-12-30 18:54:48'),
(2, 'acl', '0001_initial', '2015-12-30 18:54:48'),
(3, 'nextify', '0002_page_fk_to_acl', '2015-12-30 18:54:48'),
(4, 'contenttypes', '0001_initial', '2015-12-30 18:54:48'),
(5, 'contenttypes', '0002_remove_content_type_name', '2015-12-30 18:54:48');

--
-- Dumping data for table `sarv_acl`
--

INSERT INTO `sarv_acl` (`id`, `id_tested`, `type`, `id_destination_row`, `id_destination`, `id_permission`, `rights_group_id`, `destination_type`) VALUES
(1, 1, 'group', 1, NULL, 1, 5, 17),
(2, 1, 'group', 2, NULL, 1, 5, 17),
(3, 1, 'group', 3, NULL, 1, 5, 17),
(4, 1, 'group', 6, NULL, 1, 5, 17);

--
-- Dumping data for table `sarv_acl_group`
--

INSERT INTO `sarv_acl_group` (`id`, `keyword`, `name`) VALUES
(1, 'git', 'gittest');

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
(1, 'git', 'gittest', '');

--
-- Dumping data for table `sarv_menu`
--

INSERT INTO `sarv_menu` (`id`, `column`, `row`, `page_id`, `usergroup_id`) VALUES
(1, 1, 0, 1, 1),
(2, 1, 1, 2, 1),
(3, 1, 2, 3, 1),
(9, 1, 4, 6, 1);

--
-- Dumping data for table `sarv_page`
--

INSERT INTO `sarv_page` (`id`, `name`, `url`, `language`, `visibility`, `settings`) VALUES
(1, 'Administration', '', 'en-us', 'acl', NULL),
(2, 'Pages administration', 'admin/menu', 'en-us', 'acl', NULL),
(3, 'User right administration', 'admin/acl', 'en-us', 'acl', NULL),
(6, 'Issue', 'issue', 'en-us', 'acl', NULL);

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`id`, `username`, `forename`, `surename`, `email`, `remarks`, `isikukood`, `priv`, `dbs`, `db`, `user_added`, `date_added`, `user_changed`, `date_changed`, `timestamp`, `database_id`) VALUES
(1, 'admin', '', '', '', '', 0, NULL, '', 'git', 'admin', '2015-12-30 23:35:45', '', '2015-12-30 23:35:45', '2015-12-30 23:35:45', 1);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
