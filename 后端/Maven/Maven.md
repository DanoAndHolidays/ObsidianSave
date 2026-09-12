# Maven
> Last Format Time：9/12/2026 23:49:51

![[Pasted image 20260912012926.png]]

---
## Maven 管什么
*已补充*

Maven 通过 `pom.xml` 描述项目坐标、依赖、插件和模块，按生命周期编译、测试、打包。它会从仓库解析依赖，而不是要求开发者手动维护一堆 JAR。

| 位置 | 用途 |
|---|---|
| `pom.xml` | 当前项目的构建模型 |
| `src/main/java` | 生产 Java 源码 |
| `src/main/resources` | 配置与类路径资源 |
| `src/test/java`、`src/test/resources` | 测试源码与测试资源 |
| `target` | 当前项目的构建产物 |
| 用户目录下 `.m2/repository` | 默认本地仓库，缓存下载和本地安装的构件 |
| 用户目录下 `.m2/settings.xml` | 用户级镜像、代理、仓库认证等配置 |

`target` 是项目输出目录，`.m2/repository` 是依赖仓库；`clean` 通常清理前者，不会清空后者。配置入口见 [Maven Settings](https://maven.apache.org/settings.html)。

---
## 生命周期
![[Pasted image 20260912154720.png]]

Maven 有 `clean`、`default`、`site` 三套内置生命周期。在**同一套**生命周期中，指定后面的阶段，会先经过前面的阶段；因此 `mvn test` 包含编译，但不会自动执行另一套生命周期中的 `clean`。*已修改*

### 阶段与插件目标
*已补充*

```text
default 常用阶段（省略中间阶段）：
validate → compile → test → package → verify → install → deploy

clean 生命周期：pre-clean → clean → post-clean
site 生命周期：pre-site → site → post-site → site-deploy
```

| 命令 | 主要结果 |
|---|---|
| `mvn compile` | 编译生产源码 |
| `mvn test` | 编译并执行配置好的单元测试 |
| `mvn package` | 执行前置阶段并打包到 `target` |
| `mvn verify` | 继续执行已配置的集成测试验证、质量检查等 |
| `mvn install` | 将本项目构件放入本地仓库，供其他本地项目依赖 |
| `mvn deploy` | 将构件发布到配置的远程 Maven 仓库，不等于启动线上服务 |
| `mvn clean package` | 先清理，再经过 default 生命周期到 package |

阶段是流程位置，真正执行工作的是绑定的插件目标，例如 `compiler:compile`、`surefire:test`。`dependency:tree` 是直接调用插件目标，不是生命周期阶段。某阶段未绑定目标时没有对应工作；`verify` 也不会凭空生成集成测试配置。

![[Pasted image 20260912013523.png]]

参见 [Build Lifecycle](https://maven.apache.org/guides/introduction/introduction-to-the-lifecycle.html)。

---
## POM 项目对象模型
*已修改*

POM 是 Project Object Model。常用坐标是 `groupId:artifactId:version`；`modelVersion` 是 POM 模型版本，不是项目版本或本机 Maven 版本。

原例的 `JavaWeb` 使用 `packaging=pom` 并包含 `MavenTest`，属于聚合项目。下面补成一组配套的根 POM 与子模块 POM，保留这个结构：
```text
JavaWeb/
├── pom.xml
└── MavenTest/
    ├── pom.xml
    └── src/main/java/org/example/App.java
```

### 根 POM
*已纠正*

根目录 `JavaWeb/pom.xml`：
```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>
    <groupId>org.example</groupId>
    <artifactId>JavaWeb</artifactId>
    <version>1.0-SNAPSHOT</version>
    <packaging>pom</packaging>

    <modules>
        <module>MavenTest</module>
    </modules>

    <properties>
        <maven.compiler.release>21</maven.compiler.release>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
    </properties>

    <build>
        <plugins>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-compiler-plugin</artifactId>
                <version>3.16.0</version>
            </plugin>
        </plugins>
    </build>
</project>
```

这里把原例的 `source/target=25` 改成教学基线 `release=21`：用支持该目标的 JDK（例如 JDK 21 或 25）编译，同时约束语言、字节码和 Java SE API。`source/target` 本身不会阻止误用较新 JDK API。项目确实需要 Java 25 特性时，再把目标改成 25 并统一开发与运行环境。参见 [Compiler Plugin --release](https://maven.apache.org/plugins/maven-compiler-plugin/examples/set-compiler-release.html)。

### 子模块 POM 与源码
*已补充*

`JavaWeb/MavenTest/pom.xml`：
```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>
    <parent>
        <groupId>org.example</groupId>
        <artifactId>JavaWeb</artifactId>
        <version>1.0-SNAPSHOT</version>
        <relativePath>../pom.xml</relativePath>
    </parent>
    <artifactId>MavenTest</artifactId>
    <packaging>jar</packaging>
</project>
```

`JavaWeb/MavenTest/src/main/java/org/example/App.java`：
```java
package org.example;

public class App {
    public static void main(String[] args) {
        System.out.println("Maven is ready");
    }
}
```

在 `JavaWeb` 根目录运行：
```powershell
mvn clean package
java -cp .\MavenTest\target\MavenTest-1.0-SNAPSHOT.jar org.example.App
```

预期打印 `Maven is ready`。此普通 JAR 未配置主类清单，示例显式通过 classpath 与主类启动。

`<modules>` 表达聚合关系，决定一起构建哪些项目；子 POM 的 `<parent>` 表达继承关系。只在根 POM 列出模块，不会自动让子模块继承其配置，也不会自动建立兄弟模块间的代码依赖。参见 [Introduction to the POM](https://maven.apache.org/guides/introduction/introduction-to-the-pom.html)。

---
## 项目依赖
*已修改*

下面把原笔记的 Commons IO 示例版本更新为本次核对到的正式版 `2.22.0`，坐标见 [Commons IO 官方文档](https://commons.apache.org/proper/commons-io/dependency-info.html)。在子模块 POM 的 `<project>` 内添加：
```xml
<dependencies>
    <dependency>
        <groupId>commons-io</groupId>
        <artifactId>commons-io</artifactId>
        <version>2.22.0</version>
    </dependency>
</dependencies>
```

应用实际使用的依赖放在相应模块中。放在父 POM 的 `<dependencies>` 中可能让所有继承它的子模块都引入该依赖；只想统一版本时使用 `<dependencyManagement>`。

### 作用域与版本管理
*已补充*

| scope | 主代码编译 | 测试 | 运行时 classpath |
|---|---|---|---|
| `compile`（默认） | 有 | 有 | 有 |
| `provided` | 有 | 有 | 无，预期由容器等提供 |
| `runtime` | 无 | 有 | 有 |
| `test` | 无 | 有 | 无 |

此外，`import` 只用于 `dependencyManagement` 中导入 `type=pom` 的 BOM；`system` 依赖固定本地路径，可移植性差。

- `<dependencies>` 声明实际依赖。
- `<dependencyManagement>` 管理版本等默认值，本身不会引入所有列出的依赖。
- BOM 是集中管理一组依赖版本的 POM。
- 未直接指定版本且没有父 POM / BOM 提供版本时，普通依赖声明不完整。

### Spring Boot 测试依赖
*已纠正*

原例直接为 `spring-boot-starter-test` 指定 `4.2.0-M1`，这是里程碑预览版；不应脱离项目的 Boot 版本单独选择。以下片段只适用于**已经继承 Boot 父 POM或导入匹配 Boot BOM** 的项目，不要直接贴进上面的普通 Java 示例：
```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-test</artifactId>
    <scope>test</scope>
</dependency>
```

使用父 POM 时还能获得相应插件管理；仅导入 BOM 不等于导入构建插件配置。参见 [Boot Maven Plugin 的依赖管理说明](https://docs.spring.io/spring-boot/maven-plugin/using.html)。

### 传递依赖、冲突与排除
*已纠正*

项目依赖 A，A 又依赖 B，B 可能作为传递依赖进入项目。没有其他管理规则覆盖时，Maven 常按“路径较近优先，同深度先声明优先”选择冲突版本，并不是总选最新版。

原例排除 `io.airlift:airbase`，但未提供实际依赖树依据。排除项应写在**确实引入该传递依赖的直接依赖**下；只影响这条路径，其他路径仍可能引入同一构件。先检查再排除，避免凭空写坐标。

需要排除时，在已确认的直接依赖 `<dependency>` 内加入如下结构。这里的名称是占位符，要用依赖树里的真实坐标替换：
```text
<exclusions>
    <exclusion>
        <groupId>待排除依赖的 groupId</groupId>
        <artifactId>待排除依赖的 artifactId</artifactId>
    </exclusion>
</exclusions>
```

```powershell
mvn dependency:tree
mvn help:effective-pom
```

前者看实际依赖路径和版本，后者看父 POM、配置等合并后的有效模型。作用域、BOM、冲突和排除规则见 [Dependency Mechanism](https://maven.apache.org/guides/introduction/introduction-to-dependency-mechanism.html)。

---
## 常用操作与排错
*已补充*

| 命令 / 问题 | 用途 / 检查点 |
|---|---|
| `mvn -v` | 看 Maven 版本与实际使用的 JDK |
| `.\mvnw.cmd verify` | 项目有 Maven Wrapper 时，在 Windows 使用项目指定的 Maven |
| `mvn -pl MavenTest -am package` | 构建指定模块及本次 Reactor 中它需要的上游模块 |
| `mvn -U verify` | 强制检查缺失的 release 和更新的 snapshot，不是无条件重下所有依赖 |
| 找不到依赖 | 检查坐标、仓库、镜像、网络和认证配置 |
| `invalid target release` | Maven 使用的 JDK 不支持目标版本，先看 `mvn -v` |
| IDE 能编译，终端失败 | 比较 IDE Maven JDK、终端 JDK、profile 和 settings |
| 测试失败导致打包失败 | 阅读 `target/surefire-reports`，先修复失败原因 |

Maven 的 `install` 是安装**本项目构件**到本地仓库，与前端 `npm install` 下载项目依赖的含义不同。Wrapper 固定 Maven 版本，不负责把 JDK 也安装成正确版本。参见 [Maven Wrapper](https://maven.apache.org/tools/wrapper/) 与 [多模块构建](https://maven.apache.org/guides/mini/guide-multiple-modules.html)。
