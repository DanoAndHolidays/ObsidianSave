# 03 Session 短信登录
> Last Format Time：10/6/2026 02:27:25

[[14 ThreadLocal]]

---
## 流程
![[Pasted image 20260929193441.png]]

### 发送验证码
用户在提交手机号后，会校验手机号是否合法，如果不合法，则要求用户重新输入手机号

如果手机号合法，后台此时生成对应的验证码，同时将验证码进行保存，然后再通过短信的方式将验证码发送给用户

```java
@Service
@Slf4j
```

这个 `HttpSession session` 不是自己 new 出来的，也不是前端直接传进来的，而是 Spring MVC 在处理 HTTP 请求时，从当前请求对应的 Servlet 环境里拿到并自动注入的

```java
public class UserServiceImpl extends ServiceImpl<UserMapper, User> implements IUserService {

    @Override
    public Result sendCode(String phone, HttpSession session) {
        if(RegexUtils.isPhoneInvalid(phone)) return Result.fail("手机号格式错误");

        String code = RandomUtil.randomNumbers(6);

        session.setAttribute("code", code);
```

这里会使用专用的服务来实现

```java
        //模拟发送
        log.info("发送验证码{}", code);

        return Result.ok();
    }
}
```

### 短信验证码登录、注册
用户将验证码和手机号进行输入，后台从session中拿到当前验证码，然后和用户输入的验证码进行校验，如果不一致，则无法通过校验，如果一致，则后台根据手机号查询用户，如果用户不存在，则为用户创建账号信息，保存到数据库，无论是否存在，都会将用户信息保存到session中，方便后续获得当前登录信息

```java
@Override
public Result login(LoginFormDTO loginForm, HttpSession session) {
    String phone = loginForm.getPhone();
    if(RegexUtils.isPhoneInvalid(phone)) return Result.fail("手机号格式错误");

    String cachedCode = session.getAttribute("code").toString();
    log.info("cachedCode, {}",cachedCode);
```

这里的字符串比较要使用 `equals` 因为这不是 js，字符串是引用类型的

```java
    if(cachedCode == null || !cachedCode.equals(loginForm.getCode())) return Result.fail("验证码错误");

    User user = query().eq("phone", phone).one();
    if(user == null) {
        user = createUserWithPhone(phone);
    }

    session.setAttribute("user", user);

    return Result.ok();
}

private User createUserWithPhone(String phone) {
    User user = new User();

    user.setPhone(phone);
    user.setNickName("user_" + RandomUtil.randomString(10));
    save(user);
    log.info(user.toString());
    return user;
}
```

### 校验登录状态
用户在请求时候，会从 cookie 中携带者 JsessionId 到后台，后台通过 JsessionId 从 session 中拿到用户信息，如果没有 session 信息，则进行拦截，如果有 session 信息，则将用户信息保存到 [[14 ThreadLocal]] 中，并且放行：
```java
@Slf4j
public class LoginInterceptor implements HandlerInterceptor {

    @Override
    public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler) throws Exception {
        //return HandlerInterceptor.super.preHandle(request, response, handler);
        HttpSession session = request.getSession();

        UserDTO user = (UserDTO) session.getAttribute("user");

        if (user == null) {
            response.setStatus(401);
            return false;
        }
        log.info(user.toString());
```

这样在后续的过程中，都不需要将 user 的信息作为方法的参数传入，类似于前端的全局的状态管理或者props的提升

```java
        UserHolder.saveUser(user);
        return true;
    }

    @Override
    public void afterCompletion(HttpServletRequest request, HttpServletResponse response, Object handler, Exception ex) throws Exception {
        //HandlerInterceptor.super.afterCompletion(request, response, handler, ex);
        UserHolder.removeUser();
    }
}
```

配置需要拦截的请求路径：
```java
@Configuration
public class MvcConfig implements WebMvcConfigurer {

    @Override
    public void addInterceptors(InterceptorRegistry registry) {
        //WebMvcConfigurer.super.addInterceptors(registry);

        registry.addInterceptor(new LoginInterceptor()).excludePathPatterns(
                "/shop/**",
                "/voucher/**",
                "/shop-type/**",
                "/upload/**",
                "/blog/hot",
                "/user/code",
                "/user/login"
        );
    }


}
```

### session 共享问题
每个 Tomcat 中都有一份属于自己的 session，假设用户第一次访问第一台 Tomcat，并且把自己的信息存放到第一台服务器的 session 中
但是第二次这个用户访问到了第二台 Tomcat，那么在第二台服务器上，没有第一台的session，此时登录状态丢失

*说白了，现在就没有使用 session 来实现的了，都是 JWT 了*

早期方案 session 拷贝，同步给其他的 Tomcat 服务器的 session，这样的话，就可以实现session的共享了，但是这种方案具有两个大问题：

- 每台服务器中都有完整的一份session数据，服务器压力过大
- session 拷贝数据时，可能会出现延迟

把 session 换成 redis，redis 数据本身就是共享的，就可以避免 session 共享的问题了

