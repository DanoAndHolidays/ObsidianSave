**GUI**
电话薄
```java
import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

public class PhoneBookGUI extends JFrame {
    // 输入组件
    private JTextField nameField, companyField, jobField, homePhoneField, mobilePhoneField, officePhoneField;
    // 显示区域
    private JTextArea displayArea;

    public PhoneBookGUI() {
        // 窗口基本设置
        setTitle("电话簿信息输入");
        setSize(600, 500);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setLocationRelativeTo(null); // 居中显示

        // 创建主面板（使用网格袋布局，便于精确控制组件位置）
        JPanel mainPanel = new JPanel(new GridBagLayout());
        GridBagConstraints gbc = new GridBagConstraints();
        gbc.insets = new Insets(5, 5, 5, 5); // 组件间距
        gbc.anchor = GridBagConstraints.WEST; // 左对齐

        // 添加标签和输入框
        int row = 0; // 行索引

        // 姓名
        gbc.gridx = 0;
        gbc.gridy = row++;
        mainPanel.add(new JLabel("姓名："), gbc);
        nameField = new JTextField(20);
        gbc.gridx = 1;
        mainPanel.add(nameField, gbc);

        // 工作单位
        gbc.gridx = 0;
        gbc.gridy = row++;
        mainPanel.add(new JLabel("工作单位："), gbc);
        companyField = new JTextField(20);
        gbc.gridx = 1;
        mainPanel.add(companyField, gbc);

        // 职务
        gbc.gridx = 0;
        gbc.gridy = row++;
        mainPanel.add(new JLabel("职务："), gbc);
        jobField = new JTextField(20);
        gbc.gridx = 1;
        mainPanel.add(jobField, gbc);

        // 住宅电话
        gbc.gridx = 0;
        gbc.gridy = row++;
        mainPanel.add(new JLabel("住宅电话："), gbc);
        homePhoneField = new JTextField(20);
        gbc.gridx = 1;
        mainPanel.add(homePhoneField, gbc);

        // 手机号码
        gbc.gridx = 0;
        gbc.gridy = row++;
        mainPanel.add(new JLabel("手机号码："), gbc);
        mobilePhoneField = new JTextField(20);
        gbc.gridx = 1;
        mainPanel.add(mobilePhoneField, gbc);

        // 办公室电话
        gbc.gridx = 0;
        gbc.gridy = row++;
        mainPanel.add(new JLabel("办公室电话："), gbc);
        officePhoneField = new JTextField(20);
        gbc.gridx = 1;
        mainPanel.add(officePhoneField, gbc);

        // 提交按钮
        JButton submitBtn = new JButton("提交");
        gbc.gridx = 0;
        gbc.gridy = row++;
        gbc.gridwidth = 2; // 跨两列
        gbc.anchor = GridBagConstraints.CENTER; // 居中
        mainPanel.add(submitBtn, gbc);

        // 显示区域（文本区，不可编辑）
        displayArea = new JTextArea(10, 40);
        displayArea.setEditable(false);
        displayArea.setBorder(BorderFactory.createTitledBorder("输入的电话簿信息"));
        JScrollPane scrollPane = new JScrollPane(displayArea); // 支持滚动
        gbc.gridx = 0;
        gbc.gridy = row++;
        gbc.fill = GridBagConstraints.BOTH; // 填充空间
        gbc.weightx = 1;
        gbc.weighty = 1;
        mainPanel.add(scrollPane, gbc);

        // 按钮点击事件：获取输入信息并显示
        submitBtn.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                // 拼接输入信息
                String info = String.format(
                        "姓名：%s\n工作单位：%s\n职务：%s\n住宅电话：%s\n手机号码：%s\n办公室电话：%s\n\n",
                        nameField.getText(),
                        companyField.getText(),
                        jobField.getText(),
                        homePhoneField.getText(),
                        mobilePhoneField.getText(),
                        officePhoneField.getText());
                // 显示到文本区（追加模式）
                displayArea.append(info);
                // 清空输入框
                clearInputFields();
            }
        });

        // 添加主面板到窗口
        add(mainPanel);
        setVisible(true);
    }

    // 清空所有输入框
    private void clearInputFields() {
        nameField.setText("");
        companyField.setText("");
        jobField.setText("");
        homePhoneField.setText("");
        mobilePhoneField.setText("");
        officePhoneField.setText("");
    }

    public static void main(String[] args) {
        // 确保在EDT（事件调度线程）中运行GUI
        SwingUtilities.invokeLater(PhoneBookGUI::new);
    }
}
```

