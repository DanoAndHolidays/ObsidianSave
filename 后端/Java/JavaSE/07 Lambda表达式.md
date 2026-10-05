# 07 Lambda表达式
> Last Format Time：9/9/2026 11:45:07

---
## 学习目标
*已补充* Lambda 表达式不是“没有名字的方法”，而是一种把**行为作为值传递**的语法。学完本篇应能够：

- 理解接口、实现类、匿名内部类与 Lambda 的关系；
- 判断一个接口是否是函数式接口；
- 正确编写表达式 Lambda、语句块 Lambda 和方法引用；
- 理解参数类型推断、返回值、变量捕获与“有效 final”；
- 熟练使用 `Predicate`、`Consumer`、`Function`、`Supplier`、`UnaryOperator`、`BinaryOperator` 等函数式接口；
- 能读懂集合排序、过滤、映射和线程任务中的 Lambda 代码。

---
## 从接口实现到 Lambda
### 传统的实现方法
*已修改* 假设系统要发送不同类型的消息。首先定义一个接口，接口只描述“能够发送消息”这一能力：

```java
package org.albert;

public interface Message {
    void send();
}
```

然后分别创建邮件和短信实现类：

```java
package org.albert;

public class Email implements Message {
    private String email;

    public Email(String email) {
        this.email = email;
    }

    @Override
    public void send() {
        System.out.println("发送邮件到：" + email);
    }
}
```

```java
package org.albert;

public class Sms implements Message {
    private String phoneNumber;

    public Sms(String phoneNumber) {
        this.phoneNumber = phoneNumber;
    }

    @Override
    public void send() {
        System.out.println("发送短信到：" + phoneNumber);
    }
}
```

调用时，可以通过接口类型接收不同的实现对象：

```java
package org.albert;

public class Main {
    public static void main(String[] args) {
        Message email = new Email("alice@example.com");
        sendMessage(email);

        Message sms = new Sms("13800000000");
        sendMessage(sms);
    }

    static void sendMessage(Message message) {
        message.send();
    }
}
```

这种写法体现了**面向接口编程和多态**，但如果某个行为只使用一次，为了实现一个简单的 `send()` 方法而专门创建 `Email`、`Sms` 等类，代码可能比较冗长。

### 匿名内部类
*已补充* 在 Lambda 出现以前，可以使用匿名内部类临时实现接口：

```java
Message message = new Message() {
    @Override
    public void send() {
        System.out.println("发送一次性消息");
    }
};

sendMessage(message);
```

匿名内部类仍然会创建一个实现对象，只是省略了具名类。它适合需要多个方法、额外字段，或需要在类体中写较复杂逻辑的场景。

### Lambda 表达式
*已修改* 当目标类型是只有一个抽象方法的函数式接口时，可以直接用 Lambda 提供该方法的实现：

```java
public class Main {
    public static void main(String[] args) {
        sendMessage(() -> System.out.println("发送一封邮件"));
    }

    static void sendMessage(Message message) {
        message.send();
    }
}
```

这里的 `() -> System.out.println("发送一封邮件")` 是一个 Lambda 表达式：

- `()`：抽象方法的参数列表；
- `->`：把参数列表和方法体分隔开；
- `System.out.println(...)`：方法体；
- `Message`：由 `sendMessage` 参数的目标类型推断出来的函数式接口类型。

*已纠正* Lambda 不是独立的“函数类型”，也不能脱离目标类型单独存在。它必须被赋值给函数式接口变量、作为函数式接口参数传入，或在具有目标类型的上下文中使用。

---
## 函数式接口
### 定义
函数式接口（functional interface）是**恰好有一个抽象方法**的接口。它可以拥有：

- 一个抽象方法；
- 任意数量的 `default` 方法和 `static` 方法；
- 从 `Object` 继承而来的、与 `Object` 方法签名匹配的方法不计入抽象方法数量。

推荐使用 `@FunctionalInterface` 进行约束：

```java
@FunctionalInterface
public interface Message {
    void send();
}
```

如果以后误加了第二个抽象方法，编译器会立即报错，而不是等到 Lambda 使用处才发现问题。

### 带参数和返回值的函数式接口
函数式接口的抽象方法可以有参数和返回值：

```java
@FunctionalInterface
interface Formatter {
    String format(String text);
}

Formatter formatter = text -> text.trim().toUpperCase();
String result = formatter.format(" java ");
System.out.println(result); // JAVA
```

多参数 Lambda：

```java
@FunctionalInterface
interface Calculator {
    int calculate(int left, int right);
}

Calculator add = (left, right) -> left + right;
Calculator max = (left, right) -> Math.max(left, right);
```

