-- phpMyAdmin SQL Dump
-- version 4.9.1
-- https://www.phpmyadmin.net/
--
-- Хост: 127.0.0.1
-- Время создания: Апр 18 2021 г., 15:55
-- Версия сервера: 10.4.8-MariaDB
-- Версия PHP: 7.3.10

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- База данных: `diplom`
--

DELIMITER $$
--
-- Процедуры
--
CREATE DEFINER=`root`@`127.0.0.1` PROCEDURE `addCamera` (IN `ip` VARCHAR(20), IN `pt` INT(10))  NO SQL
INSERT INTO cameras (IP_address, PORT, cam_is_running, cam_is_allowed) VALUES (ip, pt, '0', '1')$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `deleteCamera` (IN `ID` INT)  NO SQL
DELETE FROM cameras WHERE cameras.ID = ID$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `editCamera` (IN `ID` INT, IN `new_ip` VARCHAR(15), IN `new_port` VARCHAR(10))  NO SQL
UPDATE cameras SET cameras.IP_address = new_ip, cameras.PORT = new_port WHERE cameras.ID = ID$$

DELIMITER ;

-- --------------------------------------------------------

--
-- Структура таблицы `cameras`
--

CREATE TABLE `cameras` (
  `ID` int(11) NOT NULL,
  `IP_address` varchar(15) NOT NULL,
  `PORT` varchar(10) NOT NULL,
  `cam_is_running` int(11) NOT NULL,
  `cam_is_allowed` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Дамп данных таблицы `cameras`
--

INSERT INTO `cameras` (`ID`, `IP_address`, `PORT`, `cam_is_running`, `cam_is_allowed`) VALUES
(1, '127.0.0.1', '1212', 0, 1),
(2, '123.125.128.98', '5000', 0, 1),
(31, '127.0.0.1', '10001', 0, 1);

-- --------------------------------------------------------

--
-- Структура таблицы `users`
--

CREATE TABLE `users` (
  `Login` varchar(20) NOT NULL,
  `First_name` varchar(50) NOT NULL,
  `Last_name` varchar(50) NOT NULL,
  `Password` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Дамп данных таблицы `users`
--

INSERT INTO `users` (`Login`, `First_name`, `Last_name`, `Password`) VALUES
('ABC', 'Антонов', 'Владимир', '01051995');

--
-- Индексы сохранённых таблиц
--

--
-- Индексы таблицы `cameras`
--
ALTER TABLE `cameras`
  ADD PRIMARY KEY (`ID`);

--
-- Индексы таблицы `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`Login`);

--
-- AUTO_INCREMENT для сохранённых таблиц
--

--
-- AUTO_INCREMENT для таблицы `cameras`
--
ALTER TABLE `cameras`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=44;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
