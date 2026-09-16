# 14 File与IO流
> Last Format Time：9/16/2026 19:24:55

![[Pasted image 20260910230829.png]]

![[Pasted image 20260910231324.png]]

```java
File testFile = new File("G:\\Save\\Grogramming\\Java\\test.txt");  
  
System.out.println(testFile.exists());  
// false  
  
System.out.println(testFile.length());  
  
System.out.println(testFile.getAbsolutePath());  
System.out.println(testFile.lastModified());  
System.out.println(testFile.getName().split("\\.")[1]);  
  
File f = new File("G:\\Save\\Grogramming\\Java\\test5.txt\\rrr");  
boolean newFile = f.createNewFile();  
System.out.println(newFile);  

// 空文件夹、文件直接删不进回收站，有内容的不行
boolean delete = f.delete();  
  
f.mkdirs();  
f.mkdir();  
// mkdir 没啥用了就

File testFile = new File("G:\\Save\\Grogramming\\Java\\test\\src\\com\\app");  
  
for (File file : testFile.listFiles()) {  
    System.out.println(file);  
    // G:\Save\Grogramming\Java\test\src\com\app\Animal.java  
    // G:\Save\Grogramming\Java\test\src\com\app\Cat.java    // G:\Save\Grogramming\Java\test\src\com\app\Dog.java    // ...}
```