*已补充* Lambda 参数通常可以省略类型，让编译器根据目标接口推断：

```java
Calculator add = (left, right) -> left + right;
```

也可以显式写出所有参数类型，但不能只写一部分：

```java
Calculator add = (int left, int right) -> left + right;
```

### 表达式体与语句块体
单个表达式可以省略大括号和 `return`：

```java
Function<String, Integer> length = text -> text.length();
```

需要多条语句时使用语句块；有返回值时必须显式 `return`：

```java
Function<String, Integer> length = text -> {
    String normalized = text.trim();
    return normalized.length();
};
```

`void` 返回的 Lambda 可以写成表达式体：

```java
Consumer<String> printer = text -> System.out.println(text);
```

也可以写成语句块：

```java
Consumer<String> printer = text -> {
    String normalized = text.trim();
    System.out.println(normalized);
};
```

---
## Java 内置函数式接口
*已补充* `java.util.function` 包提供了常用函数式接口，实际开发中优先复用它们，而不是为每一种简单行为重复定义接口。

| 接口 | 抽象方法 | 用途 | 示例 |
| --- | --- | --- | --- |
| `Predicate<T>` | `boolean test(T)` | 判断条件 | `text -> text.length() > 3` |
| `Consumer<T>` | `void accept(T)` | 消费一个值，不返回结果 | `System.out::println` |
| `Function<T, R>` | `R apply(T)` | 输入一个值，转换为另一个值 | `String::length` |
| `Supplier<T>` | `T get()` | 不接收参数，提供一个值 | `UUID::randomUUID` |
| `UnaryOperator<T>` | `T apply(T)` | 同类型的一元转换 | `value -> value * 2` |
| `BinaryOperator<T>` | `T apply(T, T)` | 两个同类型值合并 | `Integer::sum` |

示例：

```java
Predicate<String> nonBlank = text -> text != null && !text.isBlank();
Consumer<String> log = text -> System.out.println("日志：" + text);
Function<String, Integer> toLength = String::length;
Supplier<String> defaultName = () -> "anonymous";
UnaryOperator<String> normalize = String::trim;
BinaryOperator<Integer> sum = Integer::sum;
```

基本类型专用接口可以减少装箱拆箱：

- `IntPredicate`、`LongPredicate`、`DoublePredicate`；
- `IntConsumer`、`LongConsumer`、`DoubleConsumer`；
- `IntFunction<R>`、`ToIntFunction<T>` 等；
- `IntSupplier`、`LongSupplier`、`DoubleSupplier`。

---
## Lambda 与集合处理
*已补充* Lambda 最常见的使用场景是集合遍历、排序和数据转换：

```java
List<String> names = new ArrayList<>(List.of("Tom", "Alice", "Bob"));

names.forEach(name -> System.out.println(name));
names.sort((left, right) -> left.length() - right.length());

List<String> longNames = names.stream()
        .filter(name -> name.length() >= 4)
        .map(String::toUpperCase)
        .toList();
```

更推荐使用比较器组合方法表达排序意图，避免手写减法比较器在极端整数值下溢出：

```java
names.sort(Comparator.comparingInt(String::length)
        .thenComparing(Comparator.naturalOrder()));
```

集合和 Stream 的完整操作见 [[09 单列集合]] 以及后续的 Stream 专题笔记。

---
## 方法引用
*已补充* 方法引用是 Lambda 的简写形式，前提是方法签名与目标函数式接口的抽象方法兼容。

```java
Consumer<String> printer = System.out::println;
Function<String, Integer> length = String::length;
BinaryOperator<Integer> max = Math::max;
Supplier<List<String>> listFactory = ArrayList::new;
```

常见形式：

| 形式 | 示例 | 含义 |
| --- | --- | --- |
| 静态方法引用 | `Math::max` | 引用类的静态方法 |
| 特定对象的实例方法引用 | `System.out::println` | 引用某个对象的方法 |
| 任意对象的实例方法引用 | `String::trim` | 第一个参数作为调用对象 |
| 构造方法引用 | `ArrayList::new` | 调用构造方法创建对象 |

如果方法引用不够直观，可以退回 Lambda；可读性优先于追求语法最短。

---
## 变量捕获与有效 final
Lambda 可以读取所在作用域的局部变量，但局部变量必须是 `final` 或**有效 final（effectively final）**：声明后没有再次赋值。

```java
String prefix = "Java: ";
Consumer<String> printer = text -> System.out.println(prefix + text);
```

下面的代码不能编译，因为 `prefix` 在 Lambda 创建后被重新赋值：

```java
String prefix = "Java: ";
prefix = "JDK: ";
Consumer<String> printer = text -> System.out.println(prefix + text);
```

