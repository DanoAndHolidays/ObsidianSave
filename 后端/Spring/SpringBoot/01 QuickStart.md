# 01 QuickStart
> Last Format Time：9/12/2026 23:49:51

[Spring 官方快速入门](https://spring.io/quickstart/)

![[Pasted image 20260912171252.png]]

---
## Spring 与 Spring Boot
*已补充*

Spring Framework 提供 IoC 容器、依赖注入、事务和 Web 等基础能力；Spring Boot 在 Spring 之上提供自动配置、Starter 依赖组合和应用启动支持，减少项目搭建时的重复配置。

从前端视角看，Controller 类似 API 路由处理函数，Service 类似业务服务模块。Maven 负责构建和依赖管理，Spring Boot 负责应用的配置与运行，两者职责不同。

---
## 创建项目
*已补充*

在 [Spring Initializr](https://start.spring.io/) 中选择 Maven、Java、Jar，以及 Spring Web 依赖。Group 可填 `com.example`，Artifact 填 `demo`，Package name 使用 `com.example.demo`。下载后解压，用 IDE 打开包含 `pom.xml` 的目录。

- 选择正式发布版本；`M1`、`RC` 表示预发布阶段，`SNAPSHOT` 表示开发快照。
- JDK 与 Java 配置保持一致，例如选择 Java 21；如果沿用本地 JDK 25，要核对所选 Boot 版本的兼容范围。
- 保留 Initializr 生成的父 POM、Starter 和插件配置；不同 Boot 大版本的依赖拆分可能不同，不要混抄多个版本的 POM。
- 在项目根目录执行 `java -version` 和 `.\mvnw.cmd -v`，确认终端和 Maven 使用的 JDK。

版本要求以所选版本的 [Spring Boot System Requirements](https://docs.spring.io/spring-boot/system-requirements.html) 为准。

本次示例使用 Boot `4.1.1` 完成构建验证。若生成的 POM 报 `Non-resolvable parent POM`，先核对父 POM 的实际发布版本；例如 `4.1.1` 与 `4.1.1.RELEASE` 是不同坐标，不能随意追加后缀。*已补充*

### 目录结构
*已补充*

```text
demo/
├── pom.xml
├── mvnw
├── mvnw.cmd
├── .mvn/wrapper/
└── src/
    ├── main/
    │   ├── java/com/example/demo/
    │   │   ├── DemoApplication.java
    │   │   └── controller/HelloController.java
    │   └── resources/application.properties
    └── test/java/com/example/demo/
```

启动类放在 `com.example.demo`，业务类放在它的子包中，便于默认组件扫描发现它们。`resources` 放配置和类路径资源；测试代码放在 `src/test/java`。

---
## 第一个 HTTP 接口
*已补充*

启动类 `src/main/java/com/example/demo/DemoApplication.java`：
```java
package com.example.demo;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class DemoApplication {
    public static void main(String[] args) {
        SpringApplication.run(DemoApplication.class, args);
    }
}
```

控制器 `src/main/java/com/example/demo/controller/HelloController.java`：
```java
package com.example.demo.controller;

import java.util.Map;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class HelloController {
    @GetMapping("/api/hello")
    public Map<String, String> hello(
            @RequestParam(name = "name", defaultValue = "World") String name) {
        return Map.of("message", "Hello, " + name + "!");
    }
}
```

- `@SpringBootApplication` 组合了 Boot 配置、自动配置和组件扫描能力。
- `@RestController` 将控制器方法的返回值写入响应体；在生成的 Web 项目中，上面的 Map 会被转换为 JSON。
- `@GetMapping` 处理指定路径的 GET 请求。
- `@RequestParam` 读取查询参数，例如 `?name=Dano`；这里显式写参数名，不依赖编译器保留方法参数名。

接口与消息转换规则见 [Servlet Web Applications](https://docs.spring.io/spring-boot/reference/web/servlet.html)。

### 启动与验证
*已补充*

在包含 `pom.xml` 的目录打开 PowerShell：
```powershell
.\mvnw.cmd spring-boot:run
```

macOS / Linux 对应 `./mvnw spring-boot:run`。首次执行 Wrapper 可能下载 Maven 和依赖。启动成功后另开终端：
```powershell
Invoke-RestMethod 'http://localhost:8080/api/hello?name=Dano'
```

原始 JSON 响应应为：
```json
{"message":"Hello, Dano!"}
```

PowerShell 会把 JSON 转成对象显示。浏览器也可以直接访问上述 URL；不传 `name` 时返回 `Hello, World!`。用 `Ctrl+C` 停止开发进程。

### 配置与打包
*已补充*

如需改端口，在 `src/main/resources/application.properties` 中写入以下内容，并将访问地址改为 8081：
```text
server.port=8081
```

在保留 Initializr 生成的 Boot Maven 插件配置时，可以打包为可执行 JAR：
```powershell
.\mvnw.cmd clean package
java -jar .\target\demo-0.0.1-SNAPSHOT.jar
```

JAR 文件名以 `target` 中实际产物为准。普通 Maven JAR 不一定能直接用 `java -jar` 启动；这里依靠 Boot 插件的重新打包能力。参见 [Boot Maven Plugin](https://docs.spring.io/spring-boot/maven-plugin/using.html)。

---
## 三层架构
*已修改*

| 层 | 主要职责 | 常用标记 |
|---|---|---|
| Controller | 接收 HTTP 参数、调用业务服务、组织响应 | `@RestController` |
| Service | 实现业务规则、协调多个数据操作，通常也是事务边界 | `@Service` |
| DAO / Repository | 访问和持久化数据，隔离具体存储方式 | `@Repository` 或持久层框架提供的注册方式 |

DAO 是 Data Access Object。MyBatis 的 Mapper、Spring Data 的 Repository 有各自的注册机制，不能认为给任意接口加 `@Repository` 就会自动生成数据库实现。

```text
浏览器 fetch / Axios
  → HTTP 请求
  → Controller
  → Service
  → DAO / Repository
  → MySQL
  → 结果逐层返回，Controller 输出 HTTP 响应
```

这里的 Hello 接口只用于验证 Web 环境，不需要为了返回一句话强行拆三层。出现查询、校验或多步骤业务时再分层，层之间通过构造方法注入依赖。

---
## 参数与联调排查
*已补充*

| 前端传参位置 | Spring MVC 常用读取方式 | 示例 |
|---|---|---|
| 查询字符串 | `@RequestParam` | `/users?page=1` |
| URL 路径 | `@PathVariable` | `/users/42` |
| JSON 请求体 | `@RequestBody` | POST JSON，并设置 `Content-Type: application/json` |

| 现象 | 优先检查 |
|---|---|
| 无法连接 | 应用是否启动，主机与端口是否一致 |
| 404 | URL、类级路径前缀，以及 Controller 是否在扫描范围 |
| 405 | GET / POST 等请求方法是否与映射一致 |
| 400 | 必填参数、类型转换或 JSON 格式 |
| 415 | `Content-Type` 与服务端支持的请求格式 |
| 500 | 后端异常日志及根因，不能只看前端报错 |
| 命令行可调用，浏览器跨域失败 | 浏览器同源策略，以及开发代理或后端 CORS 配置 |

开发服务器的端口（例如 5173）和 Boot 的 8080 不同，属于不同源。可以配置前端开发代理，或按实际允许的源配置后端 CORS。相关机制见 [Spring MVC CORS](https://docs.spring.io/spring-framework/reference/web/webmvc-cors.html)。