进制转换
```java
import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

public class NumberConverter extends JFrame {
    // 输入输出组件
    private JTextField decimalInput; // 十进制输入
    private JTextField binaryOutput, octalOutput, hexOutput; // 各进制输出

    public NumberConverter() {
        // 窗口基本设置
        setTitle("进制转换器");
        setSize(500, 300);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setLocationRelativeTo(null); // 居中显示

        // 主面板（网格布局，4行2列）
        JPanel mainPanel = new JPanel(new GridLayout(4, 2, 10, 10));
        mainPanel.setBorder(BorderFactory.createEmptyBorder(20, 20, 20, 20)); // 边距

        // 十进制输入
        mainPanel.add(new JLabel("十进制整数："));
        decimalInput = new JTextField();
        mainPanel.add(decimalInput);

        // 二进制输出
        mainPanel.add(new JLabel("二进制："));
        binaryOutput = new JTextField();
        binaryOutput.setEditable(false); // 不可编辑
        mainPanel.add(binaryOutput);

        // 八进制输出
        mainPanel.add(new JLabel("八进制："));
        octalOutput = new JTextField();
        octalOutput.setEditable(false);
        mainPanel.add(octalOutput);

        // 十六进制输出
        mainPanel.add(new JLabel("十六进制："));
        hexOutput = new JTextField();
        hexOutput.setEditable(false);
        mainPanel.add(hexOutput);

        // 转换按钮
        JButton convertBtn = new JButton("转换");
        convertBtn.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                convertNumber();
            }
        });
        // 底部面板放按钮
        JPanel bottomPanel = new JPanel();
        bottomPanel.add(convertBtn);

        // 组装窗口
        add(mainPanel, BorderLayout.CENTER);
        add(bottomPanel, BorderLayout.SOUTH);

        setVisible(true);
    }

    // 转换逻辑：十进制转其他进制
    private void convertNumber() {
        try {
            // 获取输入的十进制数
            String input = decimalInput.getText().trim();
            if (input.isEmpty()) {
                JOptionPane.showMessageDialog(this, "请输入十进制整数", "提示", JOptionPane.WARNING_MESSAGE);
                return;
            }
            int num = Integer.parseInt(input);

            // 转换并显示
            binaryOutput.setText(Integer.toBinaryString(num)); // 二进制
            octalOutput.setText(Integer.toOctalString(num));   // 八进制
            hexOutput.setText(Integer.toHexString(num).toUpperCase()); // 十六进制（大写）
        } catch (NumberFormatException ex) {
            // 处理非整数输入
            JOptionPane.showMessageDialog(this, "请输入有效的十进制整数", "输入错误", JOptionPane.ERROR_MESSAGE);
            // 清空输出
            binaryOutput.setText("");
            octalOutput.setText("");
            hexOutput.setText("");
        }
    }

    public static void main(String[] args) {
        // 在EDT中运行GUI
        SwingUtilities.invokeLater(NumberConverter::new);
    }
}
```

**多线程**
```java
import java.util.Random;

class BankAccount {
    private int balance = 0;
    public synchronized void deposit(int amount) {
        balance += amount;
        System.out.println("在线程" + Thread.currentThread().getName() + "中，存入：" + amount + " 现有：" + balance);
    }
}

class DepositTask implements Runnable {
    private final BankAccount account;
    public DepositTask(BankAccount account) {
        this.account = account;
    }

    @Override
    public void run() {
        Random random = new Random();
        for (int i = 0; i < 5; i++) {
            int amount = random.nextInt(100) + 1;
            account.deposit(amount);
            try {
                Thread.sleep(100);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
    }

}

public class Main {
    public static void main(String[] args) {
        BankAccount account = new BankAccount();

        Thread t1 = new Thread(new DepositTask(account), "1");
        Thread t2 = new Thread(new DepositTask(account), "2");

        t1.start();
        t2.start();
    }
}
```

