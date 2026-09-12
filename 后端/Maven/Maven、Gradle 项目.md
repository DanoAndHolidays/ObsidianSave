# Maven、Gradle 项目
> Last Format Time：9/12/2026 23:49:51

Maven / Gradle 项目，本质上就是使用 Maven 或 Gradle 管理构建与依赖的项目。在这里讨论的是 Java 项目；构建工具不会发明一种新的 Java 语言。*已修改*

---
## 从前端工具理解
*已修改*

```text
前端：包管理器 + package.json + 构建工具 / scripts
Java：Maven + pom.xml
      Gradle + build.gradle 或 build.gradle.kts
```

这个类比用于理解职责，不代表命令一一对应。Maven / Gradle 可以统筹依赖解析、编译、测试、打包和发布；前端通常由 npm / pnpm 与 Vite 等工具协作完成。

| 前端经验 | Java 工程中的相近概念 | 区别 |
|---|---|---|
| `package.json` | `pom.xml`、Gradle 构建脚本 | POM 还描述坐标、生命周期插件与模块 |
| 包名与版本 | `groupId:artifactId:version` | Java 依赖常用三段坐标 |
| `node_modules` 与包缓存 | 构建 classpath 与本地仓库缓存 | JAR 通常不复制到项目内的 `node_modules` 式目录 |
| `npm run build` | `mvn package`、Gradle `build` | 测试、检查是否执行取决于工具及配置 |
| workspace | 多模块 / 多项目构建 | 模块聚合不等于声明模块之间的依赖 |

---
## 为什么需要构建工具
*已修改*

一个 Spring Boot 项目可能需要 Web、MySQL 驱动、测试框架和 JSON 处理库。手工管理 JAR 不仅要下载文件，还要处理传递依赖、版本冲突，以及编译、测试、运行时各自的 classpath。

构建文件把这些要求写成可复用配置。IDE 能读取配置，但构建规则不应只存在于某个开发者的 IDE 设置中。

例如 Maven 的一个依赖声明片段：
```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-web</artifactId>
</dependency>
```

这段省略版本的写法要求父 POM 或 BOM 已提供版本管理。它用于解释语法；具体 Web Starter 名称以所选 Boot 版本生成的项目为准。构建工具在解析项目依赖时下载需要的构件，单独把片段写进一个空 XML 文件还不构成可用工程。*已纠正*

