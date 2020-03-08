# linux相关命令总结及说明

## server login info

w: 服务器当前谁在登录

last：最近谁登录过。登录的信息存放在/var/log/wtmp二进制文件中（容易被删除）。

history：最近使用的命令。历史命令的信息存放在~/.bash_history中（容易被删除）。

strace -p PID: 显示进程调度的资源

lsof -p PID: 程序打开的文件。（句柄）

lsof -i or netstat -plunt：列出正在联网的进程

/var/log/secure: 记录主机的安全信息

/etc/passwd: 用户、用户密码、shell信息

## ssh info

ssh-copy-id: 将公匙发送到目标主机

/.ssh/authorized_keys: 记录所有的公匙信息，也可手动将公匙加入文件的最后。

## user

adduser username

passwd username

usermod -aG wheel username