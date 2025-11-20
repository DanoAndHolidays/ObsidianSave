# Graphical User Interface
现在常用的开发模式是Web开发，这种使用Swing与AWT的开发方式已经过时，这次学习主要是为了学校的课程考核要求
![[Pasted image 20251115164053.png]]
![[Pasted image 20251115164218.png]]
![[Pasted image 20251115164439.png]]
![[Pasted image 20251115164648.png]]
![[Pasted image 20251115164930.png]]
![[Pasted image 20251115165052.png]]

![[Pasted image 20251115165302.png]]
![[Pasted image 20251115165321.png]]
![[Pasted image 20251115165439.png]]
![[Pasted image 20251115170153.png]]
![[Pasted image 20251115170219.png]]
![[Pasted image 20251115170315.png]]
![[Pasted image 20251115170453.png]]
![[Pasted image 20251115170650.png]]
![[Pasted image 20251115170958.png]]
![[Pasted image 20251115171024.png]]
![[Pasted image 20251115171123.png]]
![[Pasted image 20251115171150.png]]
![[Pasted image 20251115171504.png]]
![[Pasted image 20251115171617.png]]
![[Pasted image 20251115171739.png]]
![[Pasted image 20251115171812.png]]
![[Pasted image 20251115171917.png]]
![[Pasted image 20251115172103.png]]
![[Pasted image 20251115172147.png]]
![[Pasted image 20251115172204.png]]
![[Pasted image 20251115172249.png]]

![[Pasted image 20251115173419.png]]
![[Pasted image 20251115173549.png]]
![[Pasted image 20251115173650.png]]
![[Pasted image 20251115173822.png]]
![[Pasted image 20251115174001.png]]
![[Pasted image 20251115174617.png]]
## 2024真题
使用Flow 布局。求数 1数 2的最大公约数，最小公倍数的输入框。计算，并有退出按钮。
```java
import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

public class GCDLCDCalculator extends JFrame {

    private final JTextField num1Field;
    private final JTextField num2Field;
    private final JTextField gcdField;
    private final JTextField lcmField;

    public GCDLCDCalculator() {
        // 设置窗口标题
        setTitle("最大公约数和最小公倍数计算器");

        // 设置窗口关闭操作
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

        // 设置 FlowLayout 布局
        setLayout(new FlowLayout(FlowLayout.CENTER, 50, 50));

        // 创建标签和输入框
        JLabel num1Label = new JLabel("数 1:");
        num1Field = new JTextField(10);

        JLabel num2Label = new JLabel("数 2:");
        num2Field = new JTextField(10);

        JLabel gcdLabel = new JLabel("最大公约数:");
        gcdField = new JTextField(10);
        gcdField.setEditable(false); // 结果框不可编辑

        JLabel lcmLabel = new JLabel("最小公倍数:");
        lcmField = new JTextField(10);
        lcmField.setEditable(false); // 结果框不可编辑

        // 创建按钮
        JButton calculateButton = new JButton("计算");
        JButton exitButton = new JButton("退出");

        // 添加组件到窗口
        add(num1Label);
        add(num1Field);
        add(num2Label);
        add(num2Field);
        add(gcdLabel);
        add(gcdField);
        add(lcmLabel);
        add(lcmField);
        add(calculateButton);
        add(exitButton);

        // 为计算按钮添加事件监听器
        calculateButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                calculator();
            }
        });

        // 为退出按钮添加事件监听器
        exitButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                System.exit(0);
            }
        });

        // 设置窗口大小和位置
        setSize(300, 500);
        setLocationRelativeTo(null); // 居中显示
        setResizable(false); // 禁止调整大小
    }

    public static void main(String[] args) {
        // 在事件调度线程中创建和显示GUI
        SwingUtilities.invokeLater(new Runnable() {
            @Override
            public void run() {
                new GCDLCDCalculator().setVisible(true);
            }
        });
    }

    // 计算最大公约数（欧几里得算法）
    private int calculateGCD(int a, int b) {
        a = Math.abs(a);
        b = Math.abs(b);
        while (b != 0) {
            int temp = b;
            b = a % b;
            a = temp;
        }
        return a;
    }

    // 计算最小公倍数
    private int calculateLCM(int a, int b, int gcd) {
        return Math.abs(a * b) / gcd;
    }

    // 执行计算
    private void calculator() {
        try {
            // 获取输入值
            int num1 = Integer.parseInt(num1Field.getText().trim());
            int num2 = Integer.parseInt(num2Field.getText().trim());

            // 检查是否为0
            if (num1 == 0 || num2 == 0) {
                JOptionPane.showMessageDialog(this,
                        "输入的数字不能为零！",
                        "输入错误",
                        JOptionPane.ERROR_MESSAGE);
                return;
            }

            // 计算最大公约数
            int gcd = calculateGCD(num1, num2);

            // 计算最小公倍数
            int lcm = calculateLCM(num1, num2, gcd);

            // 显示结果
            gcdField.setText(String.valueOf(gcd));
            lcmField.setText(String.valueOf(lcm));

        } catch (NumberFormatException ex) {
            JOptionPane.showMessageDialog(this,
                    "请输入有效的整数！",
                    "输入错误",
                    JOptionPane.ERROR_MESSAGE);
            // 清空输入框
            num1Field.setText("");
            num2Field.setText("");
            gcdField.setText("");
            lcmField.setText("");
            // 重新聚焦到第一个输入框
            num1Field.requestFocus();
        }
    }
}
```


