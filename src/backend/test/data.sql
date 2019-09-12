/*
 Navicat Premium Data Transfer

 Source Server         : sqlite-dev
 Source Server Type    : SQLite
 Source Server Version : 3017000
 Source Schema         : main

 Target Server Type    : SQLite
 Target Server Version : 3017000
 File Encoding         : 65001

 Date: 11/09/2019 15:16:47
*/

PRAGMA foreign_keys = false;

-- ----------------------------
-- Table structure for permission
-- ----------------------------
DROP TABLE IF EXISTS "permission";
CREATE TABLE "permission" (
  "id" INTEGER NOT NULL,
  "path" VARCHAR(200) NOT NULL,
  "name" VARCHAR(20) NOT NULL,
  "desc" VARCHAR(50),
  "create_time" DATETIME,
  "update_time" DATETIME,
  PRIMARY KEY ("id")
);

-- ----------------------------
-- Records of permission
-- ----------------------------
INSERT INTO "permission" VALUES (1, 'user_get_user', '获取用户信息', NULL, '2019-09-10 14:02:43', '2019-09-10 14:02:43');
INSERT INTO "permission" VALUES (2, 'user_update_user', '更新用户信息', NULL, '2019-09-10 14:02:43', '2019-09-10 14:02:43');
INSERT INTO "permission" VALUES (3, 'user_update_password', '修改密码', NULL, '2019-09-10 14:02:43', '2019-09-10 14:02:43');
INSERT INTO "permission" VALUES (4, 'user_get_users', '获取所有用户', NULL, '2019-09-10 14:02:43', '2019-09-10 14:02:43');
INSERT INTO "permission" VALUES (5, 'device_add_device', '添加设备', NULL, '2019-09-10 14:02:43', '2019-09-10 14:02:43');

-- ----------------------------
-- Table structure for role
-- ----------------------------
DROP TABLE IF EXISTS "role";
CREATE TABLE "role" (
  "id" INTEGER NOT NULL,
  "name" VARCHAR(20) NOT NULL,
  "desc" VARCHAR(50),
  "create_time" DATETIME,
  "update_time" DATETIME,
  PRIMARY KEY ("id")
);

-- ----------------------------
-- Records of role
-- ----------------------------
INSERT INTO "role" VALUES (1, 'admin', '管理员', '2019-09-10 14:02:43', '2019-09-10 14:02:43');
INSERT INTO "role" VALUES (2, 'normal', '普通用户', '2019-09-10 14:02:43', '2019-09-10 14:02:43');

-- ----------------------------
-- Table structure for role_permission
-- ----------------------------
DROP TABLE IF EXISTS "role_permission";
CREATE TABLE "role_permission" (
  "role_id" INTEGER NOT NULL,
  "permission_id" INTEGER NOT NULL,
  PRIMARY KEY ("role_id", "permission_id"),
  FOREIGN KEY ("permission_id") REFERENCES "permission" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION,
  FOREIGN KEY ("role_id") REFERENCES "role" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION
);

-- ----------------------------
-- Records of role_permission
-- ----------------------------
INSERT INTO "role_permission" VALUES (2, 1);
INSERT INTO "role_permission" VALUES (2, 2);
INSERT INTO "role_permission" VALUES (2, 3);
INSERT INTO "role_permission" VALUES (2, 4);
INSERT INTO "role_permission" VALUES (2, 5);

-- ----------------------------
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS "user";
CREATE TABLE "user" (
  "id" INTEGER NOT NULL,
  "username" VARCHAR(32) NOT NULL,
  "password" VARCHAR(128) NOT NULL,
  "realname" VARCHAR(32) NOT NULL,
  "email" VARCHAR(40) NOT NULL,
  "status" INTEGER,
  "create_time" DATETIME,
  "update_time" DATETIME,
  PRIMARY KEY ("id")
);

-- ----------------------------
-- Records of user
-- ----------------------------
INSERT INTO "user" VALUES (1, 'admin', 'admin', '超级管理员', 'admin@admin.com', 1, '2019-09-10 14:02:43', '2019-09-10 14:02:43');
INSERT INTO "user" VALUES (2, 'test1', 'test1', 'test1', 'test1@test1.com', 1, '2019-09-10 14:02:43', '2019-09-10 14:02:43');
INSERT INTO "user" VALUES (3, 'test2', 'test2', 'test2', 'test2@test2.com', 1, '2019-09-10 14:02:43', '2019-09-10 14:02:43');
INSERT INTO "user" VALUES (4, 'test3', 'test3', 'test3', 'test3@test3.com', 1, '2019-09-10 14:02:43', '2019-09-10 14:02:43');
INSERT INTO "user" VALUES (5, 'test4', 'test4', 'test4', 'test4@test4.com', 1, '2019-09-10 14:02:43', '2019-09-10 14:02:43');

-- ----------------------------
-- Table structure for user_role
-- ----------------------------
DROP TABLE IF EXISTS "user_role";
CREATE TABLE "user_role" (
  "user_id" INTEGER NOT NULL,
  "role_id" INTEGER NOT NULL,
  PRIMARY KEY ("user_id", "role_id"),
  FOREIGN KEY ("role_id") REFERENCES "role" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION,
  FOREIGN KEY ("user_id") REFERENCES "user" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION
);

-- ----------------------------
-- Records of user_role
-- ----------------------------
INSERT INTO "user_role" VALUES (1, 1);
INSERT INTO "user_role" VALUES (2, 2);
INSERT INTO "user_role" VALUES (3, 2);

-- ----------------------------
-- Indexes structure for table permission
-- ----------------------------
CREATE INDEX "ix_permission_path"
ON "permission" (
  "path" ASC
);

-- ----------------------------
-- Indexes structure for table role
-- ----------------------------
CREATE INDEX "ix_role_name"
ON "role" (
  "name" ASC
);

-- ----------------------------
-- Indexes structure for table user
-- ----------------------------
CREATE UNIQUE INDEX "ix_user_username"
ON "user" (
  "username" ASC
);

-- ----------------------------
-- Table structure for device
-- ----------------------------
DROP TABLE IF EXISTS "device";
CREATE TABLE device (
	id INTEGER NOT NULL,
	type VARCHAR(15) NOT NULL,
	brand VARCHAR(32) NOT NULL,
	model VARCHAR(100) NOT NULL,
	os VARCHAR(15) NOT NULL,
	os_version VARCHAR(32),
	resolution VARCHAR(32),
	asset_no VARCHAR(100),
	root VARCHAR(3),
	location VARCHAR(32),
	status INTEGER,
	owner_id INTEGER,
	current_user_id INTEGER,
	"desc" VARCHAR(200),
	create_time DATETIME,
	update_time DATETIME,
	PRIMARY KEY (id),
	FOREIGN KEY(current_user_id) REFERENCES user (id),
	FOREIGN KEY(owner_id) REFERENCES user (id)
);




PRAGMA foreign_keys = true;
