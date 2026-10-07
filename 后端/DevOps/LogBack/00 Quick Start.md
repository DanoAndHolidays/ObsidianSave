# 00 Quick Start
> Last Format Time：9/30/2026 01:00:03

![[Pasted image 20260919164955.png]]

```java
@Slf4j
@RequestMapping("/depts")
@RestController
public class DeptController {
    //private static final Logger log = LoggerFactory.getLogger(DeptController.class);
    @Autowired
    private DeptService deptService;

    // 可以使用 @GetMapping("/depts") 代替
    // @RequestMapping(value = "/depts", method = RequestMethod.GET)
    @GetMapping
    public Result list() {
        //System.out.println("查询全出的部门数据");
        log.info("查询全出的部门数据");
        List<Dept> list = deptService.findAll();
        return Result.success(list);
    }

    @DeleteMapping
    public Result delete(Integer id, String name){
        log.info("delete部门数据: {}", id);
        //System.out.println(id + name);
        deptService.deleteById(id);
        return Result.success();
    }
    // ...
}
```

---
## 日志级别
![[Pasted image 20260919180237.png]]


---
## 配置文件
![[Pasted image 20260919174246.png]]

```xml
<?xml version="1.0" encoding="UTF-8"?>
<configuration>
    <!-- 日志文件存放目录（相对项目运行目录） -->
    <property name="LOG_HOME" value="logs"/>

    <!-- 控制台输出 -->
    <appender name="CONSOLE" class="ch.qos.logback.core.ConsoleAppender">
        <encoder class="ch.qos.logback.classic.encoder.PatternLayoutEncoder">

            <!--日志格式-->
            <pattern>%d{yyyy-MM-dd HH:mm:ss.SSS} [%thread] %-5level %logger{36} - %msg%n</pattern>
            <charset>UTF-8</charset>
        </encoder>
    </appender>

    <!-- 滚动文件输出：按天切割，单文件超过 10MB 再分片，保留 30 天 -->
    <appender name="FILE" class="ch.qos.logback.core.rolling.RollingFileAppender">
        <file>${LOG_HOME}/tlias.log</file>
        <rollingPolicy class="ch.qos.logback.core.rolling.SizeAndTimeBasedRollingPolicy">
            <fileNamePattern>${LOG_HOME}/tlias.%d{yyyy-MM-dd}.%i.log.gz</fileNamePattern>
            <maxFileSize>10MB</maxFileSize>
            <maxHistory>30</maxHistory>
            <totalSizeCap>1GB</totalSizeCap>
        </rollingPolicy>
        <encoder class="ch.qos.logback.classic.encoder.PatternLayoutEncoder">
            <pattern>%d{yyyy-MM-dd HH:mm:ss.SSS} [%thread] %-5level %logger{36} - %msg%n</pattern>
            <charset>UTF-8</charset>
        </encoder>
    </appender>

    <!-- 项目自身代码：debug 级别 -->
    <logger name="org.dano" level="debug"/>

    <!-- MyBatis Mapper 接口：debug 级别，输出 SQL 及参数 -->
    <logger name="org.dano.mapper" level="debug"/>

    <!-- 全局默认：info 级别 -->
    <root level="info">
        <appender-ref ref="CONSOLE"/>
        <appender-ref ref="FILE"/>
    </root>
</configuration>
```
