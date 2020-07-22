
## 安装java
```
wget https://download.oracle.com/otn/java/jdk/8u152-b16/aa0333dd3019491ca4f6ddbe78cdb6d0/jdk-8u152-linux-x64.tar.gz
wget https://mirrors.huaweicloud.com/java/jdk/8u152-b16/jdk-8u152-linux-x64.tar.gz
mv /usr/bin/java /usr/bin/java.bak
tar -zxvf jdk-8u152-linux-x64.tar.gz -C /usr/local/
vi /etc/profile

export JAVA_HOME=/usr/local/jdk1.8.0_152/
export CLASSPATH=.:${JAVA_HOME}lib/dt.jar:${JAVA_HOME}lib/tools.jar:${JAVA_HOME}jre/lib/rt.jar
export PATH=$PATH:$JAVA_HOME/bin:

sudo ln -s /usr/local/jdk1.8.0_152/bin/java /usr/local/bin/java
sudo ln -s /usr/local/jdk1.8.0_152/bin/java /usr/local/java
```

## 安装dble
```
wget -c https://github.com/actiontech/dble/releases/download/2.20.04.0%2Ftag/actiontech-dble-2.20.04.0.tar.gz
tar -xvf tag.tar.gz

cp -rp /home/microk8s/code/edm/Learn/DBLE/actiontech-dble-2.20.04.0.tar.gz /usr/local
cd /usr/local
tar -xvf actiontech-dble-2.20.04.0.tar.gz

sudo ln -s /home/microk8s/code/edm/Learn/DBLE/dble/bin/dble /usr/local/bin/dble

配置 schema.cml  server.xml  rule.xml
```


## 在两套MySQL服务器上配置root用户
```
docker run --name backend-mysql1 -e MYSQL_ROOT_PASSWORD=123456 -p 33061:3306 -d mysql:8.0 --server-id=1 
docker run --name backend-mysql2 -e MYSQL_ROOT_PASSWORD=123456 -p 33062:3306 -d mysql:8.0 --server-id=2 

docker ps 
```
mysql -uroot -P33061 -h127.0.0.1 -p123456
GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' IDENTIFIED BY '123456' WITH GRANT OPTION;
flush privileges;

## 启动dble
```
dble start
```

## 登录验证
```
mysql -uroot -p -P8066 -h127.0.0.1 -p123456
show databases;
use testdb;
show tables;
```

## 创建分片
```
    <dataNode name="dn1" dataHost="dataHost1" database="db_1"/>
    <dataNode name="dn2" dataHost="dataHost2" database="db_2"/>
    <dataNode name="dn3" dataHost="dataHost1" database="db_3"/>
    <dataNode name="dn4" dataHost="dataHost2" database="db_4"/>
    <dataNode name="dn5" dataHost="dataHost1" database="db_5"/>
    <dataNode name="dn6" dataHost="dataHost2" database="db_6"/>
    
mysql -uman1 -p -P9066 -h192.168.56.185 -p654321
mysql -uman1 -p -P9066 -h127.0.0.1 -p654321
create database @@dataNode='dn$1-6';    
```

## 查看结果
```
mysql -uroot -P33061 -h127.0.0.1 -p123456
mysql> show databases;
+--------------------+
| Database           |
+--------------------+
| db_1               |
| db_3               |
| db_5               |
| information_schema |
| mysql              |
| performance_schema |
| sys                |
+--------------------+
7 rows in set (0.00 sec)

mysql -uroot -P33062 -h127.0.0.1 -p123456
```

## 创建表
```
mysql -uroot -p -P8066 -h127.0.0.1 -p123456
source /home/microk8s/code/dble_blog/dble/conf/template_table.sql 

mysql> explain select * from blog_article where id=1285758779131955700;
+-----------+----------+---------------------------------------------------------+
| DATA_NODE | TYPE     | SQL/REF                                                 |
+-----------+----------+---------------------------------------------------------+
| dn1       | BASE SQL | select * from blog_article where id=1285758779131955700 |
+-----------+----------+---------------------------------------------------------+
1 row in set (0.00 sec)

mysql> explain select * from blog_article_tag where blog_article_id=1285758779131955700;
+-----------+----------+--------------------------------------------------------------------------+
| DATA_NODE | TYPE     | SQL/REF                                                                  |
+-----------+----------+--------------------------------------------------------------------------+
| dn1       | BASE SQL | select * from blog_article_tag where blog_article_id=1285758779131955700 |
+-----------+----------+--------------------------------------------------------------------------+
1 row in set (0.00 sec)




mysql> explain select * from blog_article where id=1285758796311825700;
+-----------+----------+---------------------------------------------------------+
| DATA_NODE | TYPE     | SQL/REF                                                 |
+-----------+----------+---------------------------------------------------------+
| dn5       | BASE SQL | select * from blog_article where id=1285758796311825700 |
+-----------+----------+---------------------------------------------------------+
1 row in set (0.00 sec)

mysql> explain select * from blog_article_tag where blog_article_id=1285758796311825700;
+-----------+----------+--------------------------------------------------------------------------+
| DATA_NODE | TYPE     | SQL/REF                                                                  |
+-----------+----------+--------------------------------------------------------------------------+
| dn5       | BASE SQL | select * from blog_article_tag where blog_article_id=1285758796311825700 |
+-----------+----------+--------------------------------------------------------------------------+
1 row in set (0.00 sec)



explain select * from blog_article where id in (1285758796311825700, 1285758779131955700);

```

## 问题
1. int字段改为bigint报错，一开始要建立bigint类型
2. ChildTable multi insert not provided