```java
import java.util.concurrent.TimeUnit;
import java.util.concurrent.locks.Condition;
import java.util.concurrent.locks.Lock;
import java.util.concurrent.locks.ReentrantLock;

public class ClassThreadDemo {
    // 创建锁对象
    private static final Lock lock = new ReentrantLock();
    // 为student1和student2分别创建Condition（精确唤醒）
    private static final Condition student1Condition = lock.newCondition();
    private static final Condition student2Condition = lock.newCondition();

    public static void main(String[] args) {
        // 定义student1线程
        Thread student1 = new Thread(() -> {
            lock.lock(); // 获取锁
            try {
                System.out.println("student1：准备休息10分钟，等待上课信号...");
                // 等待10分钟（超时自动唤醒）或被teacher唤醒
                student1Condition.await(10, TimeUnit.MINUTES);
                
                System.out.println("student1：收到上课信号，准备唤醒student2...");
                // 唤醒student2
                student2Condition.signal();
                System.out.println("student1：已唤醒student2，开始上课！");
            } catch (InterruptedException e) {
                e.printStackTrace();
            } finally {
                lock.unlock(); // 释放锁
            }
        }, "student1");

        // 定义student2线程
        Thread student2 = new Thread(() -> {
            lock.lock(); // 获取锁
            try {
                System.out.println("student2：准备休息1小时，等待被唤醒...");
                // 等待1小时（超时自动唤醒）或被student1唤醒
                student2Condition.await(60, TimeUnit.MINUTES);
                
                System.out.println("student2：被唤醒，开始上课！");
            } catch (InterruptedException e) {
                e.printStackTrace();
            } finally {
                lock.unlock(); // 释放锁
            }
        }, "student2");

        // 定义teacher线程
        Thread teacher = new Thread(() -> {
            lock.lock(); // 获取锁
            try {
                // 等待0.5秒，确保学生线程先进入等待状态
                Thread.sleep(500);
                
                System.out.println("teacher：发出上课信号，唤醒student1！");
                // 唤醒student1
                student1Condition.signal();
            } catch (InterruptedException e) {
                e.printStackTrace();
            } finally {
                lock.unlock(); // 释放锁
            }
        }, "teacher");

        // 启动线程（先启动学生，再启动老师）
        student1.start();
        student2.start();
        teacher.start();
    }
}
```

**单线程**
```java
import java.util.ArrayList;
import java.util.Scanner;

class NumThread extends Thread {
    private ArrayList<Integer> list = new ArrayList<>();

    @Override
    public void run() {
        Scanner scanner = new Scanner(System.in);
        String input;
        System.out.println("请你输入数字，以$为结尾");
        while (true) {
            input = scanner.nextLine();
            if (input.equalsIgnoreCase("$")) {
                break;
            }

            try {
                int num = Integer.parseInt(input);
                list.add(num);
            } catch (NumberFormatException e) {
                System.out.println("请你输入正确的数字");
            }
        }
        scanner.close();

        if (list.size() > 0) {
            int min = list.get(0);
            int max = list.get(0);
            int sum = 0;

            for (Integer itemInteger : list) {

                if (itemInteger < min) {
                    min = itemInteger;
                }
                if (itemInteger > max) {
                    max = itemInteger;
                }
                sum += itemInteger;
            }

            double average = sum / list.size();

            System.out.println("min:" + min + " max:" + max + " average:" + average);
        } else {
            System.out.println("没有输入任何数字！！！");
        }
    }
}

public class Main {
    public static void main(String[] args) {
        Thread numThread = new NumThread();
        numThread.start();
    }
}
``` 

