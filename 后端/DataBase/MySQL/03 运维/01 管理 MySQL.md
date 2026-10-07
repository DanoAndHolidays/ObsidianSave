# 01 管理 MySQL
> Last Format Time：10/7/2026 22:01:26

---
## 系统数据库
![[Pasted image 20261007171256.png]]

---
## 常用工具
### mysql
mysql 不是指 mysql 服务，而是指 mysql 的客户端工具

```sh
mysql [options] [database]
```

* -u  --user=name：指定用户名
* -p  --password[=name]：指定密码
* -h  --host=name：指定服务器IP或域名
* -P  --port=#：指定连接端口
* -e  --execute=name：执行SQL语句并退出，在控制台执行SQL语句，而不用连接到数据库执行

示例：
```sh
mysql -h 127.0.0.1 -P 3306 -u root -p
mysql -u root -p 2143 db01 -e "select * from tb_book";
```

### mysqladmin
mysqladmin 是一个执行管理操作的客户端程序，用来检查服务器的配置和当前状态、创建并删除数据库等

通过 `mysqladmin --help` 指令查看帮助文档

```sh
mysqladmin -u root -p 2143 create 'test01';
```

### mysqlbinlog
服务器生成的日志文件以二进制格式保存，如果需要检查这些文本，就要使用 mysqlbinlog 日志管理工具

```shell
mysqlbinlog [options] log-files1 log-files2 ...
```

* -d  --database=name：指定数据库名称，只列出指定的数据库相关操作

* -o  --offset=#：忽略掉日志中的前 n 行命令。

* -r  --result-file=name：将输出的文本格式日志输出到指定文件。

* -s  --short-form：显示简单格式，省略掉一些信息。

* --start-datatime=date1  --stop-datetime=date2：指定日期间隔内的所有日志

* --start-position=pos1 --stop-position=pos2：指定位置间隔内的所有日志


### mysqldump
##### 命令介绍
mysqldump 客户端工具用来备份数据库或在不同数据库之间进行数据迁移，备份内容包含创建表，及插入表的 SQL 语句

```sh
mysqldump [options] db_name [tables]
mysqldump [options] --database/-B db1 [db2 db3...]
mysqldump [options] --all-databases/-A
```

连接选项：

* -u  --user=name：指定用户名
* -p  --password[=name]：指定密码
* -h  --host=name：指定服务器 IP 或域名
* -P  --port=#：指定连接端口

输出内容选项：

* --add-drop-database：在每个数据库创建语句前加上 Drop database 语句
* --add-drop-table：在每个表创建语句前加上 Drop table 语句 , 默认开启，不开启 (--skip-add-drop-table)
* -n  --no-create-db：不包含数据库的创建语句
* -t  --no-create-info：不包含数据表的创建语句
* -d --no-data：不包含数据
* -T, --tab=name：自动生成两个文件：一个 .sql 文件，创建表结构的语句；一个 .txt 文件，数据文件，相当于 select into outfile  

示例：
```sh
mysqldump -uroot -p2143 db01 tb_book --add-drop-database --add-drop-table > a
mysqldump -uroot -p2143 -T /tmp test city
```

##### 数据备份
命令行方式：

* 备份命令：mysqldump -u root -p 数据库名称 > 文件保存路径
* 恢复
  1. 登录MySQL数据库：`mysql -u root p`
  2. 删除已经备份的数据库
  3. 重新创建与备份数据库名称相同的数据库
  4. 使用该数据库
  5. 导入文件执行：`source 备份文件全路径`

更多方式参考：https://time.geekbang.org/column/article/81925

图形化界面：

* 备份

  ![图形化界面备份](https://seazean.oss-cn-beijing.aliyuncs.com/img/DB/图形化界面备份.png)

* 恢复

  ![图形化界面恢复](https://seazean.oss-cn-beijing.aliyuncs.com/img/DB/图形化界面恢复.png)

### mysqlimport
mysqlimport 是客户端数据导入工具，用来导入mysqldump 加 -T 参数后导出的文本文件

```sh
mysqlimport [options]  db_name  textfile1  [textfile2...]
```

示例：
```sh
mysqlimport -uroot -p2143 test /tmp/city.txt
```

导入 sql 文件，可以使用 MySQL 中的 source 指令 : 
```mysql
source 文件全路径
```

### mysqlshow
mysqlshow 客户端对象查找工具，用来很快地查找存在哪些数据库、数据库中的表、表中的列或者索引

```sh
mysqlshow [options] [db_name [table_name [col_name]]]
```

* --count：显示数据库及表的统计信息（数据库，表 均可以不指定）
* -i：显示指定数据库或者指定表的状态信息

示例：
```sh
#查询每个数据库的表的数量及表中记录的数量
mysqlshow -uroot -p1234 --count
#查询test库中每个表中的字段书，及行数
mysqlshow -uroot -p1234 test --count
#查询test库中book表的详细情况
mysqlshow -uroot -p1234 test book --count
```
