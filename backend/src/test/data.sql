use mobile_device_borrowing;
SET FOREIGN_KEY_CHECKS = 0;
REPLACE INTO permission VALUES (1, 'user_get_user', '获取用户信息', NULL, '2019-09-10 14:02:43', '2019-09-10 14:02:43');
REPLACE INTO permission VALUES (2, 'user_update_user', '更新用户信息', NULL, '2019-09-10 14:02:43', '2019-09-10 14:02:43');
REPLACE INTO permission VALUES (3, 'user_update_password', '修改密码', NULL, '2019-09-10 14:02:43', '2019-09-10 14:02:43');
REPLACE INTO permission VALUES (4, 'user_get_users', '获取用户列表', NULL, '2019-09-10 14:02:43', '2019-09-10 14:02:43');
REPLACE INTO permission VALUES (5, 'device_add_device', '添加设备', NULL, '2019-09-10 14:02:43', '2019-09-10 14:02:43');
REPLACE INTO permission VALUES (6, 'device_update_device', '更新设备', NULL, '2019-09-10 14:02:43', '2019-09-10 14:02:43');
REPLACE INTO permission VALUES (7, 'device_get_device', '获取设备信息', NULL, '2019-09-10 14:02:43', '2019-09-10 14:02:43');
REPLACE INTO permission VALUES (8, 'device_get_devices', '获取设备列表', NULL, '2019-09-10 14:02:43', '2019-09-10 14:02:43');
REPLACE INTO permission VALUES (9, 'device_apply', '申请设备', NULL, '2019-09-10 14:02:43', '2019-09-10 14:02:43');
REPLACE INTO permission VALUES (10, 'device_return', '归还设备', NULL, '2019-09-10 14:02:43', '2019-09-10 14:02:43');
REPLACE INTO permission VALUES (11, 'device_audit', '审批设备', NULL, '2019-09-10 14:02:43', '2019-09-10 14:02:43');
REPLACE INTO permission VALUES (12, 'device_cancel', '取消申请', NULL, '2019-09-10 14:02:43', '2019-09-10 14:02:43');
REPLACE INTO permission VALUES (13, 'device_disable_device', '禁用设备', NULL, '2019-09-10 14:02:43', '2019-09-10 14:02:43');
REPLACE INTO permission VALUES (14, 'role_add', '添加角色', NULL, '2019-09-10 14:02:43', '2019-09-10 14:02:43');
REPLACE INTO permission VALUES (15, 'role_update', '修改角色', NULL, '2019-09-10 14:02:43', '2019-09-10 14:02:43');
REPLACE INTO permission VALUES (16, 'role_delete', '删除角色', NULL, '2019-09-10 14:02:43', '2019-09-10 14:02:43');
REPLACE INTO permission VALUES (17, 'role_get', '获取角色信息', NULL, '2019-09-10 14:02:43', '2019-09-10 14:02:43');
REPLACE INTO permission VALUES (18, 'role_get_roles', '获取角色列表', NULL, '2019-09-10 14:02:43', '2019-09-10 14:02:43');
REPLACE INTO permission VALUES (19, 'role_assign_permission', '分配角色权限', NULL, '2019-09-10 14:02:43', '2019-09-10 14:02:43');
REPLACE INTO permission VALUES (20, 'role_assign_user', '分配角色用户', NULL, '2019-09-10 14:02:43', '2019-09-10 14:02:43');
REPLACE INTO permission VALUES (21, 'role_user_assign_role', '用户分配角色', NULL, '2019-09-10 14:02:43', '2019-09-10 14:02:43');
REPLACE INTO role VALUES (1, 'admin', '管理员', '2019-09-10 14:02:43', '2019-09-10 14:02:43');
REPLACE INTO role VALUES (2, 'normal', '普通用户', '2019-09-10 14:02:43', '2019-09-10 14:02:43');
REPLACE INTO role VALUES (3, '角色1', '角色1', '2019-09-10 14:02:43', '2019-09-10 14:02:43');
REPLACE INTO role_permission VALUES (2, 1);
REPLACE INTO role_permission VALUES (2, 2);
REPLACE INTO role_permission VALUES (2, 3);
REPLACE INTO role_permission VALUES (2, 4);
REPLACE INTO role_permission VALUES (2, 5);
REPLACE INTO role_permission VALUES (2, 6);
REPLACE INTO role_permission VALUES (2, 7);
REPLACE INTO role_permission VALUES (2, 8);
REPLACE INTO role_permission VALUES (2, 9);
REPLACE INTO role_permission VALUES (2, 10);
REPLACE INTO role_permission VALUES (2, 11);
REPLACE INTO role_permission VALUES (2, 12);
REPLACE INTO role_permission VALUES (2, 13);
REPLACE INTO role_permission VALUES (2, 14);
REPLACE INTO role_permission VALUES (2, 15);
REPLACE INTO role_permission VALUES (2, 16);
REPLACE INTO role_permission VALUES (2, 17);
REPLACE INTO role_permission VALUES (2, 18);
REPLACE INTO role_permission VALUES (2, 19);
REPLACE INTO role_permission VALUES (2, 20);
REPLACE INTO role_permission VALUES (2, 21);
REPLACE INTO user VALUES (1, 'admin', 'admin', '超级管理员', 'admin@admin.com', 1, '2019-09-10 14:02:43', '2019-09-10 14:02:43');
REPLACE INTO user VALUES (2, 'test1', 'test1', 'test1', 'test1@test1.com', 1, '2019-09-10 14:02:43', '2019-09-10 14:02:43');
REPLACE INTO user VALUES (3, 'test2', 'test2', 'test2', 'test2@test2.com', 1, '2019-09-10 14:02:43', '2019-09-10 14:02:43');
REPLACE INTO user VALUES (4, 'test3', 'test3', 'test3', 'test3@test3.com', 1, '2019-09-10 14:02:43', '2019-09-10 14:02:43');
REPLACE INTO user VALUES (5, 'test4', 'test4', 'test4', 'test4@test4.com', 1, '2019-09-10 14:02:43', '2019-09-10 14:02:43');
REPLACE INTO user_role VALUES (1, 1);
REPLACE INTO user_role VALUES (2, 2);
REPLACE INTO user_role VALUES (3, 2);
REPLACE INTO device VALUES (1, 'phone', 'Apple', 'Apple iPhone XR (A2108) 128GB 黑色 移动联通电信4G手机 双卡双待', 'ios', '12.1.4', '1792×828', '20150731-0134', 'no', '广州', 1, 1, 2, '这个是补充信息', '2019-09-13 09:28:55', '2019-09-13 09:28:55');
REPLACE INTO device VALUES (2, 'phone', 'Apple', 'Apple iPhone 8 (A1863) 64GB 银色 移动联通电信4G手机', 'ios', '12.1.3', '1334×750', '20150731-1111', 'no', '广州', 1, 1, 2, '这个是补充信息', '2019-09-13 09:33:09', '2019-09-13 09:33:09');
REPLACE INTO device VALUES (3, 'phone', '华为', '华为 HUAWEI P30 Pro', 'android', '9.1', '2340*1080', '20150731-2222', 'no', '广州', 1, 1, 1, '这个是补充信息', '2019-09-13 09:53:24', '2019-09-13 09:53:24');
REPLACE INTO device VALUES (4, 'phone', '华为', '华为 HUAWEI P30 Pro', 'android', '9.1', '2340*1080', '20150731-2222', 'no', '广州', 1, 2, 1, '这个是补充信息', '2019-09-13 09:53:24', '2019-09-13 09:53:24');
SET FOREIGN_KEY_CHECKS = 1;