这里 stringRedisTemplate 需要格外的注意，由于这个类不是由 Spring 管理的，这里的不能直接注入，需要自己去调用构造函数：
```java
@Slf4j
public class LoginInterceptor implements HandlerInterceptor {

    private StringRedisTemplate stringRedisTemplate;

    public LoginInterceptor(StringRedisTemplate stringRedisTemplate) {
        this.stringRedisTemplate = stringRedisTemplate;
    }

    @Override
    public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler) throws Exception {
        String token = request.getHeader("authorization");
        log.info("authorization: {}", token);
        if(StrUtil.isBlank(token)){
            response.setStatus(401);
            return false;
        }
        String key = LOGIN_USER_PER + token;

		// 这里的 Map 不可能是 null 所以判空
        Map<Object, Object> userMap = stringRedisTemplate.opsForHash().entries(key);
        if(userMap.isEmpty()){
            response.setStatus(401);
            return false;
        }

        UserDTO user = BeanUtil.fillBeanWithMap(userMap, new UserDTO(), false);

        log.info(user.toString());
        UserHolder.saveUser(user);
        stringRedisTemplate.expire(key, LOGIN_USER_TTL, TimeUnit.MINUTES);
        return true;
    }

    @Override
    public void afterCompletion(HttpServletRequest request, HttpServletResponse response, Object handler, Exception ex) throws Exception {
        //HandlerInterceptor.super.afterCompletion(request, response, handler, ex);
        UserHolder.removeUser();
    }
}
```

```java
@Service
@Slf4j
public class UserServiceImpl extends ServiceImpl<UserMapper, User> implements IUserService {
    @Autowired
    StringRedisTemplate stringRedisTemplate;

    @Override
    public Result sendCode(String phone, HttpSession session) {
        if (RegexUtils.isPhoneInvalid(phone)) return Result.fail("手机号格式错误");

        String code = RandomUtil.randomNumbers(6);

		// 改造后将验证码存到 Redis 中去了
        stringRedisTemplate.opsForValue().set(LOGIN_CODE_PER + phone, code, LOGIN_CODE_TTL, TimeUnit.MINUTES);

        //模拟发送
        log.info("发送验证码：{}", code);

        return Result.ok();
    }

    @Override
    public Result login(LoginFormDTO loginForm, HttpSession session) {
        String phone = loginForm.getPhone();
        if (RegexUtils.isPhoneInvalid(phone)) return Result.fail("手机号格式错误");

        String cachedCode = stringRedisTemplate.opsForValue().get(LOGIN_CODE_PER + phone);

        //String cachedCode = session.getAttribute("code").toString();
        log.info("cachedCode, {}", cachedCode);

        if (cachedCode == null || !cachedCode.equals(loginForm.getCode())) return Result.fail("验证码错误");

        User user = query().eq("phone", phone).one();
        if (user == null) {
            user = createUserWithPhone(phone);
        }

        UserDTO userDTO = BeanUtil.copyProperties(user, UserDTO.class);

        String token = UUID.randomUUID().toString(true);
        String key =  LOGIN_USER_PER + token;

        Map<String, Object> stringObjectMap = BeanUtil.beanToMap(
                userDTO,
                new HashMap<>(),
                CopyOptions.create().setIgnoreNullValue(true).setFieldValueEditor((fieldName, fieldValue) -> fieldValue.toString())
        );

        stringRedisTemplate.opsForHash().putAll(key, stringObjectMap);
        stringRedisTemplate.expire(key, LOGIN_USER_TTL, TimeUnit.MINUTES);
        log.info(token);

        return Result.ok(token);
    }

    private User createUserWithPhone(String phone) {
        User user = new User();

        user.setPhone(phone);
        user.setNickName("user_" + RandomUtil.randomString(10));
        save(user);
        log.info(user.toString());
        return user;
    }
}
```

### 状态登录刷新
可以使用对应路径的拦截，同时刷新登录 token 令牌的存活时间，但只是拦截需要被拦截的路径
假设当前用户访问了一些不需要拦截的路径，拦截器就不会生效，所以此时令牌刷新的动作实际上就不会执行

可以添加一个拦截器，在第一个拦截器中拦截所有的路径，把第二个拦截器做的事情放入到第一个拦截器中，同时刷新令牌，因为第一个拦截器有了threadLocal的数据，所以此时第二个拦截器只需要判断拦截器中的user对象是否存在即可，完成整体刷新功能

```java
public class RefreshTokenInterceptor implements HandlerInterceptor {

    private StringRedisTemplate stringRedisTemplate;

    public RefreshTokenInterceptor(StringRedisTemplate stringRedisTemplate) {
        this.stringRedisTemplate = stringRedisTemplate;
    }

    @Override
    public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler) throws Exception {
        // 1.获取请求头中的token
        String token = request.getHeader("authorization");
        if (StrUtil.isBlank(token)) {
            return true;
        }
        // 2.基于TOKEN获取redis中的用户
        String key  = LOGIN_USER_KEY + token;
        Map<Object, Object> userMap = stringRedisTemplate.opsForHash().entries(key);
        // 3.判断用户是否存在
        if (userMap.isEmpty()) {
            return true;
        }
        // 5.将查询到的hash数据转为UserDTO
        UserDTO userDTO = BeanUtil.fillBeanWithMap(userMap, new UserDTO(), false);
        // 6.存在，保存用户信息到 ThreadLocal
        UserHolder.saveUser(userDTO);
        // 7.刷新token有效期
        stringRedisTemplate.expire(key, LOGIN_USER_TTL, TimeUnit.MINUTES);
        // 8.放行
        return true;
    }

    @Override
    public void afterCompletion(HttpServletRequest request, HttpServletResponse response, Object handler, Exception ex) throws Exception {
        // 移除用户
        UserHolder.removeUser();
    }
}

```

```java
public class LoginInterceptor implements HandlerInterceptor {

    @Override
    public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler) throws Exception {
        // 1.判断是否需要拦截（ThreadLocal中是否有用户）
        if (UserHolder.getUser() == null) {
            // 没有，需要拦截，设置状态码
            response.setStatus(401);
            // 拦截
            return false;
        }
        // 有用户，则放行
        return true;
    }
}
```
