-- 检查 MySQL 现有用户的脚本
-- 使用 root 用户登录后运行此脚本

-- 查看所有用户
SELECT user, host FROM mysql.user;

-- 查看当前用户
SELECT USER(), CURRENT_USER();

-- 查看用户权限
SHOW GRANTS FOR CURRENT_USER();

-- 如果需要创建 userP6 用户（需要 root 权限）
-- CREATE USER 'userP6'@'localhost' IDENTIFIED BY 'mdpP6';
-- GRANT ALL PRIVILEGES ON foncieres.* TO 'userP6'@'localhost';
-- FLUSH PRIVILEGES;
