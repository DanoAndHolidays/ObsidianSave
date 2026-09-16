# 02 DDL 、 DML 与  DQL
> Last Format Time：9/16/2026 19:24:55

---
## DDL
![[Pasted image 20260913001334.png]]

```sql
CREATE TABLE USER2(
  id INT PRIMARY KEY AUTO_INCREMENT,
  username VARCHAR (50) NOT NULL UNIQUE,
  name varchar(10) NOT NULL,
  age INT,
  gender char(1) DEFAULT('男')
) comment '用户信息表';
```

```sql
show tables;-- 查询当前数据库的所有表
desc 表名; -- 查询表结构
show create table 表名; -- 查询建表语句

alter table 表名 add 字段名 类型(长度)[comment 注释] [约束]; --添加字段
alter table 表名 modify 字段名 新数据类型(长度);--修改字段类型
alter table 表名 change |旧字段名新字段名类型(长度)[comment 注释] [约束];--修改字段名与字段类型
alter table 表名 drop column 字段名; -- 删除字段
alter table 表名 rename to 新表名; -- 修改表名

drop table [if exists] 表名; -- 删除表
```

---
## DML
```sql
--指定字段添加数据[批量]
insert into 表名(字段名1,字段名2) values (值1,值2)[, (值1,值2)];

--全部字段添加数据[批量]
insert into 表名 values (值1,值2, ...)[, (值1,值2)];
```

```sql
-- 修改数据
update 表名 set 字段名1 = 值1，字段名2 = 值2， .... [ where 条件 ];
```

```sql
-- 删除数据
delete from 表名 [where 条件];
```

---
## DQL
```sql
select
	字段列表
from
	表名列表
where
	条件列表
group by
	分组字段列表
having
	分组后条件列表
order by
	排序字段列表
limit
	分页参数
```

```sql
-- 查询多个字段
select 字段1,字段2,字段3 from 表名；

-- 查询所有字段(通配符)，性能不好，不如直接全写出来
select * from 表名;

--为查询字段设置别名，as关键字可以省略
select 字段1[as 别名1]，字段2[as 别名2] from 表名;

-- 去除重复记录
select distinct 字段列表 from 表名;
```

```sql
select 字段列表 from 表名 where 条件列表；
```

| 条件          | 表达式举例1          | 表达式举例2           | 说明                                  |
| ----------- | --------------- | ---------------- | ----------------------------------- |
| =           | score = 80      | name = 'abc'     | 字符串需要用单引号括起来                        |
| >           | score > 80      | name > 'abc'     | 字符串比较根据ASCII码，中文字符比较根据数据库设置         |
| >=          | score >= 80     | name >= 'abc'    |                                     |
| <           | score < 80      | name <= 'abc'    |                                     |
| <=          | score <= 80     | name <= 'abc'    |                                     |
| <> !=       | score <> 80     | name <> 'abc'    |                                     |
| LIKE        | name LIKE 'ab%' | name LIKE '%bc%' | %表示任意字符，例如'ab%'将匹配'ab'，'abc'，'abcd' |
| between and |                 |                  |                                     |
| is null     |                 |                  |                                     |
| and &&      |                 |                  |                                     |
| or \|\|     |                 |                  |                                     |
| not !       |                 |                  |                                     |

```sql
SELECT 字段
FROM 表名
ORDER BY 字段 [ASC | DESC];

SELECT *
FROM user
LIMIT 10, 10;
```

### 聚合函数
|聚合函数|返回|
|---|---|
|`SUM`|数字字段表达式中值的总计。例如，`SUM(SALARY)` 返回所有薪金字段值的总和。|
|`AVG`|数字字段表达式中值的平均值。例如，`AVG(SALARY)` 返回所有薪金字段值的平均值。|
|`COUNT`|字段表达式中值的数目。例如，`COUNT(NAME)` 返回名称值的数目。将 `COUNT` 与字段名一起使用时，`COUNT` 返回非 null 字段值的数目。特例为 `COUNT(*)`，它返回集合中记录的数目，包括值为 null 的记录。|
|`MAX`|字段表达式中的最大值。例如，`MAX(SALARY)` 返回最大的薪金字段值。|
|`MIN`|字段表达式中的最小值。例如，`MIN(SALARY)` 返回最小的薪金字段值。|

```sql
--分组查询
select 字段列表from 表名 [where 条件列表] group by 分组字段名 [having 分组后过滤条件];
```

where与having的区别:
- 执行时机不同: where是分组之前进行过滤，不满足where条件，不参与分组。而having是分组之后对结果进行过滤。
- 判断条件不同: where不能对聚合函数进行判断，而having可以。