# 02 CRUD
> Last Format Time：9/16/2026 19:24:55

```java
@Autowired  
private UserMapper userMapper;  
  
@Test  
public void testFindAll(){  
    List<User> userList = userMapper.findAll();  
    userList.forEach(System.out::println);  
}  
  
@Test  
public void testDeleteById(){  
    Integer i = userMapper.deleteById(1);  
    System.out.println(i);  
    /*  
    ==>  Preparing: delete from user2 where id = ? 预编译的  
    ==> Parameters: 1(Integer)    <==    Updates: 1    */}  
  
@Test  
public void testInsert(){  
    User user = new User(null, "Dano66", "shit", 34, "男");  
    userMapper.insert(user);  
}
```

---
## delete
推荐使用 `#{...}`：
![[Pasted image 20260916002838.png]]

---
## insert
![[Pasted image 20260916004407.png]]

