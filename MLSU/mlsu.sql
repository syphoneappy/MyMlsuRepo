-- phpMyAdmin SQL Dump
-- version 4.8.5
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Sep 21, 2020 at 01:44 PM
-- Server version: 10.1.38-MariaDB
-- PHP Version: 7.3.3

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `mlsu`
--

-- --------------------------------------------------------

--
-- Table structure for table `asprequest`
--

CREATE TABLE `asprequest` (
  `id` int(11) NOT NULL,
  `user1` varchar(111) NOT NULL,
  `user2` varchar(111) NOT NULL,
  `SubCode` varchar(111) NOT NULL,
  `Sem` int(11) NOT NULL,
  `DD` date NOT NULL,
  `details` mediumtext NOT NULL,
  `pdf` longtext NOT NULL,
  `marks` int(11) NOT NULL,
  `TotalMarks` int(11) NOT NULL,
  `image` mediumtext NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `asprequest`
--

INSERT INTO `asprequest` (`id`, `user1`, `user2`, `SubCode`, `Sem`, `DD`, `details`, `pdf`, `marks`, `TotalMarks`, `image`) VALUES
(1, '98023', 'himashutripathi669@gmail.com', 'SBCA201', 0, '2020-05-31', 'This Assignment details are as-:\r\n', '', 0, 0, ''),
(2, '16188', 'example@gmail.com', 'SBCA204', 0, '2020-09-29', 'Please Submit the assignment on the topic Of advance technology or latest technology on the fields of research such as-:\r\n1.artificial intelligence in Civil engg.\r\n2.artificial intelligence in medical engg.\r\n3.artificial intelligence in social networking.\r\n4.artificial intelligence and data science,data mining\r\n5.artificial intelligence role in future wars.', '', 0, 0, ''),
(3, '98023', 'example@gmail.com', 'SBCA204', 0, '2020-09-29', 'Please Submit the assignment on the topic Of advance technology.', '', 0, 0, ''),
(4, '12345', 'example@gmail.com', 'SBCA 205', 0, '2020-10-20', 'Same Topic that was given in the class today.', '', 0, 0, ''),
(5, '12345', 'example@gmail.com', 'SBCA 207', 5, '2020-09-08', 'lksjlkcjslkjscl', 'wAdXX9mCqU9EaQ.pdf', 390, 500, '3GPcNMdrKJQdjQ.png'),
(6, '5656', 'example@gmail.com', 'SBCA201', 2, '2020-09-30', 'zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz  jakljscljcsl hcshkdc', '', 0, 0, '');

-- --------------------------------------------------------

--
-- Table structure for table `collauth`
--

CREATE TABLE `collauth` (
  `ClgId` int(11) NOT NULL,
  `RegistrationId` varchar(111) NOT NULL,
  `ProfName` varchar(255) NOT NULL,
  `Password` varchar(111) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `collauth`
--

INSERT INTO `collauth` (`ClgId`, `RegistrationId`, `ProfName`, `Password`) VALUES
(20, 'MLSU 7671', 'Himanshu Tripathi', '$pbkdf2-sha256$29000$RagVglDqfe/9n3PuHaM0pg$zNBAdxWDNlgg7dkkA4ozsPLriDI4F1uhD55LJpsT2vs'),
(21, 'MLSU 4040', 'Harsh Tripathi', '$pbkdf2-sha256$29000$GOMcA2Ds3TtHKOWc8967lw$KCfGan.zKPfjBrgya1OKhgkSKqbgA4i3g1WmF7ldEiQ');

-- --------------------------------------------------------

--
-- Table structure for table `collegecourse`
--

CREATE TABLE `collegecourse` (
  `Cid` int(11) NOT NULL,
  `SName` varchar(111) NOT NULL,
  `Cname` varchar(111) NOT NULL,
  `Year` varchar(111) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `collegecourse`
--

INSERT INTO `collegecourse` (`Cid`, `SName`, `Cname`, `Year`) VALUES
(2, 'CBCS', 'MCA', '2001'),
(3, 'CBCS', 'BCA', '2001'),
(4, 'CBCS', 'MSCIT', '2001'),
(5, 'CBCS', 'BTECHCS', '2001'),
(6, 'CBCS', 'MTECHIT', '2001'),
(7, 'Annual', 'MCA', '2001'),
(8, 'Annual', 'BCA', '2001'),
(9, 'Annual', 'BTECHCS', '2001'),
(10, 'Annual', 'MTECHIT', '1999'),
(11, 'Annual', 'MSCIT', '1999'),
(12, 'Semester', 'MCA', '2005'),
(13, 'Semester', 'BCA', '2005'),
(14, 'Semester', 'MSCIT', '2005');

-- --------------------------------------------------------

--
-- Table structure for table `courseid`
--

CREATE TABLE `courseid` (
  `Id` int(11) NOT NULL,
  `Course` varchar(111) NOT NULL,
  `date` date NOT NULL,
  `time` time NOT NULL,
  `details` longtext NOT NULL,
  `pdf` mediumtext NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `courseid`
--

INSERT INTO `courseid` (`Id`, `Course`, `date`, `time`, `details`, `pdf`) VALUES
(3, 'CBCS MCA', '2020-09-02', '14:48:00', 'It is great opportunity for me to have the BACHELOR IN COMPUTER APPLICATION (BCA) in UNIVERSITY COLLEGE OF SCIENCE, UDAIPUR. In the accomplishment of this degree I am submitting a project report on “PHOTO GALLERY”. Subject to the limitation of time efforts and resources every possible attempt has been made to study the problem deeply. The whole project is measured through the questionnaire, the data further analysed and interpreted and the result was obtained.  \r\n\r\n I hope that readers will enjoy reading this report\r\n', '1qe1fuCeyKReKg.pdf'),
(4, 'CBCS MCA', '2020-09-07', '17:51:00', '\r\nWhat is php?\r\nPHP (recursive acronym for \"PHP: Hypertext Preprocessor\") is a widely-used Open Source general-purpose scripting language that is especially suited for Web development and can be embedded into HTML\r\nPHP stands for PHP: Hypertext Preprocessor\r\nPHP is a server-side scripting language, like ASP\r\nPHP scripts are executed on the server\r\nPHP supports many databases (MySQL, Informix, Oracle, Sybase, Solid, PostgreSQL, Generic ODBC, etc.)\r\nPHP is an open source software\r\nPHP is free to download and use\r\n\r\nWhat is php file?\r\nPHP files can contain text, HTML tags and scripts\r\nPHP files are returned to the browser as plain HTML \r\n', 'AZzMCKotAePGBA.pdf'),
(5, 'Annual MCA', '2020-09-25', '16:05:00', '', 'FW7DcYxEqx0c3A');

-- --------------------------------------------------------

--
-- Table structure for table `notification`
--

CREATE TABLE `notification` (
  `Nid` int(11) NOT NULL,
  `Title` date NOT NULL,
  `time` time NOT NULL,
  `Noti` mediumtext NOT NULL,
  `pdf` mediumtext NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `notification`
--

INSERT INTO `notification` (`Nid`, `Title`, `time`, `Noti`, `pdf`) VALUES
(3, '2020-09-22', '04:06:00', 'MLSU\\FolderDB\\Notification\\Global', 'QfMDPy-i6s55cw.pdf'),
(4, '2020-09-09', '17:49:00', '/python practice/MyMlsuRepo/MLSU/Student/static/Global', 'BKbjFWEhCLynWA.pdf'),
(5, '2020-09-09', '15:56:00', 'lK;lksc;ds', 'cRSGeWvtOArBmw.pdf');

-- --------------------------------------------------------

--
-- Table structure for table `post`
--

CREATE TABLE `post` (
  `id` int(11) NOT NULL,
  `RollNo` varchar(111) NOT NULL,
  `comment` longtext NOT NULL,
  `image` longtext NOT NULL,
  `accounttype` varchar(111) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `post`
--

INSERT INTO `post` (`id`, `RollNo`, `comment`, `image`, `accounttype`) VALUES
(1, '16188', 'Hey ', '6jQM5FZvovxgVw.jpg', 'Public'),
(2, '16188', 'This Is my Photo two', 'XQ17Pbs0-k0fzQ.jpg', 'Public'),
(3, '16188', 'This is a photo three', 'hPIAIygYskUplw.jpg', 'Public');

-- --------------------------------------------------------

--
-- Table structure for table `senddocsadmin`
--

CREATE TABLE `senddocsadmin` (
  `id` int(11) NOT NULL,
  `user` varchar(111) NOT NULL,
  `Email` varchar(111) NOT NULL,
  `Course` varchar(111) NOT NULL,
  `SubjectCode` varchar(111) NOT NULL,
  `SemYear` varchar(111) NOT NULL,
  `RollNo` varchar(111) NOT NULL,
  `Marks` varchar(111) NOT NULL,
  `TMarks` varchar(111) NOT NULL,
  `image` varchar(1111) NOT NULL,
  `pdf` mediumtext NOT NULL,
  `guide` mediumtext NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `senddocsadmin`
--

INSERT INTO `senddocsadmin` (`id`, `user`, `Email`, `Course`, `SubjectCode`, `SemYear`, `RollNo`, `Marks`, `TMarks`, `image`, `pdf`, `guide`) VALUES
(3, 'MLSU8990', 'example@gmail.com', 'CBCS MCA', 'SBCA205', '2020', '16188', '300', '500', 'nwyvQag5bjZhHg.jpeg', 'BSo4wh4d5LG38Q.pdf', 'oisdjoijsoi'),
(4, 'MLSU8990', 'example@gmail.com', 'CBCS MCA', 'SMCA201', '2020', '98023', '209', '201', '7Rylny8KjIGHOQ.jpeg', '1Pdbb9y0O5l6tw.pdf', 'skcl;ksc;ljcsjdvskljsdvlkjdsv'),
(6, 'MLSU8990', 'himashutripathi669@gmail.com', 'CBCS MSCIT', 'SCOc2389', '2020', '98023', '', '', '', 'vRM6cqqnafQt7Q.pdf', 'Guidline'),
(7, 'MLSU8990', 'example@gmail.com', 'CBCS MCA', 'SBCA2001', '2001', '12345', '', '', '', 'CJJsj1zr-Vut7A.pdf', 'Harsh Tripathi');

-- --------------------------------------------------------

--
-- Table structure for table `studentacc`
--

CREATE TABLE `studentacc` (
  `id` int(111) NOT NULL,
  `user1` varchar(111) NOT NULL,
  `user2` varchar(111) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `studentacc`
--

INSERT INTO `studentacc` (`id`, `user1`, `user2`) VALUES
(1, '5656', '16188');

-- --------------------------------------------------------

--
-- Table structure for table `studentd`
--

CREATE TABLE `studentd` (
  `Sid` int(11) NOT NULL,
  `RollNo` varchar(111) NOT NULL,
  `CourseId` varchar(111) NOT NULL,
  `Email` varchar(111) NOT NULL,
  `Password` varchar(111) NOT NULL,
  `Name` text NOT NULL,
  `image` varchar(1500) NOT NULL,
  `Bio` mediumtext NOT NULL,
  `Atype` varchar(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `studentd`
--

INSERT INTO `studentd` (`Sid`, `RollNo`, `CourseId`, `Email`, `Password`, `Name`, `image`, `Bio`, `Atype`) VALUES
(1, '16188', 'CBCS MCA', 'harshtripathi669@gmail.com', 'FunnyFun@992', 'HARSH TRIPATHI', 'P8PhXTRsAYvoBw.jpg', 'This is a Bio', 'Public'),
(2, '98023', 'Semester MCA', 'HarshTripathi1999@gmail.com', 'FunnyFun@992', 'HARSH TRIPATHI', 'mQZgiwWnMxw7YA.jpg', '', ''),
(3, '12345', 'CBCS MCA', 'harsh123@gmail.com', 'FunnyFun@992', 'Harsh', 'uVzGrn-F5vApaQ.jpg', '', ''),
(4, '5656', 'CBCS BCA', 'BhavinJain@gmail.com', 'Bhavin@123', 'Bhavin Jain', 'k0a0QCv009pVUA.jpg', '', '');

-- --------------------------------------------------------

--
-- Table structure for table `studentreq`
--

CREATE TABLE `studentreq` (
  `id` int(11) NOT NULL,
  `user1` varchar(1111) NOT NULL,
  `user2` varchar(1111) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `studentreq`
--

INSERT INTO `studentreq` (`id`, `user1`, `user2`) VALUES
(2, '98023', '16188'),
(3, '12345', '16188'),
(4, '12345', '98023');

-- --------------------------------------------------------

--
-- Table structure for table `teacherd`
--

CREATE TABLE `teacherd` (
  `id` int(11) NOT NULL,
  `FirstName` text NOT NULL,
  `LastName` text NOT NULL,
  `Email` varchar(200) NOT NULL,
  `Password` varchar(200) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `teacherd`
--

INSERT INTO `teacherd` (`id`, `FirstName`, `LastName`, `Email`, `Password`) VALUES
(1, 'Himanshu', 'Tripathi', 'himashutripathi669@gmail.com', 'Funnyfun@992'),
(2, 'HARSH', 'TRIPATHI', 'example@gmail.com', 'FunnyFun@992'),
(3, 'Anita ', 'TRIPATHI', 'anitatripathi.sharma@gmail.com', 'FunnyFun@992'),
(4, 'sushil', '', 'sushiltripathi@gmail.com', 'FunnyFun@992');

-- --------------------------------------------------------

--
-- Table structure for table `tprequest`
--

CREATE TABLE `tprequest` (
  `TPid` int(11) NOT NULL,
  `TPName1` varchar(2000) NOT NULL,
  `TPName2` varchar(2000) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `trequest`
--

CREATE TABLE `trequest` (
  `id` int(11) NOT NULL,
  `user1` varchar(111) NOT NULL,
  `user2` varchar(111) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `trequest`
--

INSERT INTO `trequest` (`id`, `user1`, `user2`) VALUES
(12, 'MLSU 4040', 'himashutripathi669@gmail.com');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `asprequest`
--
ALTER TABLE `asprequest`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `collauth`
--
ALTER TABLE `collauth`
  ADD PRIMARY KEY (`ClgId`);

--
-- Indexes for table `collegecourse`
--
ALTER TABLE `collegecourse`
  ADD PRIMARY KEY (`Cid`);

--
-- Indexes for table `courseid`
--
ALTER TABLE `courseid`
  ADD PRIMARY KEY (`Id`);

--
-- Indexes for table `notification`
--
ALTER TABLE `notification`
  ADD PRIMARY KEY (`Nid`);

--
-- Indexes for table `post`
--
ALTER TABLE `post`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `senddocsadmin`
--
ALTER TABLE `senddocsadmin`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `studentacc`
--
ALTER TABLE `studentacc`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `studentd`
--
ALTER TABLE `studentd`
  ADD PRIMARY KEY (`Sid`),
  ADD UNIQUE KEY `RollNo` (`RollNo`),
  ADD UNIQUE KEY `Email` (`Email`);

--
-- Indexes for table `studentreq`
--
ALTER TABLE `studentreq`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `teacherd`
--
ALTER TABLE `teacherd`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `Email` (`Email`);

--
-- Indexes for table `tprequest`
--
ALTER TABLE `tprequest`
  ADD PRIMARY KEY (`TPid`);

--
-- Indexes for table `trequest`
--
ALTER TABLE `trequest`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `asprequest`
--
ALTER TABLE `asprequest`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `collauth`
--
ALTER TABLE `collauth`
  MODIFY `ClgId` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=22;

--
-- AUTO_INCREMENT for table `collegecourse`
--
ALTER TABLE `collegecourse`
  MODIFY `Cid` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- AUTO_INCREMENT for table `courseid`
--
ALTER TABLE `courseid`
  MODIFY `Id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `notification`
--
ALTER TABLE `notification`
  MODIFY `Nid` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `post`
--
ALTER TABLE `post`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `senddocsadmin`
--
ALTER TABLE `senddocsadmin`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `studentacc`
--
ALTER TABLE `studentacc`
  MODIFY `id` int(111) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `studentd`
--
ALTER TABLE `studentd`
  MODIFY `Sid` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `studentreq`
--
ALTER TABLE `studentreq`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `teacherd`
--
ALTER TABLE `teacherd`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `tprequest`
--
ALTER TABLE `tprequest`
  MODIFY `TPid` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `trequest`
--
ALTER TABLE `trequest`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
