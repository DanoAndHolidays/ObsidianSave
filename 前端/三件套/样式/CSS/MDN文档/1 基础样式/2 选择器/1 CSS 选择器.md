# CSS 选择器

- [上一页](https://developer.mozilla.org/zh-CN/docs/Learn_web_development/Core/Styling_basics/Styling_a_bio_page)
- [概述：CSS 构建](https://developer.mozilla.org/zh-CN/docs/Learn_web_development/Core/Styling_basics)
- [下一页](https://developer.mozilla.org/zh-CN/docs/Learn_web_development/Core/Styling_basics/Attribute_selectors)

[CSS](https://developer.mozilla.org/zh-CN/docs/Glossary/CSS)中，选择器用来指定网页上我们想要样式化的[HTML](https://developer.mozilla.org/zh-CN/docs/Glossary/HTML)元素。有 CSS 选择器提供了很多种方法，所以在选择要样式化的元素时，我们可以做到很精细的地步。本文和本文的子篇中，我们将会详细地讲授选择器的不同使用方式，并了解它们的工作原理。

|       |                                                                                                                                                                                                                                                          |
| ----- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 学习前提： | 计算机的基本知识， 安装了基础软件，处理文件的基本知识，HTML 基础（学习[HTML 介绍](https://developer.mozilla.org/zh-CN/docs/Learn_web_development/Core/Structuring_content)）以及对 CSS 工作方式的了解（学习[CSS 初步](https://developer.mozilla.org/zh-CN/docs/Learn_web_development/Core/Styling_basics)） |
| 目标：   | 详细学习 CSS 选择器的工作方式。                                                                                                                                                                                                                                       |
|       |                                                                                                                                                                                                                                                          |

## [选择器是什么？](https://developer.mozilla.org/zh-CN/docs/Learn_web_development/Core/Styling_basics/Basic_selectors#%E9%80%89%E6%8B%A9%E5%99%A8%E6%98%AF%E4%BB%80%E4%B9%88%EF%BC%9F)

你也许已经见过选择器了。CSS 选择器是 CSS 规则的第一部分。它是元素和其他部分组合起来告诉浏览器哪个 HTML 元素应当是被选为应用规则中的 CSS 属性值的方式。选择器所选择的元素，叫做“选择器的对象”。

![Some code with the h1 highlighted.](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Styling_basics/Basic_selectors/selector.png)

前面的文章中，你也许已经遇到过几种不同的选择器，了解到选择器可以以不同的方式选择元素，比如选择诸如`h1`的元素，或者是根据 class (类) 选择例如`.special`。

CSS 中，选择器由 CSS 选择器规范加以定义。就像是 CSS 的其他部分那样，它们需要浏览器的支持才能工作。你会遇到的大多数选择器都是在[CSS 3](https://www.w3.org/TR/selectors-3/)中定义的，这是一个成熟的规范，因此你会发现浏览器对这些选择器有良好的支持。

## [选择器列表](https://developer.mozilla.org/zh-CN/docs/Learn_web_development/Core/Styling_basics/Basic_selectors#%E9%80%89%E6%8B%A9%E5%99%A8%E5%88%97%E8%A1%A8)

如果你有多个使用相同样式的 CSS 选择器，那么这些单独的选择器可以被混编为一个“选择器列表”，这样，规则就可以应用到所有的单个选择器上了。例如，如果我的`h1`和`.special`类有相同的 CSS，那么我可以把它们写成两个分开的规则。

cssCopy

```
h1 {
  color: blue;
}

.special {
  color: blue;
}
```

我也可以将它们组合起来，在它们之间加上一个逗号，变为选择器列表。

cssCopy

```
h1, .special {
  color: blue;
}
```

空格可以在逗号前或后，你可能还会发现如果每个选择器都另起一行，会更好读些。

cssCopy

```
h1,
.special {
  color: blue;
}
```

在下面的实时示例中，试着把两个有相同声明的选择器组合起来。外观在组合起来以后应该还是一样的。

htmlCopy[Play](https://developer.mozilla.org/zh-CN/play?uuid=9a9db9ce5665dc6b2d0846667e6dc97fef69a26e&state=hVI9j9swDP0rhOZcgltTI0sLdO1w6JSFlhlJtUQKpJTAd7j%2FXjg5Z%2BnQTQIf3wfJDxdbye7ohvh6elsqgVEm30RtOMTX05mHejozwG8KIZEBGYzC3eAqY7IdVJXEE8FVDKpY61mAzHqBgiHZ2jpYRT7NErPimOBG2SIIJ%2BHhcC%2FBhGkWBiyoyC1Cw2aSoEnBlnIWKJTX%2Bnuf08o4EjIE1Jz8%2FszDYbX4dPqzl1FgJGoQlIgNvCiDySwwWFPhcCKe0pWGw9cXwr0nSNdpD79QLdOyclnEnKWBl66BWqPNWiUEqyq9GVzwig9LXnJGnTbdCXminIRBZsWV74YzFnoEkz38eAJ8972MpECoLXJvd4VKuD7v1t%2B79zFx%2BjfwW1dOdRNdUFVuoMnT3ZP2hiMGhIHKV27w2HO6ZLmRDgcqJzBCyNRa97QyPnf13MgNGylYTYw%2BAl7F4yTb3hgrgsdxxECAVlExdINb4ka68tWulpEJZsy0h%2B%2BUSReo0rAJmMd8n8FERtpAMVliiKJGilOyuOluyd3OeTN3dKNMC3ysChfh9nLBkvJyBEO2FyNNl29n%2FjzzemQP2Ih%2BDiqdpxcvWfQIC%2BUstwfuzI97eGC%2FAEojeY%2B1a8204aj8D%2BN27s9q0e1ci1TIHV1OITb3%2BRc%3D&srcPrefix=%2Fzh-CN%2Fdocs%2FLearn_web_development%2FCore%2FStyling_basics%2FBasic_selectors%2F)

```
<h1>Type selectors</h1>
<p>
  Veggies es bonus vobis, proinde vos postulo essum magis
  <span>kohlrabi welsh onion</span> daikon amaranth tatsoi tomatillo melon azuki
  bean garlic.
</p>

<p>
  Gumbo beet greens corn soko <strong>endive</strong> gumbo gourd. Parsley
  shallot courgette tatsoi pea sprouts fava bean collard greens dandelion okra
  wakame tomato. Dandelion cucumber earthnut pea peanut soko zucchini.
</p>

<p>
  Turnip greens yarrow ricebean rutabaga <em>endive cauliflower</em> sea lettuce
  kohlrabi amaranth water spinach avocado daikon napa cabbage asparagus winter
  purslane kale. Celery potato scallion desert raisin horseradish spinach
</p>
```

cssCopy[Play](https://developer.mozilla.org/zh-CN/play?uuid=9a9db9ce5665dc6b2d0846667e6dc97fef69a26e&state=hVI9j9swDP0rhOZcgltTI0sLdO1w6JSFlhlJtUQKpJTAd7j%2FXjg5Z%2BnQTQIf3wfJDxdbye7ohvh6elsqgVEm30RtOMTX05mHejozwG8KIZEBGYzC3eAqY7IdVJXEE8FVDKpY61mAzHqBgiHZ2jpYRT7NErPimOBG2SIIJ%2BHhcC%2FBhGkWBiyoyC1Cw2aSoEnBlnIWKJTX%2Bnuf08o4EjIE1Jz8%2FszDYbX4dPqzl1FgJGoQlIgNvCiDySwwWFPhcCKe0pWGw9cXwr0nSNdpD79QLdOyclnEnKWBl66BWqPNWiUEqyq9GVzwig9LXnJGnTbdCXminIRBZsWV74YzFnoEkz38eAJ8972MpECoLXJvd4VKuD7v1t%2B79zFx%2BjfwW1dOdRNdUFVuoMnT3ZP2hiMGhIHKV27w2HO6ZLmRDgcqJzBCyNRa97QyPnf13MgNGylYTYw%2BAl7F4yTb3hgrgsdxxECAVlExdINb4ka68tWulpEJZsy0h%2B%2BUSReo0rAJmMd8n8FERtpAMVliiKJGilOyuOluyd3OeTN3dKNMC3ysChfh9nLBkvJyBEO2FyNNl29n%2FjzzemQP2Ih%2BDiqdpxcvWfQIC%2BUstwfuzI97eGC%2FAEojeY%2B1a8204aj8D%2BN27s9q0e1ci1TIHV1OITb3%2BRc%3D&srcPrefix=%2Fzh-CN%2Fdocs%2FLearn_web_development%2FCore%2FStyling_basics%2FBasic_selectors%2F)

```
body {
  font-family: sans-serif;
}
span {
  background-color: yellow;
}

strong {
  color: rebeccapurple;
}

em {
  color: rebeccapurple;
}
```

[Play](https://developer.mozilla.org/zh-CN/play?uuid=9a9db9ce5665dc6b2d0846667e6dc97fef69a26e&state=hVI9j9swDP0rhOZcgltTI0sLdO1w6JSFlhlJtUQKpJTAd7j%2FXjg5Z%2BnQTQIf3wfJDxdbye7ohvh6elsqgVEm30RtOMTX05mHejozwG8KIZEBGYzC3eAqY7IdVJXEE8FVDKpY61mAzHqBgiHZ2jpYRT7NErPimOBG2SIIJ%2BHhcC%2FBhGkWBiyoyC1Cw2aSoEnBlnIWKJTX%2Bnuf08o4EjIE1Jz8%2FszDYbX4dPqzl1FgJGoQlIgNvCiDySwwWFPhcCKe0pWGw9cXwr0nSNdpD79QLdOyclnEnKWBl66BWqPNWiUEqyq9GVzwig9LXnJGnTbdCXminIRBZsWV74YzFnoEkz38eAJ8972MpECoLXJvd4VKuD7v1t%2B79zFx%2BjfwW1dOdRNdUFVuoMnT3ZP2hiMGhIHKV27w2HO6ZLmRDgcqJzBCyNRa97QyPnf13MgNGylYTYw%2BAl7F4yTb3hgrgsdxxECAVlExdINb4ka68tWulpEJZsy0h%2B%2BUSReo0rAJmMd8n8FERtpAMVliiKJGilOyuOluyd3OeTN3dKNMC3ysChfh9nLBkvJyBEO2FyNNl29n%2FjzzemQP2Ih%2BDiqdpxcvWfQIC%2BUstwfuzI97eGC%2FAEojeY%2B1a8204aj8D%2BN27s9q0e1ci1TIHV1OITb3%2BRc%3D&srcPrefix=%2Fzh-CN%2Fdocs%2FLearn_web_development%2FCore%2FStyling_basics%2FBasic_selectors%2F)

当你使用选择器列表时，如果任何一个选择器无效 (存在语法错误)，那么整条规则都会被忽略。

在下面的示例中，无效的 class 选择器会被忽略，而`h1`选择器仍会被样式化。

cssCopy

```
h1 {
  color: blue;
}

..special {
  color: blue;
}
```

但是在被组合起来以后，整个规则都会失效，无论是`h1`还是这个 class 都不会被样式化。

cssCopy

```
h1,
..special {
  color: blue;
}
```

## [选择器的种类](https://developer.mozilla.org/zh-CN/docs/Learn_web_development/Core/Styling_basics/Basic_selectors#%E9%80%89%E6%8B%A9%E5%99%A8%E7%9A%84%E7%A7%8D%E7%B1%BB)

有几组不同的选择器，知道了需要哪种选择器，你会更容易正确使用它们。在本文的子篇中，我们将会来更详细地看下不同种类的选择器。

### [类型、类和 ID 选择器](https://developer.mozilla.org/zh-CN/docs/Learn_web_development/Core/Styling_basics/Basic_selectors#%E7%B1%BB%E5%9E%8B%E3%80%81%E7%B1%BB%E5%92%8C_id_%E9%80%89%E6%8B%A9%E5%99%A8)

这个选择器组，第一个是指向了所有 HTML 元素 `<h1>`。

cssCopy

```
h1 {
}
```

它也包含了一个 class 的选择器：

cssCopy

```
.box {
}
```

亦或，一个 id 选择器：

cssCopy

```
#unique {
}
```

### [标签属性选择器](https://developer.mozilla.org/zh-CN/docs/Learn_web_development/Core/Styling_basics/Basic_selectors#%E6%A0%87%E7%AD%BE%E5%B1%9E%E6%80%A7%E9%80%89%E6%8B%A9%E5%99%A8)

这组选择器根据一个元素上的某个标签的属性的存在以选择元素的不同方式：

cssCopy

```
a[title] {
}
```

或者根据一个有特定值的标签属性是否存在来选择：

cssCopy

```
a[href="https://example.com"] {
}
```

### [伪类与伪元素](https://developer.mozilla.org/zh-CN/docs/Learn_web_development/Core/Styling_basics/Basic_selectors#%E4%BC%AA%E7%B1%BB%E4%B8%8E%E4%BC%AA%E5%85%83%E7%B4%A0)

这组选择器包含了伪类，用来样式化一个元素的特定状态。例如`:hover`伪类会在鼠标指针悬浮到一个元素上的时候选择这个元素：

cssCopy

```
a:hover {
}
```

它还可以包含了伪元素，选择一个元素的某个部分而不是元素自己。例如，`::first-line`是会选择一个元素（下面的情况中是`<p>`）中的第一行，类似`<span>`包在了第一个被格式化的行外面，然后选择这个`<span>`。

cssCopy

```
p::first-line {
}
```

### [运算符](https://developer.mozilla.org/zh-CN/docs/Learn_web_development/Core/Styling_basics/Basic_selectors#%E8%BF%90%E7%AE%97%E7%AC%A6)

最后一组选择器可以将其他选择器组合起来，更复杂的选择元素。下面的示例用运算符（`>`）选择了`<article>`元素的初代子元素。

cssCopy

```
article > p {
}
```

## [接下来要做的事情](https://developer.mozilla.org/zh-CN/docs/Learn_web_development/Core/Styling_basics/Basic_selectors#%E6%8E%A5%E4%B8%8B%E6%9D%A5%E8%A6%81%E5%81%9A%E7%9A%84%E4%BA%8B%E6%83%85)

你可以看下下面的选择器参考表，可以获得到这个学习章节——或者总体来说是 MDN 上——的各种选择器的直接链接；你也可以继续下去，开始你的了解[类型、类和 ID 选择器](https://developer.mozilla.org/zh-CN/docs/Learn_web_development/Core/Styling_basics/Basic_selectors)的旅程。