参见 [Maven 依赖机制](https://maven.apache.org/guides/introduction/introduction-to-dependency-mechanism.html)。

---
## Maven 项目
*已修改*

识别入口是 `pom.xml`。典型目录如下：
```text
my-project/
├── pom.xml
├── mvnw、mvnw.cmd、.mvn/wrapper/   ← 使用 Wrapper 时存在
└── src/
    ├── main/
    │   ├── java/
    │   └── resources/
    └── test/
        ├── java/
        └── resources/
```

| 命令 | 含义 |
|---|---|
| `mvn compile` | 编译 |
| `mvn test` | 执行测试阶段及前置阶段 |
| `mvn package` | 打包，通常先编译和测试 |
| `mvn verify` | 继续完成已绑定的验证任务 |

通常产物在 `target` 下，格式由 packaging 和插件决定。普通 JAR、包含依赖的可执行 JAR、WAR 的用途不同，不能看到 `.jar` 就断定 `java -jar` 一定能运行。生命周期与插件关系见 [Maven Build Lifecycle](https://maven.apache.org/guides/introduction/introduction-to-the-lifecycle.html)。

---
## Gradle 项目
*已修改*

Gradle 使用任务及任务之间的依赖关系组织构建。常见文件为 `build.gradle`（Groovy DSL）或 `build.gradle.kts`（Kotlin DSL），项目设置通常位于 `settings.gradle` 或 `settings.gradle.kts`。

下面是一个独立的 Groovy DSL `build.gradle` 示例；代码块以纯文本展示：
```text
plugins {
    id 'java'
}

repositories {
    mavenCentral()
}

java {
    toolchain {
        languageVersion = JavaLanguageVersion.of(21)
    }
}
```

源码同样可放在 `src/main/java`。此示例要求能找到 JDK 21；未配置工具链下载仓库时，不能假定 Gradle 会自动下载缺失的 JDK。

在已有项目中优先使用随仓库提供的 Wrapper。PowerShell：
```powershell
.\gradlew.bat tasks
.\gradlew.bat build
```

macOS / Linux：
```bash
./gradlew tasks
./gradlew build
```

应用 Java 插件后，`build` 会依赖组装和检查任务，产物通常位于 `build/libs`。若项目没有 Wrapper，上述命令就不存在，需要先安装兼容的 Gradle 并生成 Wrapper。

原笔记里不带版本的 `implementation` / `testImplementation` 片段也有前提：依赖必须显式写版本，或由 platform / BOM 等管理。例如普通写法是 `implementation 'group:artifact:version'`，这里三个名称是语法占位符，不能直接执行。*已纠正*

参见 [Java Plugin](https://docs.gradle.org/current/userguide/java_plugin.html)、[声明依赖](https://docs.gradle.org/current/userguide/declaring_dependencies_basics.html) 和 [Gradle Wrapper](https://docs.gradle.org/current/userguide/gradle_wrapper.html)。

---
## Maven 与 Gradle 对比
*已修改*

| 维度 | Maven | Gradle |
|---|---|---|
| 配置文件 | `pom.xml` | `build.gradle` / `build.gradle.kts` |
| 配置形式 | XML 项目模型 | Groovy / Kotlin DSL |
| 构建组织 | 生命周期阶段绑定插件目标 | 任务与任务依赖图 |
| 常见输出目录 | `target` | `build` |
| Windows Wrapper | `.\mvnw.cmd` | `.\gradlew.bat` |
| 常见使用场景 | Java 服务与库 | Java 服务与库、Android 等 |

两者都能扩展。不能仅凭“Gradle 灵活”就判断所有项目都应换工具，也不能只看命令长度判断构建速度。已有项目先遵循仓库配置；当前在学习 Maven 的生命周期和 POM，可沿 Maven 完成第一条 Spring Boot 开发链路，再对照学习 Gradle。

---
## Project、Module、Package 与 Class
*已纠正*

这些术语要区分 IDE 视角与构建工具视角。IDEA 的 Project 是工作空间，IDE Module 是代码和配置单元；Maven 子模块是拥有自己 POM 的构建项目。它们经常有关联，但不是任何 IDE Module 都自动成为 Maven 模块。

```text
shop-project/
├── pom.xml                       ← packaging=pom，列出 modules
├── shop-user/
│   ├── pom.xml                   ← 独立模块坐标与依赖
│   └── src/main/java/com/example/user/User.java
└── shop-order/
    ├── pom.xml
    └── src/main/java/com/example/order/Order.java
```

- Project：这里的整体工程 `shop-project`。
- Maven Module：`shop-user`、`shop-order`，都有自己的 `pom.xml`。
- Package：例如 `com.example.user`，对应 Java 命名空间。
- Class：例如 `User`，对应具体 Java 类型。

根 POM 的 `<modules>` 负责聚合构建，子 POM 的 `<parent>` 负责继承。`shop-order` 要使用 `shop-user` 的类，仍须在依赖中声明它。Maven Reactor 再按实际依赖关系安排构建顺序。Gradle 则通常在 settings 中 `include` 子项目，并通过项目依赖连接它们。

参见 [Maven 多模块](https://maven.apache.org/guides/mini/guide-multiple-modules.html) 与 [Gradle Multi-Project Builds](https://docs.gradle.org/current/userguide/multi_project_builds.html)。

---
## 打开陌生项目时的检查顺序
*已补充*

1. 阅读 README，确认 JDK 和构建工具要求。
2. 找根 POM 或 Gradle settings，确认是否为多模块项目。
3. 优先用 Wrapper 的版本命令检查实际环境。
4. Maven 先执行 `verify`；Gradle Java 项目执行 `build`，读第一处失败及其根因。
5. 需要运行 Spring Boot 时，再使用项目的 `spring-boot:run`、`bootRun` 或可执行产物。

Wrapper 固定构建工具版本，不等于固定全部依赖，更不等于前端的 lockfile；JDK、依赖版本与仓库配置仍要分别管理。
