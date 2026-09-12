# 01 SQL 语句
> Last Format Time：9/12/2026 23:54:16

![[Pasted image 20260912233853.png]]

---
## SQL 分类与基本约定
*已补充*

SQL 有标准，但各数据库仍存在方言和实现差异，例如 MySQL 的 `AUTO_INCREMENT`、`LIMIT` 和反引号用法不能直接照搬到所有数据库。

| 学习分类 | 用途 | 常见语句 |
|---|---|---|
| DDL | 定义数据库对象 | `CREATE`、`ALTER`、`DROP`、`TRUNCATE` |
| DML | 操作数据 | `INSERT`、`UPDATE`、`DELETE` |
| DQL | 查询数据，教学中常单列 | `SELECT` |
| DCL | 控制权限 | `GRANT`、`REVOKE` |
| TCL | 控制事务 | `START TRANSACTION`、`COMMIT`、`ROLLBACK` |

这些分类便于记忆，不是所有文档都采用相同分组。MySQL 官方将 `SELECT` 归在 Data Manipulation Statements 中，将账户管理与事务控制另列。参见 [SQL Statements](https://dev.mysql.com/doc/refman/8.4/en/sql-statements.html)。

- 语句使用英文半角分号 `;`，不能写成中文 `；`。
- 关键字大小写通常不影响含义，笔记统一大写以便阅读；数据库名、表名的大小写行为与平台和配置有关，不要据此推断所有名称都不区分大小写。
- 字符串使用单引号，如 `'Dano'`；需要引用标识符时，MySQL 使用反引号。
- `-- ` 单行注释中，两条横线后需要空白；也可使用 `/* 注释 */`。

注释语法见 [MySQL Comments](https://dev.mysql.com/doc/refman/8.4/en/comments.html)。

---
## 数据库操作
*已纠正*

原例中的 `[IF NOT EXISTS]`、`[DEFAULT ...]` 是语法说明里的可选部分，方括号不应出现在实际 SQL 中。语法模板如下，`数据库名` 也需要替换：
```text
CREATE DATABASE [IF NOT EXISTS] 数据库名 [DEFAULT CHARACTER SET utf8mb4];
DROP DATABASE [IF EXISTS] 数据库名;
```

以下为可执行示例，使用独立练习库 `sql_syntax_demo`。如果同名库已存在，先确认用途或换名，不继续修改已有数据：
```sql
-- 查询当前账户可见的数据库
SHOW DATABASES;

-- 查询当前连接选中的数据库；未选中时为 NULL
SELECT DATABASE();

-- 创建练习库
CREATE DATABASE sql_syntax_demo DEFAULT CHARACTER SET utf8mb4;

-- 使用 / 切换数据库
USE sql_syntax_demo;

-- 查看数据库定义
SHOW CREATE DATABASE sql_syntax_demo;
```

`IF NOT EXISTS` 只避免“已存在”导致的错误，不会把已有库自动改成声明的字符集，也不验证旧库结构是否符合预期。`USE` 只改变当前会话的默认数据库。参见 [CREATE DATABASE](https://dev.mysql.com/doc/refman/8.4/en/create-database.html)。

---
## 表结构操作
*已补充*

在前面的练习库中按顺序运行：
```sql
CREATE TABLE products (
    id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    price DECIMAL(10, 2) NOT NULL DEFAULT 0.00
) ENGINE = InnoDB;

SHOW TABLES;
DESC products;
SHOW CREATE TABLE products;

-- 添加字段
ALTER TABLE products ADD COLUMN stock INT UNSIGNED NOT NULL DEFAULT 0;

-- 修改字段定义；需要保留的 NOT NULL、DEFAULT 等属性也写完整
ALTER TABLE products MODIFY COLUMN name VARCHAR(150) NOT NULL;

-- MySQL 8 的列重命名语法
ALTER TABLE products RENAME COLUMN name TO title;

DESC products;
```

上面执行后字段为 `id`、`title`、`price`、`stock`。`DECIMAL(10,2)` 表示最多 10 位十进制数字，其中 2 位在小数点后。这里没有价格非负约束，业务有要求时应再设计校验和约束。

修改列类型、缩短长度或删除列可能影响已有数据，先确认现有数据能满足新定义。参见 [ALTER TABLE](https://dev.mysql.com/doc/refman/8.4/en/alter-table.html) 与 [DECIMAL](https://dev.mysql.com/doc/refman/8.4/en/fixed-point-types.html)。

---
## 操作数据与查询顺序
*已补充*

```sql
INSERT INTO products (title, price, stock)
VALUES ('Notebook', 12.50, 10), ('Pen', 3.00, 30);

SELECT id, title, price, stock
FROM products
WHERE price >= 5.00
ORDER BY price DESC, id ASC
LIMIT 10;

UPDATE products SET stock = stock - 1 WHERE id = 1 AND stock > 0;
SELECT id, title, stock FROM products WHERE id = 1;
```

在新库按顺序执行时，查询价格大于等于 5 的结果为 Notebook，更新后其库存为 9。条件更新后还需要由应用检查影响行数，不能只发送 SQL 就认定扣减成功。

常用查询的书写顺序：
```text
SELECT 列
FROM 表
WHERE 行过滤条件
GROUP BY 分组列
HAVING 分组过滤条件
ORDER BY 排序列
LIMIT 返回行数 OFFSET 跳过行数;
```

这描述的是语法书写顺序，不代表数据库执行计划一定逐行照此运行。`SELECT *` 便于临时查看，业务查询通常显式列出需要的字段。参见 [SELECT](https://dev.mysql.com/doc/refman/8.4/en/select.html)。

---
## 删除操作的区别
*已补充*

| 操作 | 影响 | 事务边界 |
|---|---|---|
| `DELETE FROM products WHERE id = 2` | 删除符合条件的行，保留表结构 | InnoDB 显式事务未提交时可以回滚 |
| `TRUNCATE TABLE products` | 清空整表，通常重置自增计数 | DDL，会隐式提交，不能当作普通可回滚删除 |
| `DROP TABLE products` | 删除表及其数据 | DDL |
| `DROP DATABASE sql_syntax_demo` | 删除整个数据库及其中对象 | DDL |

练习删除一行可以先演示回滚：
```sql
START TRANSACTION;
DELETE FROM products WHERE id = 2;
SELECT COUNT(*) AS during_transaction FROM products;
ROLLBACK;
SELECT COUNT(*) AS after_rollback FROM products;
```

预期计数先为 1，回滚后为 2。若处于默认自动提交模式，事务外执行并已提交的 `DELETE` 不能靠随后执行 `ROLLBACK` 撤销。

下面只用于练习结束后清理本篇专用库，不要与前面的学习步骤整段一起执行；确认库名和用途后才运行：
```sql
DROP DATABASE IF EXISTS sql_syntax_demo;
```

`IF EXISTS` 只控制目标不存在时的处理，不会提供误删保护或恢复能力。参见 [隐式提交语句](https://dev.mysql.com/doc/refman/8.4/en/implicit-commit.html)。
