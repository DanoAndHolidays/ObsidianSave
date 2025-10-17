# JSX (JavaScript XML)
JSX是 JavaScript XML（HTML）的缩写，表示在 JS 代码中书写 HTML 结构
优势：
0. 采用类似于HTML的语法，降低学习成本，会HTML就会JSX
1. 充分利用JS自身的可编程能力创建HTML结构
注意：
- JSX 并不是标准的 JS 语法，是 JS 的语法扩展，浏览器默认是不识别的，脚手架中内置的 [@babel/plugin-transform-react-jsx](https://link.juejin.cn?target=%40babel%2Fplugin-transform-react-jsx "@babel/plugin-transform-react-jsx") 包，用来解析该语法。

JSX实际上仅仅是React.createElement(type, config, children)方法的语法糖，该方法接收三个参数：
1. type，当前ReactElement的类型，如果是标签元素，那么使用字符串表示“div”，如果是组件元素直接使用组件的名称就可以。
2. config，我们在JSX中绑定的属性会在config对象中以键值对的形式存在。
3. children，存放标签中的内容，以children数组的形式存储 我们知道JSX是通过babel进行解析的，我们编写JSX需要依赖babel，我们可以在babel官网查看转换的过程 [babeljs.io/repl/#?pres…](https://link.juejin.cn?target=https%3A%2F%2Fbabeljs.io%2Frepl%2F%23%3Fpresets%3Dreact "https://babeljs.io/repl/#?presets=react")

# XML (可扩展标记语言)
## 一、标记语言

标记语言，是一种将文本（Text）以及文本相关的其他信息结合起来，展现出关于文档 结构和数据
处理细节的电脑文字编码。当今广泛使用的标记语言是超文本标记语言.（HyperText Markup Language，HTML）和可扩展标记语言(Extensible Markup Language XML)。标记语言广泛应用于网页和网络应用程序。

**1、超文本标记语言** **HTML**
(1)写法格式： <a href="link.html">link</a>
(2)关注数据的展示与用户体验
(3)标记是预定义、不可扩展的（如 <a></a>表示超链接）

**2、可扩展的标记语言** **XML**
(1)写法格式：同 html 样式
(2)仅关注数据本身
(3)标记可扩展，可自定义

xml 和 Html 语言由同一种父语言 SGML(Standard Generalized Markup Language,标准通用标记语言)发展出来的两种语言。

xml 由 html 发展而来，与 html 格式相似，但是比 html 严格。XML 描述的是结构、内 容和语义，它不描述页面元素的格式化。HTML 侧重于如何表现信息，内容描述与显示 整合为一体。XML 中的每个元素名都是成对出现的，结束标签前加一个/。

![[Pasted image 20251015175238.png]]

![[Pasted image 20251015175548.png]]

## 二、XML 作用

XML 可以用于描述数据、存储数据、传输（交换）数据。XML 现在已经成为一种通用的 数据交换格式,它的平台无关性,语言无关性,系统无关性,给数据集成与交互带来了极大的方便,用户可以定义自己需要的标记。

**1、存储、交换数据**

XML 只用元素和属性来描述数据，而不提供数据的显示方法，这使得 XML 具有能够运 行于不同系统平台之间和转换成不同格式目标文件。 用 XML 在应用程序和公司之间 作数据交换，几个应用程序可以共享和解析同一个 XML 文件，不必使用传统的字符串 解析或拆解过程。

**2、配置**

许多应用都将配置数据存储在各种文件里，如 SSH、Android。使用 XML 配置文件的 应用程序能够方便地处理所需数据，不用像其它应用那样要经过重新编译才能修改和维 护应用系统。xml 比 数据库占用的资源少，操作方便，用来存储简单的信息，现在主要用在程序的配置文件上（比如 web.xml）。现在有越来越多的设备也支持 XML 了。

## 三、XML 示例

用 XML 存储已注册用户的数据方式
```xml
<?xml version="1.0" encoding="UTF-8"?>  
<people>  
	<person>  
		<name>白晶晶</name> 
		<age>28</age>  
	</person>  
	<person>  
		<name>至尊宝</name> 
		<age>300</age> 
	</person> 
</people>
```