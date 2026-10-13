# 13 Bean 类型
> Last Format Time：10/6/2026 02:27:25

[https://ocn8gnorkt9i.feishu.cn/docx/JjrCdGixIoeFi1xpuk8cgnWSnuf](https://ocn8gnorkt9i.feishu.cn/docx/JjrCdGixIoeFi1xpuk8cgnWSnuf)

| **名称** | **说明**                              |
| ------ | ----------------------------------- |
| Entity | 实体，通常和数据库中的表对应                      |
| DTO    | 数据传输对象，通常用于程序中各层之间传递数据              |
| VO     | 视图对象，为前端展示数据提供的对象                   |
| POJO   | 普通 Java 对象，只有属性和对应的 getter 和 setter |

|名称|全称|作用|
|---|---|---|
|POJO|Plain Old Java Object|普通 Java 对象，宽泛的概念|
|Entity|Entity|实体对象，通常对应数据库实体|
|PO|Persistent Object|持久化对象，通常对应数据库表|
|DO|Data Object|数据对象，通常表示数据库数据|
|DTO|Data Transfer Object|数据传输对象，用于跨层或跨服务传递数据|
|VO|View Object|视图对象，用于组织返回给前端的数据|
|BO|Business Object|业务对象，封装业务处理需要的数据|
|DAO|Data Access Object|数据访问对象，负责访问数据库|
|Query|Query Object|查询条件对象，封装筛选、分页等参数|
|Request|Request Object|请求对象，用于接收客户端请求|
|Response|Response Object|响应对象，用于组织接口响应|

其中，Entity、DTO、VO、POJO、Request、Response 是你当前最值得掌握的

ORM（Object-Relational Mapping，对象关系映射）

- 作用：建立 Java 对象与关系型数据库之间的映射关系，减少手动转换数据的工作。
- 映射关系：表 ↔ 类、行 ↔ 对象、列 ↔ 属性。
- 主要能力：对象与数据库记录转换、持久化操作、关联关系映射。
- 常见框架：Hibernate、MyBatis、MyBatis-Plus。
- 区别：Hibernate 通常自动生成 SQL；MyBatis 主要由开发者编写 SQL，框架完成参数绑定和结果映射。
