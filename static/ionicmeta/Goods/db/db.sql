CREATE TABLE IF NOT EXISTS `user` (
	`user_id`	integer,
	`first_name`	text NOT NULL,
	`last_name`	text NOT NULL,
	`email`	text NOT NULL UNIQUE,
	`phone`	text NOT NULL UNIQUE,
	PRIMARY KEY(`user_id`)
);
INSERT INTO `user` VALUES (1,'aish','s','aish@gmail.com','9839840932');
INSERT INTO `user` VALUES (2,'uma','p','uma@gmail.com','6983768632');
INSERT INTO `user` VALUES (3,'hari','p','hari@gmail.com','98653768632');
INSERT INTO `user` VALUES (12,'','','','');
CREATE TABLE IF NOT EXISTS `muser` (
	`muserid`	INTEGER NOT NULL,
	`first_name`	VARCHAR ( 60 ) NOT NULL,
	`last_name`	VARCHAR ( 60 ),
	`mobile_number`	BIGINT NOT NULL,
	`email_id`	VARCHAR ( 60 ) NOT NULL,
	`password`	VARCHAR ( 60 ) NOT NULL,
	`confirm_password`	VARCHAR ( 60 ) NOT NULL,
	`is_active`	BOOLEAN,
	CHECK(is_active IN(0,1)),
	PRIMARY KEY(`muserid`)
);
INSERT INTO `muser` VALUES (1,'arunpandiyan','r',9790431499,'arunr@gmail.com','password','password',1);
CREATE TABLE IF NOT EXISTS `mastermapdetail` (
	`mastermapdetailid`	INTEGER NOT NULL,
	`moduleid`	INTEGER NOT NULL,
	`sfname`	VARCHAR ( 60 ) NOT NULL,
	`tfname`	VARCHAR ( 60 ) NOT NULL,
	`shortid`	INTEGER,
	`project_slug`	VARCHAR ( 60 ) NOT NULL,
	PRIMARY KEY(`mastermapdetailid`),
	FOREIGN KEY(`moduleid`) REFERENCES `mastermap`(`moduleid`)
);
INSERT INTO `mastermapdetail` VALUES (1,1,'gstinid','contact_id','cid','Goods');
INSERT INTO `mastermapdetail` VALUES (2,1,'cmpny_name','first_name',NULL,'Goods');
INSERT INTO `mastermapdetail` VALUES (3,2,'kkkkkkkid','user_id','uid','Goods');
CREATE TABLE IF NOT EXISTS `mastermap` (
	`moduleid`	INTEGER NOT NULL,
	`stname`	VARCHAR ( 60 ) NOT NULL,
	`ttname`	VARCHAR ( 60 ) NOT NULL,
	`url`	VARCHAR ( 60 ),
	`dependson`	VARCHAR ( 60 ),
	`orderno`	INTEGER,
	`wherecon`	VARCHAR ( 60 ),
	`project_slug`	VARCHAR ( 60 ) NOT NULL,
	PRIMARY KEY(`moduleid`)
);
INSERT INTO `mastermap` VALUES (1,'gstin','contacts','/syncmaster',NULL,1,NULL,'Goods');
INSERT INTO `mastermap` VALUES (2,'kkkkkkk','user','/syncmaster',NULL,2,NULL,'Goods');
CREATE TABLE IF NOT EXISTS `control` (
	`controlid`	INTEGER NOT NULL,
	`key`	VARCHAR ( 60 ) NOT NULL,
	`value`	VARCHAR ( 60 ) NOT NULL,
	PRIMARY KEY(`controlid`)
);
INSERT INTO `control` VALUES (1,'state','Tamilnadu');
INSERT INTO `control` VALUES (2,'sync','false');
CREATE TABLE IF NOT EXISTS `contacts` (
	`contact_id`	integer,
	`first_name`	text NOT NULL,
	`last_name`	text NOT NULL,
	`email`	text NOT NULL UNIQUE,
	`phone`	text NOT NULL UNIQUE,
	PRIMARY KEY(`contact_id`)
);
INSERT INTO `contacts` VALUES (1,'zayn','p','zayn@gmail.com','652187');
INSERT INTO `contacts` VALUES (3,'harry','p','harry@gmail.com','98653768632');
INSERT INTO `contacts` VALUES (4,'grey','p','grey@gmail.com','677921');