**冒泡排序**
```java
class Student {
    String name;
    int id;
    int score;

    public Student(String name, int id, int score) {
        this.name = name;
        this.id = id;
        this.score = score;
    }

    public int getScore() {
        return this.score;
    }

    public int compare(Student otherStudent) {
        return Integer.compare(this.score, otherStudent.score);
    }

    @Override
    public String toString() {
        return "name:" + name + " id:" + id + " score:" + score;
    }
}

public class Main {
    public static void main(String[] args) {
        Student[] students = {
                new Student("Tom1", 11, 611),
                new Student("Tom2", 12, 502),
                new Student("Tom3", 13, 603),
                new Student("Tom4", 14, 604),
                new Student("Tom5", 15, 605)
        };

        System.out.println("排序前：");
        printStudens(students);

        sortStudents(students);

        System.out.println("排序后：");
        printStudens(students);
    }

    public static void printStudens(Student[] students) {
        for (Student itemStudent : students) {
            System.out.println(itemStudent);
        }
    }

    // 使用冒泡排序实现
    public static void sortStudents(Student[] students) {
        int len = students.length;

        for (int i = 0; i < len - 1; i++) {
            for (int j = 0; j < len - i - 1; j++) {
                if (students[j].compare(students[j + 1]) > 0) {
                    Student temp = students[j];
                    students[j] = students[j + 1];
                    students[j + 1] = temp;
                }
            }
        }
    }
}
```

**Collections与ArrayList**
```java
import java.util.ArrayList;
import java.util.Collections;
import java.util.Iterator;

class Student implements Comparable<Student> {
    String name;
    int id;
    int score;

    public Student(String name, int id, int score) {
        this.name = name;
        this.id = id;
        this.score = score;
    }

    public int getId() {
        return id;
    }

    public int getScore() {
        return score;
    }

    @Override
    public String toString() {
        return "name:" + name + " id:" + id + " score:" + score;
    }

    // 实现Comparable接口，定义排序规则（按分数升序）
    @Override
    public int compareTo(Student other) {
        return Integer.compare(this.score, other.score);
    }
}

public class Main {
    public static void main(String[] args) {
        // 1. 用ArrayList存储Student对象
        ArrayList<Student> studentList = new ArrayList<>();
        studentList.add(new Student("Tom1", 11, 611));
        studentList.add(new Student("Tom2", 12, 502));
        studentList.add(new Student("Tom3", 13, 603));
        studentList.add(new Student("Tom4", 14, 604));
        studentList.add(new Student("Tom5", 15, 605));

        // 2. 遍历操作（增强for循环）
        System.out.println("===== 遍历所有学生 =====");
        for (Student s : studentList) {
            System.out.println(s);
        }

        // 3. 查询操作（根据id查询学生）
        int queryId = 13;
        Student foundStudent = null;
        for (Student s : studentList) {
            if (s.getId() == queryId) {
                foundStudent = s;
                break;
            }
        }
        System.out.println("\n===== 查询id为" + queryId + "的学生 =====");
        System.out.println(foundStudent != null ? foundStudent : "未找到该学生");

        // 4. 删除操作（根据id删除学生，用迭代器保证安全删除）
        int deleteId = 12;
        boolean isDeleted = false;
        Iterator<Student> iterator = studentList.iterator();
        while (iterator.hasNext()) {
            Student s = iterator.next();
            if (s.getId() == deleteId) {
                iterator.remove();
                isDeleted = true;
                break;
            }
        }
        System.out.println("\n===== 删除id为" + deleteId + "的学生 =====");
        System.out.println("删除" + (isDeleted ? "成功" : "失败"));
        System.out.println("删除后列表：");
        for (Student s : studentList) {
            System.out.println(s);
        }

        // 5. 利用Collections排序（按分数升序，因Student实现了Comparable）
        System.out.println("\n===== 排序操作 =====");
        System.out.println("排序前：");
        for (Student s : studentList) {
            System.out.println(s);
        }
        Collections.sort(studentList);
        System.out.println("排序后（按分数升序）：");
        for (Student s : studentList) {
            System.out.println(s);
        }
    }
}
```

**接口编程**
```java
interface ShapeOperations {
    double area();

    double perimeter();
}

class Rectangle implements ShapeOperations {
    private int width = 0;
    private int height = 0;

    public Rectangle(int width, int height) {
        this.width = width;
        this.height = height;
    }

    @Override
    public double area() {
        return width * height * 1.0f;
    }

    @Override
    public double perimeter() {
        return (width + height) * 2.0f;
    }

    public String toString() {
        return "height:" + this.height + " width:" + this.width + " area:" + area() + " perimeter:" + perimeter();
    }
}

public class Main {
    public static void main(String[] args) {
        Rectangle r = new Rectangle(20, 20);
        System.out.println(r);
    }
}
```

