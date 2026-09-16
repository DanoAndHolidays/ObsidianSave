# IO流
> Last Format Time：9/16/2026 19:24:55

---
## 📚 一、IO流核心概念
### 什么是流(Stream)
- **流**：数据在输入/输出设备与程序之间的流动通道
- **特点**：单向流动、顺序访问、先进先出

### 流的分类（考试重点⭐）
##### 按数据流向：
- **输入流**：从外部读入数据到程序 (`InputStream`, `Reader`)
- **输出流**：从程序写出数据到外部 (`OutputStream`, `Writer`)

##### 按数据处理单位：
- **字节流**：以字节为单位 (8bit)，处理所有类型数据
  - `InputStream` / `OutputStream`
- **字符流**：以字符为单位 (16bit)，处理文本数据
  - `Reader` / `Writer`

##### 按功能：
- **节点流**：直接与数据源连接
- **处理流(过滤流)**：对现有流包装，增强功能

---
## 🔧 二、常用IO流类体系
### 字节流体系：
```text
InputStream (抽象类)
├── FileInputStream (文件字节输入流)
├── FilterInputStream (过滤字节输入流)
│   ├── BufferedInputStream (缓冲字节输入流)
│   ├── DataInputStream (数据字节输入流)
│   └── ObjectInputStream (对象字节输入流)
└── ...

OutputStream (抽象类)
├── FileOutputStream (文件字节输出流)
├── FilterOutputStream (过滤字节输出流)
│   ├── BufferedOutputStream (缓冲字节输出流)
│   ├── DataOutputStream (数据字节输出流)
│   ├── PrintStream (打印输出流)
│   └── ObjectOutputStream (对象字节输出流)
└── ...
```

### 字符流体系：
```text
Reader (抽象类)
├── InputStreamReader (字节到字符的转换流)
│   └── FileReader (文件字符输入流)
├── BufferedReader (缓冲字符输入流)
└── ...

Writer (抽象类)
├── OutputStreamWriter (字符到字节的转换流)
│   └── FileWriter (文件字符输出流)
├── BufferedWriter (缓冲字符输出流)
├── PrintWriter (打印字符输出流)
└── ...
```

---
## 💻 三、必会代码模板
### 文件字节流读写（基础）
```java
// 文件字节输入流
FileInputStream fis = null;
try {
    fis = new FileInputStream("test.txt");
    int data;
    while ((data = fis.read()) != -1) {  // 一次读一个字节
        System.out.print((char) data);
    }
} catch (IOException e) {
    e.printStackTrace();
} finally {
    if (fis != null) {
        try {
            fis.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}

// 文件字节输出流
FileOutputStream fos = null;
try {
    fos = new FileOutputStream("output.txt");
    String text = "Hello World";
    fos.write(text.getBytes());  // 字符串转字节数组写入
} catch (IOException e) {
    e.printStackTrace();
} finally {
    if (fos != null) {
        try {
            fos.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
```

### 缓冲流使用（提高效率⭐）
```java
// 缓冲字节流
try (FileInputStream fis = new FileInputStream("source.txt");
     BufferedInputStream bis = new BufferedInputStream(fis);
     FileOutputStream fos = new FileOutputStream("target.txt");
     BufferedOutputStream bos = new BufferedOutputStream(fos)) {
    
    byte[] buffer = new byte[1024];
    int length;
    while ((length = bis.read(buffer)) != -1) {
        bos.write(buffer, 0, length);  // 注意：写入实际读取的长度
    }
} catch (IOException e) {
    e.printStackTrace();
}
```

### 数据流（读写基本数据类型⭐）
```java
// 写入基本数据类型
try (DataOutputStream dos = new DataOutputStream(
        new FileOutputStream("data.dat"))) {
    dos.writeInt(100);        // 写int
    dos.writeDouble(3.14);    // 写double
    dos.writeUTF("Java");     // 写字符串(UTF-8)
} catch (IOException e) {
    e.printStackTrace();
}

// 读取基本数据类型
try (DataInputStream dis = new DataInputStream(
        new FileInputStream("data.dat"))) {
    int num = dis.readInt();          // 读int
    double value = dis.readDouble();  // 读double
    String text = dis.readUTF();      // 读字符串
    System.out.println(num + ", " + value + ", " + text);
} catch (IOException e) {
    e.printStackTrace();
}
```

