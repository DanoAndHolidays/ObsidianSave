# 00 MySQLQuick Start
> Last Format Time：10/7/2026 22:01:26

[https://www.bilibili.com/video/BV1Kr4y1i7ru](https://www.bilibili.com/video/BV1Kr4y1i7ru)

---
## 概念
MySQL 是==关系型数据库管理系统（DBMS）==，用表组织结构化数据，使用 SQL 查询与修改数据

| 概念              | 含义                          | 前端视角            |
| --------------- | --------------------------- | --------------- |
| Server          | 真正保存和处理数据的服务进程              | 后端基础设施          |
| Client          | 连接 Server 的工具，如 `mysql` 命令行 | 类似调用服务的客户端      |
| Database/Schema | 一组表等对象的命名空间，在 MySQL 中两词可互用  | 一个应用的数据集合       |
| Table           | 由列和行组成的数据表                  | 可类比结构固定的记录集合    |
| Column          | 字段及类型、约束                    | 类似对象属性，但有数据库级规则 |
| Row             | 一条记录                        | 类似一个数据对象        |
| Primary Key     | 唯一标识记录的非空键                  | 类似稳定的业务数据标识     |

---
## 连接数据库
连接需要主机名或 IP、端口、用户名、密码。MySQL 经典协议的默认端口是 3306；实际以服务配置为准。以下示例要求本地服务已启动，并已有可登录的 `root` 账户：
```powershell
mysql -h 127.0.0.1 -P 3306 -u root -p
```

- `-h`：主机；使用 `127.0.0.1` 明确连接本地 TCP。
- `-P`：大写 P 表示端口。
- `-u`：用户名。
- `-p`：小写 p 后不填密码，按提示交互输入。

原来的 `-p xxxx` 会把空格后的 `xxxx` 当作数据库名，而不是密码。虽然 `-p密码` 这种紧邻写法存在，但交互输入能避免密码直接进入命令记录。参见 [MySQL 连接选项](https://dev.mysql.com/doc/refman/8.4/en/connecting.html)。

登录后出现 `mysql>`，再输入 SQL。SQL 语句通常以分号结尾；退出客户端可输入 `exit`
```sql
SELECT VERSION();
SELECT CURRENT_USER(), DATABASE();
SHOW DATABASES;
```

---
## 创建练习库和表
```sql
CREATE DATABASE backend_notes_demo CHARACTER SET utf8mb4;
USE backend_notes_demo;

CREATE TABLE users (
    id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    age INT UNSIGNED NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE = InnoDB;

SHOW TABLES;
DESC users;
SHOW CREATE TABLE users;
```

- `AUTO_INCREMENT`：未手工指定 ID 时生成自增值，不保证连续；不要用 ID 推断记录总数
- `NOT NULL`：禁止空值，不代表字符串一定非空
- `UNIQUE`：唯一约束；本例与 `NOT NULL` 配合保证 email 有值且唯一
- `utf8mb4`：可表示完整 Unicode 字符范围，包括常见 emoji
- `InnoDB`：本例使用的存储引擎，支持事务与外键

字符串可用 `VARCHAR`，日期时间可用 `DATE` / `DATETIME`；金额等精确小数通常用 `DECIMAL`。字段类型应按业务范围设计，不要把所有数据都存成字符串。

参考 [建表入门](https://dev.mysql.com/doc/refman/8.4/en/creating-tables.html) 与 [主键和唯一约束](https://dev.mysql.com/doc/refman/8.4/en/constraint-primary-key.html)。

---
## 增删改查 CRUD
### 新增与查询
```sql
INSERT INTO users (name, email, age)
VALUES ('Dano', 'dano@example.com', 22),
       ('Lin', 'lin@example.com', 20),
       ('Ming', 'ming@example.com', NULL);

SELECT id, name, email, age
FROM users
ORDER BY id;

SELECT id, name
FROM users
WHERE age >= 21
ORDER BY id
LIMIT 10 OFFSET 0;

SELECT COUNT(*) AS total FROM users;
```

新库中依次应有 3 条记录，`age >= 21` 只命中 Dano，`total` 为 3。没有 `ORDER BY` 时不能依赖返回顺序；分页采用稳定排序，排序字段不唯一时补上 ID 作为次级排序键。`LIMIT 10 OFFSET 0` 表示跳过 0 行、最多返回 10 行。参见 [SELECT](https://dev.mysql.com/doc/refman/8.4/en/select.html)。

### 修改与删除
先用相同条件查询，确认目标后再修改；这里暂时只修改练习数据：
```sql
SELECT id, name, age FROM users WHERE email = 'dano@example.com';
UPDATE users SET age = 23 WHERE email = 'dano@example.com';

SELECT id, name FROM users WHERE email = 'ming@example.com';
DELETE FROM users WHERE email = 'ming@example.com';

SELECT COUNT(*) AS remaining FROM users;
```

执行后 Dano 为 23 岁，剩余 2 条记录。`UPDATE` / `DELETE` 省略 `WHERE` 会作用于全部行；`DELETE` 删除数据行，`DROP TABLE` 删除表对象，`TRUNCATE TABLE` 清空表，三者不是等价操作。

参见 [UPDATE](https://dev.mysql.com/doc/refman/8.4/en/update.html) 与 [DELETE](https://dev.mysql.com/doc/refman/8.4/en/delete.html)。

### NULL 与聚合
`NULL` 表示缺失或未知，不等于 `0`、空字符串。应使用 `IS NULL` / `IS NOT NULL`，不能用 `= NULL` 判断
```sql
SELECT id, name FROM users WHERE age IS NULL;
SELECT COUNT(*) AS rows_count, COUNT(age) AS known_age_count FROM users;
SELECT age, COUNT(*) AS people
FROM users
GROUP BY age
HAVING COUNT(*) >= 1
ORDER BY age;
```

若已经执行上面的删除，第一条查询为空，两种计数均为 2；若在删除 Ming 之前运行，`COUNT(*)` 为 3，`COUNT(age)` 为 2。`WHERE` 过滤原始行，`HAVING` 过滤分组结果。参见 [Working with NULL](https://dev.mysql.com/doc/refman/8.4/en/working-with-null.html)。

---
## 表关系与 JOIN
一个用户可以有多条待办，这是一对多关系；把用户 ID 存在待办表中，避免每条待办重复保存用户全部信息
```sql
CREATE TABLE todos (
    id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT UNSIGNED NOT NULL,
    title VARCHAR(100) NOT NULL,
    CONSTRAINT fk_todos_user FOREIGN KEY (user_id) REFERENCES users(id)
) ENGINE = InnoDB;

INSERT INTO todos (user_id, title)
SELECT id, 'Learn Spring Boot' FROM users WHERE email = 'dano@example.com';

SELECT u.name, t.title
FROM users AS u
LEFT JOIN todos AS t ON t.user_id = u.id
ORDER BY u.id, t.id;
```

预期 Dano 对应一条待办，Lin 的 `title` 为 `NULL`。`INNER JOIN` 只保留匹配行，`LEFT JOIN` 保留左表行，未匹配的右侧字段为 `NULL`。

本例外键要求 `user_id` 指向存在的用户，引用列和被引用列使用相同类型与无符号属性。没有配置级联删除时，不能随意删除仍被待办引用的用户。数据库约束与应用层校验可以互补。参见 [Using Foreign Keys](https://dev.mysql.com/doc/refman/8.4/en/example-foreign-keys.html)。

---
## 事务
一组操作一起成功或撤销

在同一个连接中，使用 InnoDB 表执行：
```sql
START TRANSACTION;
UPDATE users SET age = 99 WHERE email = 'dano@example.com';
SELECT age FROM users WHERE email = 'dano@example.com';
ROLLBACK;
SELECT age FROM users WHERE email = 'dano@example.com';
```

按前文顺序运行，事务内看到 99，回滚后看到 23。确认要保留改动时使用 `COMMIT`，它与这里的 `ROLLBACK` 是两种结束选择。

默认自动提交模式下，事务外的单条修改通常自动提交。显式事务让多条 DML 成为一个工作单元；发生业务失败时，应用需要正确回滚，不能假设所有错误都会自动撤销整组操作。参见 [事务控制](https://dev.mysql.com/doc/refman/8.4/en/commit.html)。

`CREATE`、`ALTER`、`DROP`、`TRUNCATE` 等许多 DDL 会触发隐式提交，不能把它们和普通 DML 一样理解为执行 `ROLLBACK` 就能恢复。参见 [隐式提交](https://dev.mysql.com/doc/refman/8.4/en/implicit-commit.html)。