*已补充* 局部变量捕获的是值的使用关系，不等于可以安全共享可变状态。对象引用本身可以是有效 final，但对象内部仍可能被修改，因此并发代码中要注意线程安全：

```java
List<String> result = new ArrayList<>();
Consumer<String> add = result::add;
```

此外，Lambda 中的 `this` 指向**外层对象**，不像匿名内部类那样引入一个新的 `this` 作用域。

---
## Lambda 的类型推断与限制
### 必须有目标类型
下面的写法没有足够的上下文，无法独立推断 Lambda 类型：

```java
// var task = () -> System.out.println("run"); // 无法编译
```

应提供目标类型：

```java
Runnable task = () -> System.out.println("run");
var action = (Runnable) () -> System.out.println("run");
```

### 不能重载到无法区分的函数式接口
如果两个重载方法的函数式接口形状相同，Lambda 可能无法确定调用哪一个：

```java
void run(Consumer<String> consumer) {}
void run(Function<String, String> function) {}

// run(text -> text.trim()); // 可能产生重载歧义
```

可以显式转换目标类型：

```java
run((Function<String, String>) text -> text.trim());
```

*已补充* 在公共 API 中，不要设计仅靠 Lambda 返回值或参数形式就容易产生歧义的重载；必要时使用不同方法名、显式类型或专用接口。

### 检查异常
标准 `java.util.function` 接口的方法通常不声明受检异常。调用会抛出受检异常的方法时，不能直接把它作为普通 Lambda 使用：

```java
// Files.readString(path) 可能抛出 IOException
// Function<Path, String> read = Files::readString; // 无法直接编译
```

可以在 Lambda 内处理异常，或定义一个声明异常的自定义函数式接口：

```java
@FunctionalInterface
interface ThrowingFunction<T, R> {
    R apply(T value) throws Exception;
}
```

不要为了省事把所有异常包装成毫无上下文的 `RuntimeException`；应保留原始异常作为 cause，并在合适的边界统一处理。

---
## Lambda、匿名内部类与普通方法的选择
| 场景 | 推荐方式 |
| --- | --- |
| 一次性、短小的单行为 | Lambda |
| 需要复用的业务规则 | 具名方法或具名类 |
| 需要多个方法、字段或复杂生命周期 | 普通类或匿名内部类 |
| 需要表达策略且策略可替换 | 函数式接口 + Lambda |
| 逻辑超过几行、嵌套过深 | 拆成具名方法 |

*已补充* Lambda 应该表达清晰的行为，而不是把完整业务流程压缩到一行。遇到复杂校验、异常处理、日志和分支逻辑时，优先提取为有意义的方法名。

---
## 常见错误
1. **把任意接口都传给 Lambda**：接口必须只有一个抽象方法。
2. **忘记目标类型**：Lambda 需要由赋值、参数、返回值或显式转换提供上下文。
3. **块体漏写 `return`**：多语句且有返回值时必须显式返回。
4. **混用参数类型写法**：参数要么全部省略类型，要么全部显式写出。
5. **修改被捕获的局部变量**：局部变量必须是 final 或有效 final。
6. **用减法实现比较器**：可能整数溢出，应使用 `Comparator.comparingInt` 或 `Integer.compare`。
7. **滥用嵌套 Lambda**：可读性差时应拆分方法或引入领域对象。
8. **误以为 Lambda 自动异步**：Lambda 只是行为表示，是否异步取决于 `Thread`、线程池、`CompletableFuture` 等执行机制。

---
## 实战练习
### 练习一：消息发送策略
定义 `Message` 函数式接口，并编写一个 `sendMessage(Message message)` 方法，分别使用 Lambda 输出邮件、短信和站内信。

### 练习二：集合转换
给定一组用户名，完成以下操作：

1. 去除空白和空字符串；
2. 按忽略大小写排序；
3. 转换为大写；
4. 收集为不可变列表。

### 练习三：自定义函数式接口
定义一个 `ThrowingFunction<T, R>`，编写一个工具方法，将受检异常转换为统一的业务异常，同时保留原始异常 cause。

---
## 核心记忆
- Lambda 是函数式接口抽象方法的实现，不是独立的函数类型。
- 函数式接口只有一个抽象方法，可以使用 `@FunctionalInterface` 让编译器帮忙检查。
- `()`、`(x)`、`(x, y)` 对应参数列表；表达式体可以省略 `return`，语句块体不能。
- Lambda 的类型依赖目标类型；方法引用是兼容时的简写。
- 捕获的局部变量必须是 `final` 或有效 final。
- 优先使用 `java.util.function` 中的标准接口，并在可读性下降时提取具名方法。
