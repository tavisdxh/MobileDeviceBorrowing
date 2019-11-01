use mobile_device_borrowing;

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

TRUNCATE device;
TRUNCATE device_apply_record;
TRUNCATE device_log;
TRUNCATE permission;
TRUNCATE role;
TRUNCATE role_permission;
TRUNCATE user;
TRUNCATE user_role;

-- ----------------------------
-- Records of permission
-- ----------------------------
INSERT INTO `permission` VALUES (1, 'user_get_user', '获取用户信息', NULL, '2019-09-10 14:02:43', '2019-09-10 14:02:43');
INSERT INTO `permission` VALUES (2, 'user_update_user', '更新用户信息', NULL, '2019-09-10 14:02:43', '2019-09-10 14:02:43');
INSERT INTO `permission` VALUES (3, 'user_update_password', '修改密码', NULL, '2019-09-10 14:02:43', '2019-09-10 14:02:43');
INSERT INTO `permission` VALUES (4, 'user_get_users', '获取用户列表', NULL, '2019-09-10 14:02:43', '2019-09-10 14:02:43');
INSERT INTO `permission` VALUES (5, 'device_add_device', '添加设备', NULL, '2019-09-10 14:02:43', '2019-09-10 14:02:43');
INSERT INTO `permission` VALUES (6, 'device_update_device', '更新设备', NULL, '2019-09-10 14:02:43', '2019-09-10 14:02:43');
INSERT INTO `permission` VALUES (7, 'device_get_device', '获取设备信息', NULL, '2019-09-10 14:02:43', '2019-09-10 14:02:43');
INSERT INTO `permission` VALUES (8, 'device_get_devices', '获取设备列表', NULL, '2019-09-10 14:02:43', '2019-09-10 14:02:43');
INSERT INTO `permission` VALUES (9, 'device_apply', '申请设备', NULL, '2019-09-10 14:02:43', '2019-09-10 14:02:43');
INSERT INTO `permission` VALUES (10, 'device_return', '归还设备', NULL, '2019-09-10 14:02:43', '2019-09-10 14:02:43');
INSERT INTO `permission` VALUES (11, 'device_audit', '审批设备', NULL, '2019-09-10 14:02:43', '2019-09-10 14:02:43');
INSERT INTO `permission` VALUES (12, 'device_cancel', '取消申请', NULL, '2019-09-10 14:02:43', '2019-09-10 14:02:43');
INSERT INTO `permission` VALUES (13, 'device_disable_device', '禁用设备', NULL, '2019-09-10 14:02:43', '2019-09-10 14:02:43');
INSERT INTO `permission` VALUES (14, 'role_add', '添加角色', NULL, '2019-09-10 14:02:43', '2019-09-10 14:02:43');
INSERT INTO `permission` VALUES (15, 'role_update', '修改角色', NULL, '2019-09-10 14:02:43', '2019-09-10 14:02:43');
INSERT INTO `permission` VALUES (16, 'role_delete', '删除角色', NULL, '2019-09-10 14:02:43', '2019-09-10 14:02:43');
INSERT INTO `permission` VALUES (17, 'role_get', '获取角色信息', NULL, '2019-09-10 14:02:43', '2019-09-10 14:02:43');
INSERT INTO `permission` VALUES (18, 'role_get_roles', '获取角色列表', NULL, '2019-09-10 14:02:43', '2019-09-10 14:02:43');
INSERT INTO `permission` VALUES (19, 'role_assign_permission', '分配角色权限', NULL, '2019-09-10 14:02:43', '2019-09-10 14:02:43');
INSERT INTO `permission` VALUES (20, 'role_assign_user', '分配角色用户', NULL, '2019-09-10 14:02:43', '2019-09-10 14:02:43');
INSERT INTO `permission` VALUES (21, 'role_user_assign_role', '用户分配角色', NULL, '2019-09-10 14:02:43', '2019-09-10 14:02:43');

-- ----------------------------
-- Records of role
-- ----------------------------
INSERT INTO `role` VALUES (1, 'admin', '管理员', '2019-09-10 14:02:43', '2019-09-10 14:02:43');

-- ----------------------------
-- Records of user
-- ----------------------------
INSERT INTO `user` VALUES (1, 'admin', 'admin', '超级管理员', 'admin@admin.com', 1, '2019-09-10 14:02:43', '2019-09-10 14:02:43');

-- ----------------------------
-- Records of user_role
-- ----------------------------
INSERT INTO `user_role` VALUES (1, 1);


SET FOREIGN_KEY_CHECKS = 1;