### 字符流读写文本文件（考试重点⭐）
```java
// 字符流读取文本文件
try (FileReader fr = new FileReader("text.txt");
     BufferedReader br = new BufferedReader(fr)) {
    
    String line;
    while ((line = br.readLine()) != null) {  // 一次读一行
        System.out.println(line);
    }
} catch (IOException e) {
    e.printStackTrace();
}

// 字符流写入文本文件
try (FileWriter fw = new FileWriter("output.txt");
     BufferedWriter bw = new BufferedWriter(fw)) {
    
    bw.write("第一行");
    bw.newLine();  // 换行
    bw.write("第二行");
    bw.flush();    // 刷新缓冲区
} catch (IOException e) {
    e.printStackTrace();
}
```

### 转换流（字节流↔字符流）
```java
// 字节流转换为字符流
try (FileInputStream fis = new FileInputStream("text.txt");
     InputStreamReader isr = new InputStreamReader(fis, "UTF-8");  // 指定编码
     BufferedReader br = new BufferedReader(isr)) {
    
    String line;
    while ((line = br.readLine()) != null) {
        System.out.println(line);
    }
} catch (IOException e) {
    e.printStackTrace();
}
```

---
## 🎯 四、考试常见题型及解法
### 题型1：填空题（补全IO操作代码）
**解题技巧**：
1. 先判断是输入还是输出
2. 判断是字节流还是字符流
3. 看是否需要缓冲流或数据流
4. 注意异常处理

**示例**：
```java
// 补全文件复制代码
try (FileInputStream fis = __________;
     __________ bis = new BufferedInputStream(fis);
     FileOutputStream fos = new FileOutputStream("copy.txt");
     __________ bos = new BufferedOutputStream(fos)) {
    
    byte[] buffer = new byte[1024];
    int length;
    while ((length = __________) != -1) {
        __________;
    }
} catch (IOException e) {
    e.printStackTrace();
}
```

**答案**：
```java
new FileInputStream("source.txt")
BufferedInputStream
BufferedOutputStream
bis.read(buffer)
bos.write(buffer, 0, length)
```

### 题型2：程序分析题
**解题步骤**：
1. 识别使用的流类型
2. 分析流的功能（读取、写入、缓冲、数据类型处理）
3. 指出可能的异常
4. 分析程序执行结果

### 题型3：简答题
**常考问题**：
1. 字节流和字符流的区别？
2. 节点流和处理流的区别？
3. 为什么要使用缓冲流？
4. 如何使用DataInputStream和DataOutputStream？

---
## 📝 五、必须掌握的简答题答案
### 字节流 vs 字符流
- **字节流**：以字节为单位，可处理所有类型文件
- **字符流**：以字符为单位，专门处理文本文件，会自动处理编码

### 为什么需要缓冲流？
- 减少实际IO操作次数，提高效率
- 缓冲流内部有缓冲区，批量读写数据

### try-with-resources的优势
- 自动关闭资源，避免资源泄漏
- 代码更简洁，不需要finally块手动关闭

### 流的包装顺序原则
- 节点流在最内层
- 处理流包装在节点流外层
- 关闭时只需关闭最外层流

---
## ⚠️ 六、常见错误及注意事项
1. **忘记关闭流** → 使用try-with-resources
2. **混淆read()返回值** → 字节流read()返回int，字符流read()返回int或String
3. **文件路径问题** → 使用相对路径或绝对路径
4. **编码问题** → 字符流注意指定正确的字符编码
5. **缓冲流未flush** → 重要数据记得调用flush()

---
## 🎪 七、快速记忆口诀
```text
输入输出分清楚，
字节字符看用途。
文件操作是基础，
缓冲包装提速度。
数据流来读类型，
字符文本最合适。
try-with-resources用起来，
资源关闭不用愁。
```

---
## 📋 八、IO流选择决策树
```text
要处理什么数据？
├── 二进制数据(图片、视频等) → 字节流
└── 文本数据 → 字符流

需要什么功能？
├── 基本读写 → 文件流
├── 提高效率 → + 缓冲流
├── 读写基本数据类型 → + 数据流
└── 处理编码 → 转换流
```

按照这个指南学习，IO部分考试绝对没问题！重点掌握代码模板和分类概念，考试时直接套用即可。