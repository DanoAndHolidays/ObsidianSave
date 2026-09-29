# 02 CRUD
> Last Format Time：9/16/2026 19:24:55

```java
@Mapper // 在运行时会自动的创建代理对象（动态代理），会自动的将对象自动的存入IOC容器中  
public interface UserMapper {  
  
    @Select("select * from user2")  
    public List<User> findAll();  
  
    @Delete("delete from user2 where id = #{id}")  
    public Integer deleteById(Integer id);  
  
    @Insert("insert into user2(username, name, age, gender) values(#{username}, #{name}, #{age}, #{gender})")  
    public void insert(User user);  
    // 这里就不用一个一个写，直接传入对应的对象  
  
    @Update("update user2 set username = #{username} where id = #{id}")  
    public void update(User user);  
  
    // 这里要加个@Param，有点诡异了，多个参数要使用这注解，一个就不用了  
    @Select("select * from user2 where username = #{username}")  
    public User select(@Param("username") String username);  
}
```

---
## delete
推荐使用 `#{...}`：
![[Pasted image 20260916002838.png]]

---
## insert
![[Pasted image 20260916004407.png]]
剩下的先不写了，以后再说

---
## XML 映射配置
![[Pasted image 20260917011310.png]]