**匿名内部类**
这东西和()->{}很像，都是不用去实现一个类，就可以去实现一些功能，省去了很多的重复代码
```java
// 抽象水果类
abstract class Fruit {
    public abstract String getFruitName();
}

// 消费者类
class Consumer {
    public void eat(Fruit fruit) {
        System.out.println("吃了" + fruit.getFruitName());
    }
}

// 主类
public class Main {
    public static void main(String[] args) {
        // 创建消费者对象
        Consumer consumer = new Consumer();

        // 不使用匿名内部类的传统方式实现
        class Apple extends Fruit {
            @Override
            public String getFruitName() {
                return "苹果";
            }
        }
        Fruit apple = new Apple();

        // 用匿名类实现Fruit，创建香蕉实例
        Fruit banana = new Fruit() {
            @Override
            public String getFruitName() {
                return "香蕉";
            }
        };

        // 消费者吃水果
        consumer.eat(apple); // 输出：吃了苹果
        consumer.eat(banana); // 输出：吃了香蕉
    }
}
```

**随机数生成并统计次数**
```java
import java.util.Random;

public class RandomNumProbability {
    public static void main(String[] args) {
        int[] counts = new int[6]; // 索引0不用，1-5对应数字1-5的计数
        Random random = new Random();

        // 生成50个1-5的随机数并统计次数
        for (int i = 0; i < 50; i++) {
            int num = random.nextInt(5) + 1; // 生成1-5的随机数
            counts[num]++;
        }

        // 计算并输出每个数的概率
        System.out.println("数字\t出现次数\t概率");
        for (int i = 1; i <= 5; i++) {
            double probability = (double) counts[i] / 50;
            System.out.printf("%d\t%d\t\t%.2f\n", i, counts[i], probability);
        }
    }
}
```

**判断回文串**
```java
public class PalindromeCheck {
    public static boolean isPalindrome(String str) {
        if (str == null || str.isEmpty()) {
            return false;
        }
        int left = 0, right = str.length() - 1;
        while (left < right) {
            if (str.charAt(left) != str.charAt(right)) {
                return false;
            }
            left++;
            right--;
        }
        return true;
    }

    public static void main(String[] args) {
        String s1 = "abcba";
        String s2 = "abcde";
        System.out.println(s1 + " 是否是回文串：" + isPalindrome(s1));
        System.out.println(s2 + " 是否是回文串：" + isPalindrome(s2));
    }
}
```

**IO流**
```java
import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;

public class FileStatistics {
    public static void main(String[] args) {
        // 文本文件路径（可替换为实际文件路径）
        String filePath = "test.txt";
        int charCount = 0; // 字符数
        int lineCount = 0; // 行数

        try (BufferedReader br = new BufferedReader(new FileReader(filePath))) {
            String line;
            while ((line = br.readLine()) != null) {
                lineCount++; // 每行+1
                charCount += line.length(); // 累加该行字符数（不含换行符，若需包含可+1）
            }
            // 输出结果
            System.out.println("文件行数：" + lineCount);
            System.out.println("文件字符数：" + charCount); // 若需包含换行符，可改为 charCount + lineCount
        } catch (IOException e) {
            System.out.println("文件操作异常：" + e.getMessage());
        }
    }
}
```

```java
import java.io.*;

public class ImageCopy {
    // 源图片和目标图片路径（替换为实际路径）
    private static final String SRC_PATH = "source.jpg";
    private static final String DEST1_PATH = "copy1.jpg"; // 字节流复制结果
    private static final String DEST2_PATH = "copy2.jpg"; // 缓冲流复制结果

    public static void main(String[] args) {
        // 字节流复制
        long time1 = copyWithFileStream();
        // 缓冲流复制
        long time2 = copyWithBufferedStream();

        System.out.println("字节流复制耗时：" + time1 + "毫秒");
        System.out.println("缓冲流复制耗时：" + time2 + "毫秒");
    }

    // 字节流复制（FileInputStream/FileOutputStream）
    private static long copyWithFileStream() {
        long start = System.currentTimeMillis();
        try (InputStream is = new FileInputStream(SRC_PATH);
             OutputStream os = new FileOutputStream(DEST1_PATH)) {
            byte[] buffer = new byte[1024];
            int len;
            while ((len = is.read(buffer)) != -1) {
                os.write(buffer, 0, len);
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
        return System.currentTimeMillis() - start;
    }

    // 缓冲流复制（BufferedInputStream/BufferedOutputStream）
    private static long copyWithBufferedStream() {
        long start = System.currentTimeMillis();
        try (BufferedInputStream bis = new BufferedInputStream(new FileInputStream(SRC_PATH));
             BufferedOutputStream bos = new BufferedOutputStream(new FileOutputStream(DEST2_PATH))) {
            byte[] buffer = new byte[1024];
            int len;
            while ((len = bis.read(buffer)) != -1) {
                bos.write(buffer, 0, len);
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
        return System.currentTimeMillis() - start;
    }
}
```

