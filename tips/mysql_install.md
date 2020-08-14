OS : Windows 10 x64

解压
解压路径为 %MYSQL_HOME%

配置环境变量
add %MYSQL_HOME%\bin to path

修改my.ini
拷贝my-default.ini为my.ini，没有就新建。

#修改默认编码方式为utf-8
[client]
default-character-set=utf8

[mysqld]
basedir = path\mysql-5.7.11-winx64
datadir =  path\mysql-5.7.11-winx64\data
port = 3306
character-set-server=utf8

初始化
mysqld --initialize --user=mysql --console
记录末尾的初始密码

以管理员启动cmd
安装服务
mysqld --install MySQL

启动/停止
net start/stop mysql

登录
mysql -u root -p

修改密码
set password for root@localhost = password('123456');
flush privileges