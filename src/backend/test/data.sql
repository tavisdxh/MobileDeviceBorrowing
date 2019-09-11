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
INSERT INTO "permission" VALUES (4, 'user_delete_user', '删除用户', NULL, '2019-09-10 14:02:43', '2019-09-10 14:02:43');
INSERT INTO "permission" VALUES (5, 'user_get_users', '获取所有用户', NULL, '2019-09-10 14:02:43', '2019-09-10 14:02:43');

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
INSERT INTO "role" VALUES (2, 'normal', '普通成员', '2019-09-10 14:02:43', '2019-09-10 14:02:43');

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
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS "user";
CREATE TABLE "user" (
  "id" INTEGER NOT NULL,
  "username" VARCHAR(32) NOT NULL,
  "password" VARCHAR(128) NOT NULL,
  "realname" VARCHAR(10) NOT NULL,
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

PRAGMA foreign_keys = true;