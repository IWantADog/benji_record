```shell
wget --no-check-certificate https://raw.githubusercontent.com/teddysun/shadowsocks_install/master/shadowsocks-go.sh
chmod +x shadowsocks-go.sh
./shadowsocks-go.sh 2>&1 | tee shadowsocks-go.log
```

cat /etc/shadowsocks/config.json

多用户配置

```json
{
    "port_password":{
         "8989":"password0",
         "9001":"password1",
         "9002":"password2",
         "9003":"password3",
         "9004":"password4"
    },
    "method":"aes-256-cfb",
    "timeout":600
}
```


centos firewall

```shell
systemctl status firewalld

firewall-cmd --zone=public --add-port=80/tcp --permanent

firewall-cmd --zone=public --remove-port=80/tcp --permanent

firewall-cmd --zone=public --list-ports
```