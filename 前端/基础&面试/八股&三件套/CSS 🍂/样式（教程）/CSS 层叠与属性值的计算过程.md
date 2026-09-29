# CSS 层叠与属性值的计算过程
> Last Format Time：9/18/2026 00:43:42

#渡一

[[💡1 层叠、优先级与继承]]
[MDN：CSS 属性值处理](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_cascade/Value_processing?utm_source=chatgpt.com)
[MDN： CSS层叠](https://developer.mozilla.org/zh-CN/docs/Web/CSS/Guides/Cascade/Introduction?utm_source=chatgpt.com)

所有的CSS属性都必须有值，在浏览器中的计算样式中有，可以看到：
![[Pasted image 20260916225747.png]]

我们需要计算这些属性，这是 CSS 属性值的计算过程，可以直接记成这 6 个阶段：
```text
Declared
↓
Cascaded
↓
Specified
↓
Computed
↓
Used
↓
Actual
```

分别是：
1. **Declared value 声明值** 所有能够匹配到当前元素的合法 CSS 声明
2. **Cascaded value 层叠值** 经过 Cascade 竞争后胜出的那个值，这里会考虑来源（作者、用户与浏览器）、`!important`、cascade layer、specificity、源码顺序等
3. **Specified value 指定值**，如果没有层叠值，补出最终“指定值”：
    - `inherit`
    - initial value （这里就要使用默认值了）
    - 属性是否可继承（有些属性是不可以继承的）
4. **Computed value 计算值** 对值进行进一步计算，例如：
    ```css
    font-size: 2em;
    ```
    
    父元素 `16px`，可能得到：
    ```text
    computed = 32px
    ```
    
    但不是所有值都会在这里变成绝对 px，computed value 仍可能是 `50%`，比如：
    ```css
    width: 50%;
    ```
    
5. **Used value 应用值** 等 Layout 拿到实际布局信息以后再确定。
    ```css
    .parent {
      width: 800px;
    }
    
    .child {
      width: 50%;
    }
    ```
    
    此时：
    ```text
    computed value = 50%
    used value = 400px
    ```
    
6. **Actual value 实际值** 浏览器 / 设备真正能渲染出来的值。
	比如某些亚像素，最终设备可能只能近似显示：
```css
width: 10.333333px;
```
