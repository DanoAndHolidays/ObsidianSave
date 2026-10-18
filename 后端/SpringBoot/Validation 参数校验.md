`jakarta.validation.constraints` 是 Java 中专门用于**参数校验（Validation）** 的包，属于 Jakarta Bean Validation 规范。

简单来说，它可以通过注解的方式，检查用户传入的数据是否合法，避免我们手动编写大量的 `if` 判断。

例如，注册用户时要求：

- 用户名不能为空
    
- 密码至少 8 位
    
- 年龄必须大于等于 18 岁
    
- 邮箱格式必须正确
    

这些都可以通过这个包中的注解实现。

## 1. 常见的校验注解

|注解|作用|示例|
|---|---|---|
|`@NotNull`|不能为 `null`|`@NotNull`|
|`@NotEmpty`|不能为 `null` 或空|`@NotEmpty`|
|`@NotBlank`|字符串不能是空白内容|`@NotBlank`|
|`@Size`|限制字符串、集合等的大小|`@Size(min=2,max=20)`|
|`@Min`|数值不能小于指定值|`@Min(18)`|
|`@Max`|数值不能大于指定值|`@Max(100)`|
|`@Positive`|必须为正数|`@Positive`|
|`@Email`|校验邮箱格式|`@Email`|
|`@Pattern`|使用正则表达式校验|`@Pattern(regexp="...")`|
|`@Past`|必须是过去的日期|`@Past`|
|`@Future`|必须是未来的日期|`@Future`|

这些都是 Jakarta Validation 提供的标准约束注解。

![](https://www.google.com/s2/favicons?domain=https://jakarta.ee&sz=32)

jakarta.ee

### 特别注意：三个非空注解的区别

|输入值|`@NotNull`|`@NotEmpty`|`@NotBlank`|
|---|---|---|---|
|`null`|❌|❌|❌|
|`""`|✅|❌|❌|
|`" "`|✅|✅|❌|
|`"hello"`|✅|✅|✅|

其中 `@NotBlank` 主要用于字符串，而 `@NotEmpty` 还可以用于集合、数组等。

## 2. Spring Boot 中怎么使用？

假设我们有一个用户注册接口。

第一步：定义 DTO 并添加校验注解。

```
import jakarta.validation.constraints.*;

public record RegisterDTO(
    @NotBlank(message = "用户名不能为空")
    String username,

    @Size(min = 8, message = "密码至少8位")
    @NotBlank(message = "密码不能为空")
    String password,

    @NotNull(message = "年龄不能为空")
    @Min(value = 18, message = "年龄不能小于18岁")
    Integer age,

    @NotBlank(message = "邮箱不能为空")
    @Email(message = "邮箱格式不正确")
    String email
) {}
```

第二步：在 Controller 中使用 `@Valid` 激活校验。

```
import jakarta.validation.Valid;

@RestController
@RequestMapping("/users")
public class UserController {

    @PostMapping("/register")
    public String register(
        @Valid @RequestBody RegisterDTO dto
    ) {
        return "注册成功";
    }
}
```

例如前端传入：

```
{
  "username": "",
  "password": "123",
  "age": 16,
  "email": "hello"
}
```

校验不通过，Spring MVC 默认会返回 HTTP 400 错误，Controller 方法体不会正常执行。我们也可以通过全局异常处理器 `@RestControllerAdvice` 统一返回自定义错误信息。

## 3. `@Valid` 和 `@Validated` 有什么区别？

这两个注解经常一起出现在 Spring Boot 项目中。

||`@Valid`|`@Validated`|
|---|---|---|
|所属包|`jakarta.validation`|`org.springframework.validation.annotation`|
|来源|Jakarta 标准|Spring 框架|
|主要作用|触发对象校验、级联校验|触发校验、支持分组及 Spring 方法校验|
|校验分组|不能直接指定组|可以指定组|

通常：

- Controller 接收请求 DTO：使用 `@Valid`
    
- 需要校验分组：使用 `@Validated`
    
- Service 层方法参数校验：在 Spring Boot 3 常见配置下，可以在类上使用 `@Validated` 开启方法校验。
    
    ![](https://www.google.com/s2/favicons?domain=https://docs.spring.io&sz=32)
    
    Home
    

要注意，仅仅在字段上添加 `@NotBlank` 等注解，并不意味着任何场景都会自动执行校验，还需要对应的校验触发机制。

## 4. 需要安装什么依赖？

Spring Boot 项目通常需要引入：

```
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-validation</artifactId>
</dependency>
```

它通常会引入 Hibernate Validator 作为具体实现。

![](https://www.google.com/s2/favicons?domain=https://docs.spring.io&sz=32)

Home

这里可以理解成三个层次：

Jakarta Validation

定义校验规范、约束注解和接口

Hibernate Validator

实现校验规范，执行具体校验逻辑

Spring Boot

集成校验机制，自动触发并处理校验异常

另外，如果你看老教程，会发现：

```
// 老项目（Spring Boot 2.x）
import javax.validation.constraints.NotNull;

// 新项目（Spring Boot 3.x）
import jakarta.validation.constraints.NotNull;
```

这是 Jakarta EE 命名空间迁移造成的，作用基本相同。

## 5. 它属于什么知识体系？

建议放在你的后端笔记：

Java 后端 → Spring Boot → 参数校验（Bean Validation）

需要特别区分两种校验：

- 参数校验：`@NotNull`、`@Size` 等，检查请求数据是否合法。
    
- 数据库约束：`NOT NULL`、`UNIQUE`、`FOREIGN KEY` 等，维护数据库中的数据完整性。
    

一句话总结：`jakarta.validation.constraints` 提供声明式参数校验注解，让我们把校验规则直接写在 DTO 字段上，再由 Spring 和 Hibernate Validator 自动完成校验。