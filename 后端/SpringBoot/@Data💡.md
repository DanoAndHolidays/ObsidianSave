这两种写法都可以正常用于 Spring Boot 项目，但有两个重要区别：

1. `@NotNull` 和 `@NotBlank` 的校验规则不同。
    
2. Lombok 的 `@Data` 和手动编写 Getter/Setter 的行为并不完全相同。
    

我的建议：登录 DTO 使用 `@NotBlank`，同时可以使用 Lombok 简化代码，但不太建议直接使用 `@Data`。

下面详细解释。

## 一、`@NotNull` 和 `@NotBlank` 的区别

这是两种实现中最关键的区别。

|用户提交的值|`@NotNull`|`@NotBlank`|
|---|---|---|
|`null`|❌|❌|
|`""` 空字符串|✅|❌|
|`" "` 只有空格|✅|❌|
|`"admin"`|✅|✅|
|`" admin "`|✅|✅|

例如你的第一种写法：

```
@NotNull(message = "Password is required")
private String password;
```

如果前端传入：

```
{
  "identifier": "",
  "password": "   "
}
```

就算触发了 Bean Validation 校验，这两个字段也会通过 `@NotNull` 校验，因为它们都不是 `null`。

而第二种写法：

```
@NotBlank(message = "Password is required")
private String password;
```

会直接拒绝空字符串和纯空白字符。

因此，对于登录接口中的用户名和密码，`@NotBlank` 比 `@NotNull` 更合适。

不过要注意，`@NotBlank` 只负责检查内容是否包含非空白字符，不会自动去除前后空格，也不会检查账号是否真实存在。

## 二、Lombok `@Data` 和手写 Getter/Setter 的区别

你的第一种写法：

```
@Data
public class LoginCommand {
    private String identifier;
    private String password;
}
```

并不只是第二种写法的简化版本，因为 `@Data` 会自动生成更多方法。

根据 Lombok 官方文档，`@Data` 相当于组合了以下几个注解：

![](https://www.google.com/s2/favicons?domain=https://projectlombok.org&sz=32)

projectlombok.org

```
@Getter
@Setter
@ToString
@EqualsAndHashCode
@RequiredArgsConstructor
```

|功能|`@Data`|你手写的版本|
|---|---|---|
|Getter|✅|✅|
|Setter|✅|✅|
|无参构造函数|✅ 当前示例|✅|
|`toString()`|✅ 自动生成|继承 Object|
|`equals()`|✅ 按字段比较|继承 Object|
|`hashCode()`|✅ 按字段计算|继承 Object|
|代码简洁性|更简洁|比较冗长|

注意，`@Data` 并不保证在所有情况下都生成无参构造函数。它通过 `@RequiredArgsConstructor` 生成构造函数，当没有必需初始化的字段时，生成的就是无参构造函数。

### 为什么我不太推荐在 LoginCommand 上使用 `@Data`？

主要原因是密码泄露风险。

假设我们这样写：

```
LoginCommand command = new LoginCommand();
command.setIdentifier("admin");
command.setPassword("123456");

System.out.println(command);
```

使用 `@Data` 时，可能输出：

```
LoginCommand(identifier=admin, password=123456)
```

因为 Lombok 自动生成了 `toString()`，默认会包含 `password` 字段。

如果后端日志中出现：

```
log.info("Login request: {}", command);
```

就可能把用户的明文密码记录到日志中。

而你的第二种写法没有重写 `toString()`，默认只会输出类似：

```
LoginCommand@5f184fc6
```

所以，对于登录 DTO、支付 DTO 等包含敏感字段的对象，应特别注意自动生成的 `toString()`。

## 三、我推荐的最终写法

实际上，我们完全可以兼顾代码简洁、校验严格和安全性。

```
import jakarta.validation.constraints.NotBlank;
import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class LoginCommand {

    @NotBlank(message = "Username or email is required")
    private String identifier;

    @NotBlank(message = "Password is required")
    private String password;
}
```

这里我推荐使用 `@Getter` + `@Setter`，而不是 `@Data`。

原因很简单：

- `@NotBlank`：防止用户名和密码为空。
    
- `@Getter`：自动生成 Getter。
    
- `@Setter`：自动生成 Setter。
    
- 不生成包含密码的 `toString()`。
    
- 不额外生成不需要的 `equals()`、`hashCode()`。
    

这个类没有显式定义构造函数，所以 Java 会自动提供一个无参构造函数，能够满足常见的 Spring MVC 请求反序列化需求。

Controller 中记得使用 `@Valid`：

```
@PostMapping("/login")
public Result<?> login(
    @Valid @RequestBody LoginCommand command
) {
    return authService.login(command);
}
```

当然，如果项目中统一要求使用 `@Data`，也可以这样写：

```
@Data
public class LoginCommand {

    @NotBlank
    private String identifier;

    @NotBlank
    @ToString.Exclude
    private String password;
}
```

但这仅解决 `toString()` 包含密码的问题，并不意味着可以随意记录登录请求或敏感数据。

## 四、总结

|对比项|推荐方案|
|---|---|
|字符串必填校验|`@NotBlank`|
|普通对象简化代码|Lombok|
|登录 DTO|`@Getter` + `@Setter`|
|是否需要手写 Getter/Setter|通常不需要|
|是否推荐登录 DTO 使用 `@Data`|不优先推荐|
|是否需要手写无参构造函数|当前示例不需要|

另外补充一个容易混淆的地方： `lombok.NonNull` 和 `jakarta.validation.constraints.NotNull` 也不是一回事。前者主要通过生成空值检查保护特定方法、构造函数或 Setter 的调用，后者是 Bean Validation 约束，需要相应的校验机制触发。

所以你现在写 Spring Boot 项目时，可以养成一个习惯：DTO 根据需要选择 `@Getter`、`@Setter`；参数校验使用 Jakarta Validation；不要无差别地给所有 Java 类加 `@Data`。