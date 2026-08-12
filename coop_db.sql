-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Mar 12, 2026 at 10:20 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `coop_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `companies`
--

CREATE TABLE `companies` (
  `id` int(11) NOT NULL,
  `ลำดับ` int(11) DEFAULT NULL,
  `ชื่อสถานประกอบการ` text DEFAULT NULL,
  `position` varchar(255) DEFAULT NULL,
  `major_required` varchar(255) DEFAULT NULL,
  `skills_required` text DEFAULT NULL,
  `interest_required` text DEFAULT NULL,
  `work_mode` varchar(100) DEFAULT NULL,
  `ที่อยู่` text DEFAULT NULL,
  `เบอร์ติดต่อ` text DEFAULT NULL,
  `e-mail(บริษัท/หน่วยงาน)` text DEFAULT NULL,
  `คุณสมบัติที่ต้องการ` longtext DEFAULT NULL,
  `จำนวนที่รับ` text DEFAULT NULL,
  `สวัสดิการ` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `companies`
--

INSERT INTO `companies` (`id`, `ลำดับ`, `ชื่อสถานประกอบการ`, `position`, `major_required`, `skills_required`, `interest_required`, `work_mode`, `ที่อยู่`, `เบอร์ติดต่อ`, `e-mail(บริษัท/หน่วยงาน)`, `คุณสมบัติที่ต้องการ`, `จำนวนที่รับ`, `สวัสดิการ`) VALUES
(1, 1, 'บริษัท จีเอเบิล จำกัด ', 'Programmer/Web Application/Software tester/UX,UI/Frontend developer/Backend developer ', 'software ', 'มีความสามารถด้านการเขียนโปรแกรม /\r\nมีความสามารถในการพัฒนา /\r\nการวิเคราะห์และออกแบบระบบ /การจัดการระบบฐานข้อมูล/เป็นผู้ทดสอบระบบ/ทักษะการสื่อสาร ', 'Programmer/Web Application/Software tester/UX,UI/Frontend developer/Backend developer ', 'Hybrid ', 'สำนักงานใหญ่ : เลขที่ 127/27, 29-31 ถนนนนทรี แขวงช่องนนทรี เขตยานนาวา กรุงเทพฯ 10120', 'Tel. 02-685-9000/\r\nFax. 02-681-0425', '-', '1. มีความสามารถด้านการเขียนโปรแกรม (เป็น Programmer)\r\n2. มีความสามารถในการพัฒนา Web Application)\r\n3. การวิเคราะห์และออกแบบระบบ / การจัดการระบบฐานข้อมูล\r\n4. Software tester (เป็นผู้ทดสอบระบบ)\r\n5. ทักษะการสื่อสาร และอื่นๆ ในการทำงานร่วมกันกับบุคลากรในหน่วยงาน', 'ไม่จำกัดจำนวน\n(ทำงานแบบ hybrid)', ' - ค่าตอบแทน'),
(2, 2, 'บริษัทเวสเทิร์น ดิจิตอล  จำกัด\r\n ', 'Database Management/ Web Application/Image processing ', 'software ', 'มีความสามารถด้าน Image processing/ \r\nมีความสามารถด้านการจัดการระบบฐานข้อมูล /\r\nมีความสามารถในการพัฒนา /\r\nต้องผ่านการสัมภาษณ์ด้วยภาษาอังกฤษกับบริษัท', 'Database Management/ Web Application/Image processing ', 'On-site', 'เลขที่ 140 หมู่2, ถนนอุมสรยุทธ, ตำบลคลองจิก อำเภอบางปะอิน จังหวัดพระนครศรีอยุธยา, 13170', 'Tel. 035-277-000\r\n', '', '1. มีความสามารถด้าน Image processing \r\n2. มีความสามารถด้านการจัดการระบบฐานข้อมูล (Database Management)\r\n3. มีความสามารถในการพัฒนา Web Application\r\n**ต้องผ่านการสัมภาษณ์ด้วยภาษาอังกฤษกับบริษัท\r\nลิงก์ติดตามประกาศรับสมัคร : https://www.facebook.com/wdthupdates', '3-4 คน', '- ค่าตอบแทน\r\n- ที่พัก\r\n- รถรับส่ง'),
(3, 3, 'บริษัท แอพพลิแคด จำกัด\r\n', 'Design Engineer/Draftsman/Draftsperson/Product Design/ 3D Designer /\r\n3D Modeler/', 'Robot ', 'มีความรู้ความเข้าใจในการออกแบบและเขียนแบบ 3 มิติด้วยโปรแกรม SolidWork\r\n/มีความสามารถในการพัฒนา Application (C#) เพื่อสร้าง Plug-In ให้กับโปรแกรม SolidWork', 'DesignEngineer/Draftsman/Draftsperson/Product Design/ 3D Designer /\r\n3D Modeler/', 'On-site ', 'เลขที่ 69 ซอยสุขุมวิท 68 ถนนสุขุมวิท แขวงบางนาเหนือ เขตบางนา กรุงเทพฯ\r\n10260.', '095-365-6863', '', '1. มีความรู้ความเข้าใจในการออกแบบและเขียนแบบ 3 มิติด้วยโปรแกรม SolidWork\n2. มีความสามารถในการพัฒนา Application (C#) เพื่อสร้าง Plug-In ให้กับโปรแกรม SolidWork', '2 คน', 'มีค่าตอบแทน'),
(4, 4, 'เกษตรและสหกรณ์จังหวัดพิษณุโลก', 'UX,UI/ Backend Developer/ PHP /MAP API ', 'Software ', 'การออกแบบและวิเคราะห์ระบบ /\r\nการจัดการฐานข้อมูลด้วย SQL /\r\nการพัฒนา Web Applicartion ด้วย PHP /\r\nการใช้ MAP API เพื่อพัฒนา Web Application/\r\nทักษะอื่นๆ ในการทำงานร่วมกันกับบุคลากรในหน่วยงาน', 'UX,UI/ Backend Developer/ PHP /MAP API ', 'On-site ', ' \n 	\nชั้น 5 อาคารใหม่ศาลากลางจังหวัดพิษณุโลก ถนนวังจันทน์ ตำบลในเมือง อำเภอเมือง จังหวัดพิษณุโลก 65000', 'Tel.02-3010800', '', '1. การออกแบบและวิเคราะห์ระบบ\n2. การจัดการฐานข้อมูลด้วย SQL \n3. การพัฒนา Web Applicartion ด้วย PHP \n4. การใช้ MAP API เพื่อพัฒนา Web Application\n5. ทักษะอื่นๆ ในการทำงานร่วมกันกับบุคลากรในหน่วยงาน', '2-3 คน', ''),
(5, 5, 'บริษัทไทยแอร์โรว์ จำกัด', 'IoT Developer/ PLC Programmer/Instrumentation /Full Stack Developer / System Analyst/Web Application/Database Administrator', 'Robot /Software ', 'ระบบไฟฟ้าเบื้องต้น ที่ทำงานร่วมกับระบบอัตโนมัติ และ PLC/\r\nการใช้งานอุปกรณ์ Input,Output ของระบบอัตโนมัติ /\r\nระบบสมองกลฝังตัว เเละ IoT/ มีความสามารถด้านการเขียนโปรแกรม\r\n/มีความสามารถในการพัฒนา การวิเคราะห์และออกแบบระบบ / การจัดการระบบฐานข้อมูล', 'IoT Developer/ PLC Programmer/Instrumentation /Full Stack Developer / System Analyst/Web Application/Database Administrator', 'On-Site', 'หมู่ 7 ตำบลหัวรอ อำเมือง จังหวัดพิษณุโลก รหัสไปรษณีย์ 65000', 'Tel. 055-245245/\r\nTel. 098-785549\r\n', '', ' \n 	\nแผนก IT\n1. มีความสามารถด้านการเขียนโปรแกรม\n2. มีความสามารถในการพัฒนา Web Application\n3. การวิเคราะห์และออกแบบระบบ / การจัดการระบบฐานข้อมูล                             แผนก Innovation R&D \n1. ระบบไฟฟ้าเบื้องต้น ที่ทำงานร่วมกับระบบอัตโนมัติ และ PLC\n2. การใช้งานอุปกรณ์ Input / Output ของระบบอัตโนมัติ\n3. ระบบสมองกลฝังตัว (Embedded Systems) และ IoT', 'แผนกละ 1 คน', ''),
(6, 6, 'บริษัท Omron Electronic \r\n', 'Automation/Control Engineer /PLC Technician Engineer/Robot Programmer', 'Robot ', 'ระบบไฟฟ้าเบื้องต้น ที่ทำงานร่วมกับระบบอัตโนมัติและ PLC/\r\nการเขียนโปรแกรมเพื่อรับส่งข้อมูลผ่านการสื่อสารอุตสาหกรรม/\r\nหุ่นยนต์อุตสาหกรรม และ PLC /\r\nทักษะอื่นๆ ในการทำงานร่วมกันกับบุคลากรในหน่วยงาน', 'Automation/Control Engineer /PLC Technician Engineer/Robot Programmer', 'On-Site', 'อาคารรสาทาวเวอร์ 2 ชั้น 16 เลขที่ 555 ถนน ถ.พหลโยธิน ตำบล/แขวง จตุจักร อำเภอ/เขต จตุจักร จังหวัด กรุงเทพฯ รหัสไปรษณีย์ 10900', 'Tel. 02-9370123', '', '1. ระบบไฟฟ้าเบื้องต้น ที่ทำงานร่วมกับระบบอัตโนมัติและ PLC\n2. การเขียนโปรแกรมเพื่อรับส่งข้อมูลผ่านการสื่อสารอุตสาหกรรม\n3. หุ่นยนต์อุตสาหกรรม และ PLC\n4. ทักษะอื่นๆ ในการทำงานร่วมกันกับบุคลากรในหน่วยงาน', '2 คน', 'มีค่าตอบแทน'),
(7, 7, 'บริษัท เอส.เอ็ม.ซี.(ประเทศไทย) จำกัด', 'Automation/System Engineer/IoT/Software Developer/Software tester/ Digital Transformation', 'Robot', '1. ระบบอัตโนมัติ / หุ่นยนต์อุตสาหกรรม\r\n2. มีความสามารถด้าน IoT\r\n3. Software Developer (งานด้านจัดทำและปรับปรุงเว็บไซต์)\r\n4. Software tester \r\n5. มีทักษะการพัฒนาระบบ หรือมีทักษะการใช้ซอฟต์แวร์ เพื่อการทำ Paperless Checksheet\r\n6. มีวินัย มีความรับผิดชอบ สามารถทำงานร่วมกับผู้อื่นได้ดี\r\n7. ขยันเรียนรู้ กระตือรือร้น', 'Automation/System Engineer/IoT/Software Developer/Software tester/ Digital Transformation', 'On-Site', '267/211 ซอยเมืองใหม่มาบตาพุด ถนนสุขุมวิท อำเภอเมืองระยอง จังหวัดระยอง 21150', ' \r\n 	\r\nโทร. 0-3860-8331-2/\r\nแฟกซ์. 0-3860-8330', '', '1. ระบบอัตโนมัติ / หุ่นยนต์อุตสาหกรรม\n2. มีความสามารถด้าน IoT\n3. Software Developer (งานด้านจัดทำและปรับปรุงเว็บไซต์)\n4. Software tester \n5. มีทักษะการพัฒนาระบบ หรือมีทักษะการใช้ซอฟต์แวร์ เพื่อการทำ Paperless Checksheet\n6. มีวินัย มีความรับผิดชอบ สามารถทำงานร่วมกับผู้อื่นได้ดี\n7. ขยันเรียนรู้ กระตือรือร้น', '2 คน', 'มีค่าตอบแทนและที่พัก'),
(8, 8, 'โครงการส่งน้ำและบำรุงรักษายมน่าน', 'Embedded systems Engineer /Embedded Software Developer /IoT Engineer / IoT Developer', 'Robot ', 'ระบบสมองกลฝังตัว /\r\nมีความสามารถด้าน IoT/\r\nทักษะอื่นๆ ในการทำงานร่วมกันกับบุคลากรในหน่วยงา', 'Embedded systems Engineer /Embedded Software Developer /IoT Engineer / IoT Developer', 'On-Site', 'เลขที่ 8 หมู่ 8 ตำบลท่าทอง อำเภอเมืองพิษณุโลก จังหวัดพิษณุโลก 65000', 'โทรหน่วยงาน : 055 983589', '', '1. ระบบสมองกลฝังตัว (Embedded systems)\n2. มีความสามารถด้าน IoT\n3. ทักษะอื่นๆ ในการทำงานร่วมกันกับบุคลากรในหน่วยงาน', '2 คน', ''),
(9, 9, 'คณบดีคณะแพทยศาสตร์ มหาวิทยาลัยนเรศวร', 'AI Developer/Machine Learning Engineer/Full Stack Developer /Backend Developer', 'Software ', 'มีความสามารถในการพัฒนา Web,Mobile Application ที่เชื่อมต่อกับ API/\r\nมีความเข้าใจในการโปแกรมภาษา Python และการสร้างโมเดล AI/\r\nสามารถเรียนรู้แนวทางการนำโมเดล AI มาทำงานร่วมกันกับ Web Service', 'AI Developer/Machine Learning Engineer/Full Stack Developer ', 'On-Site', '\"งานบริหารเทคโนโลยีสารสนเทศ คณะแพทยศาสตร์ มหาวิทยาลัยนเรศวร  \nอำเภอเมืองฯ จังหวัดพิษณุโลก 65000\"', '', '', ' \n 	\n1. มีความสามารถในการพัฒนา Web/Mobile Application ที่เชื่อมต่อกับ API\n2. มีความเข้าใจในการโปแกรมภาษา Python และการสร้างโมเดล AI\n3. สามารถเรียนรู้แนวทางการนำโมเดล AI มาทำงานร่วมกันกับ Web Service', '3 คน', ''),
(10, 10, 'องค์การบริหารส่วนจังหวัดพิษณุโลก', 'Software Developer/Cybersecurity Analyst/information Security Officer / Security Engineer', 'Cyber', 'พัฒนาซอฟต์แวร์ เว็บไซต์ ระบบสารสนเทศ /\r\nความปลอดภัยไซเบอร์ ด้านเครือข่าย เว็บไซต์ /\r\nความปลอดภัยข้อมูล', 'Software Developer/Cybersecurity Analyst/information Security Officer / Security Engineer', 'On-Site', ' \n 	\nเลขที่ 206 หมู่ 4 ถนน พิษณุโลก – วังทอง ตำบลสมอแข อำเภอเมืองพิษณุโลก จังหวัดพิษณุโลก 65000', '', '', ' \n 	\n1. พัฒนาซอฟต์แวร์ เว็บไซต์ ระบบสารสนเทศ\n2. ความปลอดภัยไซเบอร์ ด้านเครือข่าย เว็บไซต์ \n3. ความปลอดภัยข้อมูล', '4 คน ', ''),
(11, 11, 'ศูนย์ประสานการรักษาความมั่นคงปลอดภัยระบบคอมพิวเตอร์แห่งชาติ\r\nสำนักบริหารโครงสร้างพื้นฐานสำคัญสารสนเทศ CII', 'Cybersecurity Analyst/Incident Response Analyst', 'Cyber', 'พื้นฐานความปลอดภัยไซเบอร์/\r\nการตอบสนองและรับมือภัยคุกคาม/\r\nความอดทน สามารถเรียนรู้ด้วยตนเองได้ ', 'Cybersecurity Analyst/Incident Response Analyst', 'On-Site', '120 หมู่ 3 อาคารรัฐประศาสนภักดี (อาคารซี)\nชั้น 7 ศูนย์ราชการเฉลิมพระเกียรติ 80 พรรษา 5 ธันวาคม 2550 ถนนแจ้งวัฒนะ แขวงทุ่งสองห้อง เขตหลักสี่ กรุงเทพฯ 10210', '', '', '1. พื้นฐานความปลอดภัยไซเบอร์\n2. การตอบสนองและรับมือภัยคุกคาม\n3. ความอดทน สามารถเรียนรู้ด้วยตนเองได้ ', '3 คน', ''),
(12, 12, ' \n 	\nบริษัท ไอบอทน้อย จำกัด', 'AI Researcher /\r\nData Analysts/\r\nFront-end Developer/\r\nBack-end Developer/\r\nSystem Developer/\r\nUX,UI Designer/\r\n3D developer', 'Software ', '1. AI Resercher ด้าน NLP, Text to Speech,Computer Vision: Python, Colab/VS code, Machine Learning, PyTorch, Tenserflow, OOP, Video Processing, Data Preprocessing\r\n2. Data Analysts/Scientist: Python, Statistic, Colab, Machine Learning\r\n3. Front-end Developer: HTML, CSS, JavaScript, TypeScript, Angular, Vuejs\r\n4. Back-end Developer: Python, Golang\r\n5. System Developer: Linux, Docker, Python\r\n6. UX/UI Designer: Sketch, Figma, Adobe XD, วิเคราะห์ความต้องการของuser, ออกแบบแนวทางแก้ปัญหา, ทดสอบใช้งานและวิเคราะห์ข้อมูล, ชอบออกแบบอะไรใหม่ๆ ศึกษาdesignใหม่ๆ, การสื่อสารกับทีม, degrative AI design\r\n7. 3D developer: Modeling Sculpt, UV map & Texture, Animation, Render, C#, Python, Unity Engine', 'AI Researcher /\r\nData Analysts/\r\nFront-end Developer/\r\nBack-end Developer/\r\nSystem Developer/\r\nUX,UI Designer/\r\n3D developer', 'Hybrid', '30 หมู่บ้านเศรษฐสิริ ราชพฤกษ์จรัญฯ ซอยปากน้ำฝั่งเหนือ 11 แขวงคลองชักพระ เขตตลิ่งชัน กรุงเทพฯ 10170', '', '', '1. AI Resercher ด้าน NLP, Text to Speech,Computer Vision: Python, Colab/VS code, Machine Learning, PyTorch, Tenserflow, OOP, Video Processing, Data Preprocessing\n2. Data Analysts/Scientist: Python, Statistic, Colab, Machine Learning\n3. Front-end Developer: HTML, CSS, JavaScript, TypeScript, Angular, Vuejs\n4. Back-end Developer: Python, Golang\n5. System Developer: Linux, Docker, Python\n6. UX/UI Designer: Sketch, Figma, Adobe XD, วิเคราะห์ความต้องการของuser, ออกแบบแนวทางแก้ปัญหา, ทดสอบใช้งานและวิเคราะห์ข้อมูล, ชอบออกแบบอะไรใหม่ๆ ศึกษาdesignใหม่ๆ, การสื่อสารกับทีม, gerative AI design\n7. 3D developer: Modeling&Sculpt, UV map & Texture, Animation, Render, C#, Python, Unity Engine', 'ไม่จำกัดจำนวน\n(ทำงานแบบ hybrid)', ''),
(13, 13, ' \n 	\nโรงพยาบาลบึงสามัคคี', 'System Analyst/Backend Developer', 'Software ', ' \r\n 	\r\nพัฒนาระบบสารสนเทศให้กับโรงพยาบาล', 'System Analyst/Backend Developer', 'On-Site', ' \n 	\n200 หมู่7 ตำบลระหาน อำเภอบึงสามัคคี จังหวัดกำแพงเพชร 62210', '', '', 'พัฒนาระบบสารสนเทศให้กับโรงพยาบาล', '2 คน', ''),
(14, 14, 'บริษัทมงคลสมัย จำกัด', 'Automation Engineer/PLC Programmer/ Robotics Engineer/ PLC Engineer', 'Robot', 'ระบบไฟฟ้าเบื้องต้น ที่ทำงานร่วมกับระบบอัตโนมัติและ PLC/\r\nการเขียนโปรแกรมเพื่อรับส่งข้อมูลผ่านการสื่อสารอุตสาหกรรม\r\n/หุ่นยนต์อุตสาหกรรม และ PLC\r\n/ทักษะอื่นๆ ในการทำงานร่วมกันกับบุคลากรในหน่วยงาน', 'Automation Engineer/PLC Programmer/ Robotics Engineer/ PLC Engineer', 'On-Site', ' \n 	\n149 หมู่ 5 ตำบลผาจุก อำเภอเมืองอุตรดิตถ์ จังหวัดอุตรดิตถ์ 53000', '', '', '1. ระบบไฟฟ้าเบื้องต้น ที่ทำงานร่วมกับระบบอัตโนมัติและ PLC\r\n2. การเขียนโปรแกรมเพื่อรับส่งข้อมูลผ่านการสื่อสารอุตสาหกรรม\r\n3. หุ่นยนต์อุตสาหกรรม และ PLC\r\n4. ทักษะอื่นๆ ในการทำงานร่วมกันกับบุคลากรในหน่วยงาน', '2 คน', ''),
(15, 15, 'บริษัท น้ำตาลพิษณุโลก จำกัด\r\n', 'Full Stack Developer/Mechatronics Software Engineer/Automation Software Engineer/Web Dashboard', 'Software /Robot', 'มีทักษะด้านการเขียนโปรแกรม/\r\nมีความสามารถในการพัฒนา Web Application /\r\nการจัดการฐานข้อมูล/ ฝ่ายวิศวกรรม (ระบบอัตโนมัติ)\r\n', 'Full Stack Developer/Mechatronics Software Engineer/Automation Software Engineer/Web Dashboard', 'On-Site', 'เลขที่ 8/8 หมู่ 8 ถนนสันติบันเทิง-บางกระทุ่ม \n(กม.14) ตำบลไผ่ล้อม อำเภอบางกระทุ่ม จังหวัดพิษณุโลก', '082-938-4567', '', 'ฝ่ายพัฒนาซอฟต์แวร์\n - มีทักษะด้านการเขียนโปรแกรม\n - มีความสามารถในการพัฒนา Web Application \n - การจัดการฐานข้อมูล            ฝ่่ายวิศวกรรม (ระบบอัตโนมัติ)\n - (รอข้อมูลความต้องการจากหน่วยงาน)', 'ฝ่ายละ 2 คน', 'ค่าตอบแทน'),
(16, 16, 'บริษัท หัวเว่ย เทคโนโลยี (ประเทศไทย) จํากัด', 'Engineering /Network Engineer/ Sales Engineer/ Green Energy Engineer/ Solution Engineer/ HR Assistant/Recruitment/ Marketing Assistant/ Project Coordinator/Supply Chain Specialist/ Admin ', 'Software ', 'ตำแหน่งที่เปิดรับ (Internship Positions)\r\nEngineering: Network Engineer, Sales Engineer, Green Energy Engineer, Solution Engineer และอื่นๆ\r\nNon-Engineering: HR Assistant/Recruitment, Marketing Assistant, Project Coordinator, Supply Chain Specialist, Admin \r\nคุณสมบัติผู้สมัคร (Qualifications)\r\nนักศึกษาปริญญาตรีปีที่ 3-4 หรือ ปริญญาโท\r\nGPA 3.00 ขึ้นไป (บางรอบพิจารณาเป็นพิเศษ)\r\nมีความสามารถในการสื่อสารภาษาอังกฤษดีเยี่ยม (หากได้ภาษาจีนจะพิจารณาเป็นพิเศษ)\r\nมีความรู้พื้นฐานเกี่ยวกับ ICT, เทคโนโลยี, หรือสาขาที่เกี่ยวข้อง\r\nมีทักษะการทำงานเป็นทีม การสื่อสาร และกระตือรือร้นเรียนรู้ \r\n 	\r\n', 'Engineering /Network Engineer/ Sales Engineer/ Green Energy Engineer/ Solution Engineer/ HR Assistant/Recruitment/ Marketing Assistant/ Project Coordinator/Supply Chain Specialist/ Admin ', NULL, 'เลขที่ 9 อาคารจี ทาวเวอร์แกรนด์ พระราม9 ชั้น 34-39 ถนนพระราม 9 แขวงห้วยขวาง เขตห้วยขวาง กรุงเทพมหานคร 10310\n\nemail : \nrecruitment.thailand@huawei.com\n\nhttps://www.facebook.com/HuaweiCareerTH/?locale=th_TH', '02 095 8199', '', ' ตำแหน่งที่เปิดรับ (Internship Positions)\nEngineering: Network Engineer, Sales Engineer, Green Energy Engineer, Solution Engineer และอื่นๆ\nNon-Engineering: HR Assistant/Recruitment, Marketing Assistant, Project Coordinator, Supply Chain Specialist, Admin \nคุณสมบัติผู้สมัคร (Qualifications)\nนักศึกษาปริญญาตรีปีที่ 3-4 หรือ ปริญญาโท\nGPA 3.00 ขึ้นไป (บางรอบพิจารณาเป็นพิเศษ)\nมีความสามารถในการสื่อสารภาษาอังกฤษดีเยี่ยม (หากได้ภาษาจีนจะพิจารณาเป็นพิเศษ)\nมีความรู้พื้นฐานเกี่ยวกับ ICT, เทคโนโลยี, หรือสาขาที่เกี่ยวข้อง\nมีทักษะการทำงานเป็นทีม การสื่อสาร และกระตือรือร้นเรียนรู้ \n 	\nเอกสารการสมัคร\n1. Resume (English Ver.)\n2. Academic Transcript', 'กี่คนก็ได้ \nหากสอบผ่าน', '500/วัน'),
(17, 17, 'ศูนย์เทคโนโลยีอิเล็กทรอนิกส์และคอมพิวเตอร์แห่งชาติ\r\n', NULL, NULL, NULL, NULL, NULL, 'เลขที่ 112 อุทยานวิทยาศาสตร์ประเทศไทย ถนนพหลโยธิน ตำบลคลองหนึ่ง\nอำเภอคลองหลวง จังหวัดปทุมธานี 12120', '02-564-6900', 'Pattraphon.som@ncr.nstda.or.th', '', '', ''),
(18, 18, 'Drone Academy Thailand \n(เรียน : คุณธีญญารัตน์ ศุภสีห์ (ฝ่ายบริหารจัดการทรัพยากรบุคคล)', NULL, NULL, NULL, NULL, NULL, '58/64 ต.คลองเหนือ อ.ปากเกร็ด นนทบุรี', '093-669939', 'info@droneth.or.th\ndroneacademythailand@gmail.com', '', '', ''),
(19, 19, ' \n 	\nบริษัท เบลตัน อินดัสเตรียล (ประเทศไทย)', NULL, NULL, NULL, NULL, NULL, ' \n 	\nตำบล บ้านช้าง อำเภออุทัย จังหวัดพระนครศรีอยุธยา 13210', '0-2529-7300 ต่อ 2222', 'thanaporn.s@beltontechnology.com', '', '', ''),
(20, 20, 'บริษัท นำชัย แคร์ จำกัด', NULL, NULL, NULL, NULL, NULL, '353/46 หมู่ 9 ตำบลหนองปรือ อำเภอบางละมุง จังหวัดชลบุรี รหัสไปรษณีย์ 20150', '0-21148289', 'allservice@numchaicare.co.th', '', '', ''),
(21, 21, 'บริษัท ออโต ไดแด็กติก จำกัด', NULL, NULL, NULL, NULL, NULL, '111 ซอยสุขุมวิท 62/1 ถนนสุขุมวิท แขวงพระโขนงใต้ เขตพระโขนง กรุงเทพฯ 10260', '', '', '', '', ''),
(22, 22, 'บริษัท Seagate Technology ', NULL, NULL, NULL, NULL, NULL, '99/225, อำเภอสูงเนิน นครราชสีมา 30170', '044 497 000', 'seagate.com', '', '', ''),
(23, 23, 'บริษัทเด็นโซ่ประเทศไทย ', NULL, NULL, 'Software/Robot', 'Digital Transformation Engineer/IoT Engineer/AI Machine Learning Engineer/Data Analyst/Digital Transformation Intern', NULL, '888 หมู่ 1 ถ.บางนา-ตราด กม. 27.5 ต.บางบ่อ อ.บางบ่อ, 10560\r\n📌สาขาสำโรง (ใกล้ BTS สำโรง / สายสีเหลืองสถานีทิพวัล)\r\n📌สาขาเวลโกรว์ นิคมอุตสาหกรรมเวลโกรว์ จ.ฉะเชิงเทรา\r\n📌สาขาบางปะกง นิคมอุตสาหกรรมอมตะซิตี้ชลบุรี จ.ชลบุรี\r\n📌สาขาระยอง\r\n \r\n \r\n ', '02 315 9500', NULL, NULL, NULL, '500/วัน');

-- --------------------------------------------------------

--
-- Table structure for table `documents`
--

CREATE TABLE `documents` (
  `id` int(11) NOT NULL,
  `student_name` varchar(100) DEFAULT NULL,
  `file_name` varchar(255) DEFAULT NULL,
  `status` varchar(50) DEFAULT 'รอตรวจ',
  `comment` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `documents`
--

INSERT INTO `documents` (`id`, `student_name`, `file_name`, `status`, `comment`) VALUES
(1, 'student1', 'student1_coop.pdf', 'ไม่ผ่าน', 'ผิดทุกไฟล์'),
(2, 'student1', 'student1_transcript.pdf', 'ไม่ผ่าน', 'ผิดทุกไฟล์'),
(3, 'student1', 'student1_studentcard.pdf', 'ไม่ผ่าน', 'ผิดทุกไฟล์'),
(4, 'student1', 'student1_idcard.pdf', 'ไม่ผ่าน', 'ผิดทุกไฟล์'),
(5, 'student1', 'student1_house.pdf', 'ไม่ผ่าน', 'ผิดทุกไฟล์'),
(6, 'student1', 'student1_cv.pdf', 'ไม่ผ่าน', 'ผิดทุกไฟล์'),
(7, '6612247030', '6612247030_coop.pdf', 'ผ่าน', ''),
(8, '6612247043', '6612247043_coop.pdf', 'ผ่าน', NULL),
(10, '6612247030', '6612247030_transcript.pdf', 'ผ่าน', ''),
(11, '6612247030', '6612247030_studentcard.pdf', 'ผ่าน', ''),
(12, '6612247030', '6612247030_idcard.pdf', 'ผ่าน', ''),
(13, '6612247030', '6612247030_house.pdf', 'ผ่าน', ''),
(14, '6612247030', '6612247030_cv.pdf', 'ผ่าน', ''),
(15, '6612247036', '6612247036_coop.pdf', 'ผ่าน', ''),
(16, '6612247036', '6612247036_transcript.pdf', 'ผ่าน', ''),
(17, '6612247036', '6612247036_studentcard.pdf', 'ผ่าน', ''),
(18, '6612247036', '6612247036_idcard.pdf', 'ผ่าน', ''),
(19, '6612247036', '6612247036_house.pdf', 'ผ่าน', ''),
(20, '6612247036', '6612247036_cv.pdf', 'ผ่าน', ''),
(21, '6612247052', '6612247052_coop.pdf', 'รอตรวจ', NULL),
(22, '6612247052', '6612247052_transcript.pdf', 'รอตรวจ', NULL),
(23, '6612247052', '6612247052_studentcard.pdf', 'รอตรวจ', NULL),
(24, '6612247052', '6612247052_idcard.pdf', 'รอตรวจ', NULL),
(25, '6612247052', '6612247052_house.pdf', 'รอตรวจ', NULL),
(26, '6612247052', '6612247052_cv.pdf', 'รอตรวจ', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `match_result`
--

CREATE TABLE `match_result` (
  `id` int(11) NOT NULL,
  `student_id` varchar(20) DEFAULT NULL,
  `company_name` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `match_result`
--

INSERT INTO `match_result` (`id`, `student_id`, `company_name`) VALUES
(1, '6612247043', 'บริษัทเวสเทิร์น ดิจิตอล  จำกัด\r\n '),
(2, 'วริศรา หอมรื่น', ' \n 	\nบริษัท ไอบอทน้อย จำกัด'),
(3, 'วริศรา หอมรื่น', ' \n 	\nบริษัท ไอบอทน้อย จำกัด'),
(4, 'ทัศนพร ตาทิพย์', 'บริษัทเวสเทิร์น ดิจิตอล  จำกัด\r\n '),
(5, 'กรวิภา ผลปาน', 'บริษัทเวสเทิร์น ดิจิตอล  จำกัด\r\n '),
(6, 'จิลราวุธ อริยวงศ์', 'บริษัทเวสเทิร์น ดิจิตอล  จำกัด\r\n '),
(7, 'จิลราวุธ อริยวงศ์', 'บริษัทเวสเทิร์น ดิจิตอล  จำกัด\r\n '),
(8, 'จิลราวุธ อริยวงศ์', 'บริษัทเวสเทิร์น ดิจิตอล  จำกัด\r\n '),
(9, 'จิลราวุธ อริยวงศ์', 'บริษัทเวสเทิร์น ดิจิตอล  จำกัด\r\n '),
(10, 'จิลราวุธ อริยวงศ์', 'บริษัทเวสเทิร์น ดิจิตอล  จำกัด\r\n '),
(11, 'ประกายมาศ ศิลาอ่อน', ' \n 	\nบริษัท ไอบอทน้อย จำกัด'),
(12, 'ศักดิ์ชัย เทียมเนียม', 'บริษัทเวสเทิร์น ดิจิตอล  จำกัด\r\n '),
(13, '6612247052', ''),
(14, '6612247052', ''),
(15, 'ศักดิ์ชัย เทียมเนียม', 'บริษัทเวสเทิร์น ดิจิตอล  จำกัด\r\n '),
(16, '6612247052', ''),
(17, 'ศักดิ์ชัย เทียมเนียม', 'บริษัทเวสเทิร์น ดิจิตอล  จำกัด\r\n ');

-- --------------------------------------------------------

--
-- Table structure for table `reports`
--

CREATE TABLE `reports` (
  `id` int(11) NOT NULL,
  `student_username` varchar(50) DEFAULT NULL,
  `title` varchar(255) DEFAULT NULL,
  `detail` text DEFAULT NULL,
  `file_name` varchar(255) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `students`
--

CREATE TABLE `students` (
  `id` int(11) NOT NULL,
  `student_id` varchar(20) DEFAULT NULL,
  `fullname` varchar(100) DEFAULT NULL,
  `major` varchar(100) DEFAULT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `project` varchar(255) DEFAULT NULL,
  `gpa` varchar(10) DEFAULT NULL,
  `career_interest` varchar(255) DEFAULT NULL,
  `skills` varchar(255) DEFAULT NULL,
  `work_mode` varchar(50) DEFAULT NULL,
  `matchcompany` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `students`
--

INSERT INTO `students` (`id`, `student_id`, `fullname`, `major`, `phone`, `project`, `gpa`, `career_interest`, `skills`, `work_mode`, `matchcompany`) VALUES
(34, '6612247030', 'กรวิภา ผลปาน', 'Software Engineering', NULL, NULL, '3.54', 'backend ', 'python', 'On-site', ''),
(41, '6612247043', 'จิลราวุธ อริยวงศ์', 'Software Engineering', NULL, NULL, '3.10', 'ux ui froned', 'php python', 'On-site', ''),
(44, '6612247036', 'ประกายมาศ ศิลาอ่อน', 'Cyber Security', NULL, NULL, '3.45', 'hacker', 'python', 'Hybrid', ''),
(45, '6612247052', 'ศักดิ์ชัย เทียมเนียม', 'Software Engineering', NULL, NULL, '3.00', 'backend ', 'php python', 'On-site', ''),
(46, '6612247052', 'ศักดิ์ชัย เทียมเนียม', 'Robotics Engineering', NULL, NULL, '3.00', 'PLC', 'Solid work', 'On-site', ''),
(47, '6612247052', 'ศักดิ์ชัย เทียมเนียม', 'Robotics Engineering', NULL, NULL, '3.00', 'PLC', 'Solid work', 'On-site', ''),
(48, '6612247052', 'ศักดิ์ชัย เทียมเนียม', 'Robotics Engineering', NULL, NULL, '3.00', 'PLC', 'Solid work', 'On-site', '');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `role` enum('student','teacher','admin') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `username`, `password`, `role`) VALUES
(0, '6612247043', '63839561365b0389e5c20f2be77ae0e4', 'student'),
(1, 'student1', '81dc9bdb52d04dc20036dbd8313ed055', 'student'),
(2, 'teacher1', '81dc9bdb52d04dc20036dbd8313ed055', 'teacher'),
(3, 'admin1', '81dc9bdb52d04dc20036dbd8313ed055', 'admin'),
(4, '6612247030', '39d474230399abbd96fdb491a95e51e4', 'student'),
(6, '6612247038', '81dc9bdb52d04dc20036dbd8313ed055', 'student'),
(7, '6612247034', '81dc9bdb52d04dc20036dbd8313ed055', 'student'),
(8, '6612247036', '674f3c2c1a8a6f90461e8a66fb5550ba', 'student'),
(10, '6612247052', '86a1fa88adb5c33bd7a68ac2f9f3f96b', 'student');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `companies`
--
ALTER TABLE `companies`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `documents`
--
ALTER TABLE `documents`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `match_result`
--
ALTER TABLE `match_result`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `reports`
--
ALTER TABLE `reports`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `students`
--
ALTER TABLE `students`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `companies`
--
ALTER TABLE `companies`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=25;

--
-- AUTO_INCREMENT for table `documents`
--
ALTER TABLE `documents`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=27;

--
-- AUTO_INCREMENT for table `match_result`
--
ALTER TABLE `match_result`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;

--
-- AUTO_INCREMENT for table `reports`
--
ALTER TABLE `reports`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `students`
--
ALTER TABLE `students`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=49;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
