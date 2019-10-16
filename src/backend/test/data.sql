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
INSERT INTO "permission" VALUES (4, 'user_get_users', '获取用户列表', NULL, '2019-09-10 14:02:43', '2019-09-10 14:02:43');
INSERT INTO "permission" VALUES (5, 'device_add_device', '添加设备', NULL, '2019-09-10 14:02:43', '2019-09-10 14:02:43');
INSERT INTO "permission" VALUES (6, 'device_update_device', '更新设备', NULL, '2019-09-10 14:02:43', '2019-09-10 14:02:43');
INSERT INTO "permission" VALUES (7, 'device_get_device', '获取设备信息', NULL, '2019-09-10 14:02:43', '2019-09-10 14:02:43');
INSERT INTO "permission" VALUES (8, 'device_get_devices', '获取设备列表', NULL, '2019-09-10 14:02:43', '2019-09-10 14:02:43');
INSERT INTO "permission" VALUES (9, 'device_apply', '申请设备', NULL, '2019-09-10 14:02:43', '2019-09-10 14:02:43');
INSERT INTO "permission" VALUES (10, 'device_return', '归还设备', NULL, '2019-09-10 14:02:43', '2019-09-10 14:02:43');
INSERT INTO "permission" VALUES (11, 'device_audit', '审批设备', NULL, '2019-09-10 14:02:43', '2019-09-10 14:02:43');
INSERT INTO "permission" VALUES (12, 'device_cancel', '取消申请', NULL, '2019-09-10 14:02:43', '2019-09-10 14:02:43');

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
INSERT INTO "role_permission" VALUES (2, 6);
INSERT INTO "role_permission" VALUES (2, 7);
INSERT INTO "role_permission" VALUES (2, 8);
INSERT INTO "role_permission" VALUES (2, 9);
INSERT INTO "role_permission" VALUES (2, 10);
INSERT INTO "role_permission" VALUES (2, 11);
INSERT INTO "role_permission" VALUES (2, 12);

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
	"desc" VARCHAR(500),
	create_time DATETIME,
	update_time DATETIME,
	PRIMARY KEY (id),
	FOREIGN KEY(current_user_id) REFERENCES user (id),
	FOREIGN KEY(owner_id) REFERENCES user (id)
);

INSERT INTO "device" VALUES (1, 'phone', 'Apple', 'Apple iPhone XR (A2108) 128GB 黑色 移动联通电信4G手机 双卡双待', 'ios', '12.1.4', '1792×828', '20150731-0134', 'no', '广州', 1, 1, 2, '这个是补充信息', '2019-09-13 09:28:55', '2019-09-13 09:28:55');
INSERT INTO "device" VALUES (2, 'phone', 'Apple', 'Apple iPhone 8 (A1863) 64GB 银色 移动联通电信4G手机', 'ios', '12.1.3', '1334×750', '20150731-1111', 'no', '广州', 1, 1, 2, '这个是补充信息', '2019-09-13 09:33:09', '2019-09-13 09:33:09');
INSERT INTO "device" VALUES (3, 'phone', '华为', '华为 HUAWEI P30 Pro', 'android', '9.1', '2340*1080', '20150731-2222', 'no', '广州', 1, 1, 1, '这个是补充信息', '2019-09-13 09:53:24', '2019-09-13 09:53:24');
INSERT INTO "device" VALUES (4, 'phone', '华为', '华为 HUAWEI P30 Pro', 'android', '9.1', '2340*1080', '20150731-2222', 'no', '广州', 1, 2, 1, '这个是补充信息', '2019-09-13 09:53:24', '2019-09-13 09:53:24');

-- ----------------------------
-- Table structure for device_apply_record
-- ----------------------------
DROP TABLE IF EXISTS "device_apply_record";
CREATE TABLE device_apply_record (
	id INTEGER NOT NULL,
	device_id INTEGER NOT NULL,
	applicant_id INTEGER,
	start_time VARCHAR(20),
	end_time VARCHAR(20),
	application_desc VARCHAR(100),
	status INTEGER,
	apply_auditor_id INTEGER,
	return_auditor_id INTEGER,
	apply_audit_reason VARCHAR(100),
	return_audit_reason VARCHAR(100),
	notify_status INTEGER,
	notify_count INTEGER,
	create_time DATETIME,
	update_time DATETIME,
	PRIMARY KEY (id),
	FOREIGN KEY(applicant_id) REFERENCES user (id),
	FOREIGN KEY(apply_auditor_id) REFERENCES user (id),
	FOREIGN KEY(return_auditor_id) REFERENCES user (id)
);

PRAGMA foreign_keys = true;