```java
import java.io.*;

public class ImageCopy {
    // 源图片和目标图片路径（替换为实际路径）
    private static final String SRC_PATH = "source.jpg";
    private static final String DEST1_PATH = "copy1.jpg"; // 字节流复制结果
    private static final String DEST2_PATH = "copy2.jpg"; // 缓冲流复制结果

    public static void main(String[] args) {
        // 字节流复制
        long time1 = copyWithFileStream();
        // 缓冲流复制
        long time2 = copyWithBufferedStream();

        System.out.println("字节流复制耗时：" + time1 + "毫秒");
        System.out.println("缓冲流复制耗时：" + time2 + "毫秒");
    }

    // 字节流复制（FileInputStream/FileOutputStream）
    private static long copyWithFileStream() {
        long start = System.currentTimeMillis();
        try (InputStream is = new FileInputStream(SRC_PATH);
             OutputStream os = new FileOutputStream(DEST1_PATH)) {
            byte[] buffer = new byte[1024];
            int len;
            while ((len = is.read(buffer)) != -1) {
                os.write(buffer, 0, len);
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
        return System.currentTimeMillis() - start;
    }

    // 缓冲流复制（BufferedInputStream/BufferedOutputStream）
    private static long copyWithBufferedStream() {
        long start = System.currentTimeMillis();
        try (BufferedInputStream bis = new BufferedInputStream(new FileInputStream(SRC_PATH));
             BufferedOutputStream bos = new BufferedOutputStream(new FileOutputStream(DEST2_PATH))) {
            byte[] buffer = new byte[1024];
            int len;
            while ((len = bis.read(buffer)) != -1) {
                bos.write(buffer, 0, len);
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
        return System.currentTimeMillis() - start;
    }
}
```

```java
import java.io.*;
import java.time.LocalDate;
import java.util.Scanner;

public class ExpenseRecord {
    private static final String RECORD_FILE = "expense.txt"; // 记录文件

    public static void main(String[] args) {
        // 显示上一次消费信息
        showLastRecord();

        // 显示当前日期
        LocalDate today = LocalDate.now();
        System.out.println("\n当前日期：" + today);

        // 键盘输入消费信息
        Scanner scanner = new Scanner(System.in);
        System.out.print("请输入消费项目：");
        String item = scanner.nextLine();
        System.out.print("请输入消费金额：");
        double amount = scanner.nextDouble();

        // 生成记录字符串
        String record = String.format("[%s] 项目：%s，金额：%.2f元%n", today, item, amount);

        // 追加到文件
        appendToFile(record);
        System.out.println("记录已保存！");
        scanner.close();
    }

    // 显示上一次消费信息（文件最后一行）
    private static void showLastRecord() {
        System.out.println("上一次消费信息：");
        try (BufferedReader br = new BufferedReader(new FileReader(RECORD_FILE))) {
            String lastLine = null;
            String line;
            while ((line = br.readLine()) != null) {
                lastLine = line;
            }
            System.out.println(lastLine != null ? lastLine : "暂无消费记录");
        } catch (FileNotFoundException e) {
            System.out.println("暂无消费记录（文件不存在）");
        } catch (IOException e) {
            System.out.println("读取记录失败：" + e.getMessage());
        }
    }

    // 追加记录到文件
    private static void appendToFile(String content) {
        try (BufferedWriter bw = new BufferedWriter(new FileWriter(RECORD_FILE, true))) {
            bw.write(content);
        } catch (IOException e) {
            System.out.println("保存记录失败：" + e.getMessage());
        }
    }
}
```