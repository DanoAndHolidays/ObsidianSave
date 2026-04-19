# 在 CSS 中调整大小

- [上一页](https://developer.mozilla.org/zh-CN/docs/Learn_web_development/Core/Styling_basics/Values_and_units)
- [概述：CSS 构建](https://developer.mozilla.org/zh-CN/docs/Learn_web_development/Core/Styling_basics)
- [下一页](https://developer.mozilla.org/zh-CN/docs/Learn_web_development/Core/Styling_basics/Backgrounds_and_borders)

在前面的课程中你已经看到了几种使用 CSS 为页面中元素设定尺寸的方法。在我们设计网页的时候，需要理解这些不同方法之间的差异。在本课程中，我们将总结设定元素尺寸的方法，并定义几个术语，这些内容将会在未来对你有所帮助。

|   |   |
|---|---|
|前提：|基本的电脑知识、安装了必要的软件、处理文件的基础知识、HTML 基础（学习[Introduction to HTML](https://developer.mozilla.org/zh-CN/docs/Learn_web_development/Core/Structuring_content)）、理解 CSS 如何工作（学习 [CSS 入门](https://developer.mozilla.org/zh-CN/docs/Learn_web_development/Core/Styling_basics)）。|
|目标：|理解在 CSS 中约束物体大小的不同方式。|

## In this article

- [原始尺寸，或固有尺寸](https://developer.mozilla.org/zh-CN/docs/Learn_web_development/Core/Styling_basics/Sizing#%E5%8E%9F%E5%A7%8B%E5%B0%BA%E5%AF%B8%EF%BC%8C%E6%88%96%E5%9B%BA%E6%9C%89%E5%B0%BA%E5%AF%B8)
- [设置具体的尺寸](https://developer.mozilla.org/zh-CN/docs/Learn_web_development/Core/Styling_basics/Sizing#%E8%AE%BE%E7%BD%AE%E5%85%B7%E4%BD%93%E7%9A%84%E5%B0%BA%E5%AF%B8)
- [min- 和 max- 尺寸](https://developer.mozilla.org/zh-CN/docs/Learn_web_development/Core/Styling_basics/Sizing#min-_%E5%92%8C_max-_%E5%B0%BA%E5%AF%B8)
- [视口单位](https://developer.mozilla.org/zh-CN/docs/Learn_web_development/Core/Styling_basics/Sizing#%E8%A7%86%E5%8F%A3%E5%8D%95%E4%BD%8D)
- [小结](https://developer.mozilla.org/zh-CN/docs/Learn_web_development/Core/Styling_basics/Sizing#%E5%B0%8F%E7%BB%93)

[![Scrimba](https://developer.mozilla.org/pimg/aHR0cHM6Ly9zdGF0aWM0LmJ1eXNlbGxhZHMubmV0L3V1LzIvMTczOTc1LzE3NzU4NTg0NDYtNTAwcHgtbG9nb3Mtd29ybGRvdXRsaW5lLWJhbm5lcl8xXy5wbmc%3D.yB8rNTDy212l%2FnW2U%2FKnRLWFnqZvRVTGydwN%2FC0W%2F24%3D)

**Frontend development career path by Scrimba**A structured program to help you go from beginner to job-ready.Get started

](https://developer.mozilla.org/pong/click?code=aHR0cHM6Ly9zcnYuYnV5c2VsbGFkcy5jb20vYWRzL2NsaWNrL3gvR1RORDQyN1VDWUJJS0szTkY2U0xZS1FVQ0FTSTQySk1DNllJUFozSkNBU0k1SzdFQzZBRDYyN0tDNkFJNjJRN0NUQkRUSzNOQ1RTRDZLSjdDVEJJNFozSkNBU0lLMkpKQ1RBRFRLM0sySldOQUJZ.XcrCE0Ecl3r%2BOsnxRDifIzyU47ww4OGjZX3bXuoa8AA%3D&version=2)[Ad](https://developer.mozilla.org/en-US/advertising)

## [原始尺寸，或固有尺寸](https://developer.mozilla.org/zh-CN/docs/Learn_web_development/Core/Styling_basics/Sizing#%E5%8E%9F%E5%A7%8B%E5%B0%BA%E5%AF%B8%EF%BC%8C%E6%88%96%E5%9B%BA%E6%9C%89%E5%B0%BA%E5%AF%B8)

在受 CSS 设置影响之前，HTML 元素有其原始的尺寸。一个直观的例子就是图像。一幅图像的长和宽由这个图像文件自身确定。这个尺寸就是固有尺寸。

如果你把图片放置在网页中的时候没有在 `<img>` 标签或 CSS 中设置其尺寸，那么将使用其固有尺寸显示。我们给下面的示例图像绘制了一个边框，以便你看出图像文件的长宽。

htmlCopy[Play](https://developer.mozilla.org/zh-CN/play?uuid=b1798aaae9485515ab2ef9cd89a4ff727ccd45ee&state=HcwxDsMgDEDRqyDPSZi60KYnYYFggVsgCDtSpCh3r%2Bj4h%2FcvSFIyGHhRibYq5bKsFlhctzCa%2B7ZaSCKNjdYl1CWSpMMvtGtOrmOYHTMKayouIms8XWkZWXuK8%2FgsrUYLSr9thQk2ZjBAJapr7P3eA3ajHu1UvGcKKrj%2B9fnAp633X3wGgAkkYUEwkCkmgfsH&srcPrefix=%2Fzh-CN%2Fdocs%2FLearn_web_development%2FCore%2FStyling_basics%2FSizing%2F)

```
<img
  alt="star"
  src="https://mdn.github.io/shared-assets/images/examples/big-star.png" />
```

cssCopy[Play](https://developer.mozilla.org/zh-CN/play?uuid=b1798aaae9485515ab2ef9cd89a4ff727ccd45ee&state=HcwxDsMgDEDRqyDPSZi60KYnYYFggVsgCDtSpCh3r%2Bj4h%2FcvSFIyGHhRibYq5bKsFlhctzCa%2B7ZaSCKNjdYl1CWSpMMvtGtOrmOYHTMKayouIms8XWkZWXuK8%2FgsrUYLSr9thQk2ZjBAJapr7P3eA3ajHu1UvGcKKrj%2B9fnAp633X3wGgAkkYUEwkCkmgfsH&srcPrefix=%2Fzh-CN%2Fdocs%2FLearn_web_development%2FCore%2FStyling_basics%2FSizing%2F)

```
img {
  border: 5px solid darkblue;
}
```

[Play](https://developer.mozilla.org/zh-CN/play?uuid=b1798aaae9485515ab2ef9cd89a4ff727ccd45ee&state=HcwxDsMgDEDRqyDPSZi60KYnYYFggVsgCDtSpCh3r%2Bj4h%2FcvSFIyGHhRibYq5bKsFlhctzCa%2B7ZaSCKNjdYl1CWSpMMvtGtOrmOYHTMKayouIms8XWkZWXuK8%2FgsrUYLSr9thQk2ZjBAJapr7P3eA3ajHu1UvGcKKrj%2B9fnAp633X3wGgAkkYUEwkCkmgfsH&srcPrefix=%2Fzh-CN%2Fdocs%2FLearn_web_development%2FCore%2FStyling_basics%2FSizing%2F)

一个空的 [`<div>`](https://developer.mozilla.org/zh-CN/docs/Web/HTML/Reference/Elements/div) 是没有尺寸的。如果你在你的 HTML 文件中添加一个空 [`<div>`](https://developer.mozilla.org/zh-CN/docs/Web/HTML/Reference/Elements/div) 并给予其边框（就像刚才我们为图像做的那样），你会在页面上看到一条线。这是边框被压缩后的效果——它内部没有内容。在我们下面的例子中，边框宽度扩展到整个容器宽度，因为它是块级元素，而块级元素的行为就是这样的。它没有高度，或者说高度为 0，因为内部没有内容。

htmlCopy[Play](https://developer.mozilla.org/zh-CN/play?uuid=4065e2ea5e62380e86458f5a58ddb01187a373dc&state=HcsxDsIwDAXQq1h%2FrmBiSUtP4qWpIxJwExSHKlLVuyN4%2BzsQ26ZwmCTttOpidmf40hnzdJW0z5wxYDWDw8WXTgdnIl%2BqhOro9u5kRZOQLPXl9RNGzue%2FPH8DA1oMW4CDpkdsOL8%3D&srcPrefix=%2Fzh-CN%2Fdocs%2FLearn_web_development%2FCore%2FStyling_basics%2FSizing%2F)

```
<div class="box"></div>
```

cssCopy[Play](https://developer.mozilla.org/zh-CN/play?uuid=4065e2ea5e62380e86458f5a58ddb01187a373dc&state=HcsxDsIwDAXQq1h%2FrmBiSUtP4qWpIxJwExSHKlLVuyN4%2BzsQ26ZwmCTttOpidmf40hnzdJW0z5wxYDWDw8WXTgdnIl%2BqhOro9u5kRZOQLPXl9RNGzue%2FPH8DA1oMW4CDpkdsOL8%3D&srcPrefix=%2Fzh-CN%2Fdocs%2FLearn_web_development%2FCore%2FStyling_basics%2FSizing%2F)

```
.box {
  border: 5px solid darkblue;
}
```

[Play](https://developer.mozilla.org/zh-CN/play?uuid=4065e2ea5e62380e86458f5a58ddb01187a373dc&state=HcsxDsIwDAXQq1h%2FrmBiSUtP4qWpIxJwExSHKlLVuyN4%2BzsQ26ZwmCTttOpidmf40hnzdJW0z5wxYDWDw8WXTgdnIl%2BqhOro9u5kRZOQLPXl9RNGzue%2FPH8DA1oMW4CDpkdsOL8%3D&srcPrefix=%2Fzh-CN%2Fdocs%2FLearn_web_development%2FCore%2FStyling_basics%2FSizing%2F)

在上面的例子中，试着在空元素内部添加些内容。现在边框内包含一些文字了，因为元素的高度由其所含内容高度确定。再强调一次，这就是元素的固有尺寸——由其所包含的内容决定。

## [设置具体的尺寸](https://developer.mozilla.org/zh-CN/docs/Learn_web_development/Core/Styling_basics/Sizing#%E8%AE%BE%E7%BD%AE%E5%85%B7%E4%BD%93%E7%9A%84%E5%B0%BA%E5%AF%B8)

我们当然可以给设计中的元素指定具体大小。当给元素指定尺寸（然后其内容需要适合该尺寸）时，我们将其称为**外部尺寸**。以上面例子中的 `<div>` 举例——我们可以给它一个具体的 [`width`](https://developer.mozilla.org/zh-CN/docs/Web/CSS/Reference/Properties/width) 和 [`height`](https://developer.mozilla.org/zh-CN/docs/Web/CSS/Reference/Properties/height) 值，然后不论我们放什么内容进去它都是该尺寸。正如我们在[上一课](https://developer.mozilla.org/zh-CN/docs/Learn_web_development/Core/Styling_basics/Overflow)有关溢出的内容中所发现的，如果内容的数量超出了元素可容纳的空间，则设置的高度会导致内容溢出。

htmlCopy[Play](https://developer.mozilla.org/zh-CN/play?uuid=624d8811e3fe17dbe7b62d0e5550d99bb936091f&state=dZDLbsMgEEV%2F5WqWlZsmkbohab6iS2%2BwGRtaDBZDbUdR%2Fr0iTl%2BLrpA4Z67mzoVsHjwpOho3ofVa5KWmOelx5FTTqQ7AH9TEpabT8cm46T9YvoFXy8Jo4sKCJmYLqyeGhmXX2wzhXCFbV%2BACqwVtDJlDhgtwGbN1rcXsvF%2FjArPBEBNDRt0ystUB2TK0iOsDm3twBR0MJGJm9JwRJ06dj%2FPmtux97a%2BXKmpFSFETzRmXonQxZIXdZs8DRAd5FE6uO9ThWofN%2FS6raZyMXp8VOs%2FLKvxSTnhYtUGn3gWF%2FXb8sUrnG21iMpwUnscFEr0zMDq9N%2F6DDwWvnRR223UamJ3JtqR9x1FFb6UDVZQtD0yKfJmi6yc%3D&srcPrefix=%2Fzh-CN%2Fdocs%2FLearn_web_development%2FCore%2FStyling_basics%2FSizing%2F)

```
<div class="wrapper">
  <div class="box"></div>
  <div class="box">
    These boxes both have a height set, this box has content in it which will
    need more space than the assigned height, and so we get overflow.
  </div>
</div>
```

cssCopy[Play](https://developer.mozilla.org/zh-CN/play?uuid=624d8811e3fe17dbe7b62d0e5550d99bb936091f&state=dZDLbsMgEEV%2F5WqWlZsmkbohab6iS2%2BwGRtaDBZDbUdR%2Fr0iTl%2BLrpA4Z67mzoVsHjwpOho3ofVa5KWmOelx5FTTqQ7AH9TEpabT8cm46T9YvoFXy8Jo4sKCJmYLqyeGhmXX2wzhXCFbV%2BACqwVtDJlDhgtwGbN1rcXsvF%2FjArPBEBNDRt0ystUB2TK0iOsDm3twBR0MJGJm9JwRJ06dj%2FPmtux97a%2BXKmpFSFETzRmXonQxZIXdZs8DRAd5FE6uO9ThWofN%2FS6raZyMXp8VOs%2FLKvxSTnhYtUGn3gWF%2FXb8sUrnG21iMpwUnscFEr0zMDq9N%2F6DDwWvnRR223UamJ3JtqR9x1FFb6UDVZQtD0yKfJmi6yc%3D&srcPrefix=%2Fzh-CN%2Fdocs%2FLearn_web_development%2FCore%2FStyling_basics%2FSizing%2F)

```
body {
  font: 1.2em sans-serif;
}
.wrapper {
  display: flex;
}

.wrapper > * {
  margin: 20px;
}

.box {
  border: 5px solid darkblue;
  height: 100px;
  width: 200px;
}
```

[Play](https://developer.mozilla.org/zh-CN/play?uuid=624d8811e3fe17dbe7b62d0e5550d99bb936091f&state=dZDLbsMgEEV%2F5WqWlZsmkbohab6iS2%2BwGRtaDBZDbUdR%2Fr0iTl%2BLrpA4Z67mzoVsHjwpOho3ofVa5KWmOelx5FTTqQ7AH9TEpabT8cm46T9YvoFXy8Jo4sKCJmYLqyeGhmXX2wzhXCFbV%2BACqwVtDJlDhgtwGbN1rcXsvF%2FjArPBEBNDRt0ystUB2TK0iOsDm3twBR0MJGJm9JwRJ06dj%2FPmtux97a%2BXKmpFSFETzRmXonQxZIXdZs8DRAd5FE6uO9ThWofN%2FS6raZyMXp8VOs%2FLKvxSTnhYtUGn3gWF%2FXb8sUrnG21iMpwUnscFEr0zMDq9N%2F6DDwWvnRR223UamJ3JtqR9x1FFb6UDVZQtD0yKfJmi6yc%3D&srcPrefix=%2Fzh-CN%2Fdocs%2FLearn_web_development%2FCore%2FStyling_basics%2FSizing%2F)

由于存在溢出问题，在网络上使用长度或百分比固定元素的高度需要非常小心。

### [使用百分比](https://developer.mozilla.org/zh-CN/docs/Learn_web_development/Core/Styling_basics/Sizing#%E4%BD%BF%E7%94%A8%E7%99%BE%E5%88%86%E6%AF%94)

许多时候，百分比是长度单位，正如我们在[值和单位这节课中讨论的那样](https://developer.mozilla.org/zh-CN/docs/Learn_web_development/Core/Styling_basics/Values_and_units#%E7%99%BE%E5%88%86%E6%AF%94)，它们常常可与长度互换。当使用百分比时，你需要清楚，它是**什么**东西的百分比。对于一个处于另外一个容器当中的盒子，如果你给予了子盒子一个百分比作为宽度，那么它指的是父容器宽度的百分比。

htmlCopy[Play](https://developer.mozilla.org/zh-CN/play?uuid=a6e369ccbaa9137c0b1ef0283f5b8a7873ba1df9&state=JY3LDoIwEAB%2FZbOJN8RHwqUod%2F%2Bhl5YutFq2pK2IIfy7Qc4zk1nQ5sGjwJtxE7RepXSXqMMssXmAVROBgpFiS5xVT%2FBxJtvydjJuaiRjgW1KKFAH84VFMkAXOAu4lFcaIClOx0TRdbXkVbLkUod593SIhqKAapwhBe8MGBVf2r%2Bp3vD%2FI6A6H%2FYUC3xuIywwWxoIBXrX24zrDw%3D%3D&srcPrefix=%2Fzh-CN%2Fdocs%2FLearn_web_development%2FCore%2FStyling_basics%2FSizing%2F)

```
<div class="box">I have a percentage width.</div>
```

cssCopy[Play](https://developer.mozilla.org/zh-CN/play?uuid=a6e369ccbaa9137c0b1ef0283f5b8a7873ba1df9&state=JY3LDoIwEAB%2FZbOJN8RHwqUod%2F%2Bhl5YutFq2pK2IIfy7Qc4zk1nQ5sGjwJtxE7RepXSXqMMssXmAVROBgpFiS5xVT%2FBxJtvydjJuaiRjgW1KKFAH84VFMkAXOAu4lFcaIClOx0TRdbXkVbLkUod593SIhqKAapwhBe8MGBVf2r%2Bp3vD%2FI6A6H%2FYUC3xuIywwWxoIBXrX24zrDw%3D%3D&srcPrefix=%2Fzh-CN%2Fdocs%2FLearn_web_development%2FCore%2FStyling_basics%2FSizing%2F)

```
body {
  font: 1.2em sans-serif;
}

.box {
  border: 5px solid darkblue;
  width: 50%;
}
```

[Play](https://developer.mozilla.org/zh-CN/play?uuid=a6e369ccbaa9137c0b1ef0283f5b8a7873ba1df9&state=JY3LDoIwEAB%2FZbOJN8RHwqUod%2F%2Bhl5YutFq2pK2IIfy7Qc4zk1nQ5sGjwJtxE7RepXSXqMMssXmAVROBgpFiS5xVT%2FBxJtvydjJuaiRjgW1KKFAH84VFMkAXOAu4lFcaIClOx0TRdbXkVbLkUod593SIhqKAapwhBe8MGBVf2r%2Bp3vD%2FI6A6H%2FYUC3xuIywwWxoIBXrX24zrDw%3D%3D&srcPrefix=%2Fzh-CN%2Fdocs%2FLearn_web_development%2FCore%2FStyling_basics%2FSizing%2F)

这是因为百分比是以包含盒子的块为根据解析的。如果我们的 `<div>` 没有被指定百分比的值，那么它会占据 100% 的可用空间，因为它是块级别的元素。如果我们给了它一个百分比作为宽度，那么这就是它原来情况下可以占据空间的百分比。

### [把百分比作为内外边距](https://developer.mozilla.org/zh-CN/docs/Learn_web_development/Core/Styling_basics/Sizing#%E6%8A%8A%E7%99%BE%E5%88%86%E6%AF%94%E4%BD%9C%E4%B8%BA%E5%86%85%E5%A4%96%E8%BE%B9%E8%B7%9D)

如果你把 `margins` 和 `padding` 设置为百分比的话，你会注意到一些奇怪的表现。在下面的例子里，我们有一个盒子，我们给了里面的盒子 10% 的 [`margin`](https://developer.mozilla.org/zh-CN/docs/Web/CSS/Reference/Properties/margin) 以及 10% 的 [`padding`](https://developer.mozilla.org/zh-CN/docs/Web/CSS/Reference/Properties/padding)。盒子底部和顶部的内外边距，和左右外边距有同样的大小。

htmlCopy[Play](https://developer.mozilla.org/zh-CN/play?uuid=b4f3d0e1d6b90bfb1bf7081079495b98f4f290ad&state=Nc5NbsIwEAXgqzyN1B1NA1I3hrLvHbyxGRO7dcZRxg1BKHevEtrl%2B1l8D4q1z2ToxGnCJTvVD0u%2BzJbOn4huCujd2CWBE8bgmJN00FBRC%2FbtC4rA5QxNHLQ5vXGazlZoRxdVMuQL3%2FGwAlyLVIN9cwg91Im%2BahjT9WhlsdL4Mj9fvowcRoP3YYaWnBjsxm%2Bff8JxnW%2BJazQ4tO0wb8XTZlbJlv%2BA%2F8WyUb5WCe2oxtAHMpRTFystvw%3D%3D&srcPrefix=%2Fzh-CN%2Fdocs%2FLearn_web_development%2FCore%2FStyling_basics%2FSizing%2F)

```
<div class="box">I have margin and padding set to 10% on all sides.</div>
```

cssCopy[Play](https://developer.mozilla.org/zh-CN/play?uuid=b4f3d0e1d6b90bfb1bf7081079495b98f4f290ad&state=Nc5NbsIwEAXgqzyN1B1NA1I3hrLvHbyxGRO7dcZRxg1BKHevEtrl%2B1l8D4q1z2ToxGnCJTvVD0u%2BzJbOn4huCujd2CWBE8bgmJN00FBRC%2FbtC4rA5QxNHLQ5vXGazlZoRxdVMuQL3%2FGwAlyLVIN9cwg91Im%2BahjT9WhlsdL4Mj9fvowcRoP3YYaWnBjsxm%2Bff8JxnW%2BJazQ4tO0wb8XTZlbJlv%2BA%2F8WyUb5WCe2oxtAHMpRTFystvw%3D%3D&srcPrefix=%2Fzh-CN%2Fdocs%2FLearn_web_development%2FCore%2FStyling_basics%2FSizing%2F)

```
body {
  font: 1.2em sans-serif;
}
.box {
  border: 5px solid darkblue;
  width: 200px;
  margin: 10%;
  padding: 10%;
}
```

[Play](https://developer.mozilla.org/zh-CN/play?uuid=b4f3d0e1d6b90bfb1bf7081079495b98f4f290ad&state=Nc5NbsIwEAXgqzyN1B1NA1I3hrLvHbyxGRO7dcZRxg1BKHevEtrl%2B1l8D4q1z2ToxGnCJTvVD0u%2BzJbOn4huCujd2CWBE8bgmJN00FBRC%2FbtC4rA5QxNHLQ5vXGazlZoRxdVMuQL3%2FGwAlyLVIN9cwg91Im%2BahjT9WhlsdL4Mj9fvowcRoP3YYaWnBjsxm%2Bff8JxnW%2BJazQ4tO0wb8XTZlbJlv%2BA%2F8WyUb5WCe2oxtAHMpRTFystvw%3D%3D&srcPrefix=%2Fzh-CN%2Fdocs%2FLearn_web_development%2FCore%2FStyling_basics%2FSizing%2F)

或许，你期望元素的上下外边距是其高度的百分比，元素的左右外边距是其宽度的百分比。但情况并非如此！

使用百分比作为元素外边距（margin）或填充（padding）的单位时，值是以包含块的**内联尺寸**进行计算的，也就是元素的水平宽度。在我们的示例中，所有的外边距或填充都是宽度的 10%。请记住一个事实，当你使用百分比作为元素外边距或填充的单位时，你将得到一个相同尺寸的外边距或填充。

## [min- 和 max- 尺寸](https://developer.mozilla.org/zh-CN/docs/Learn_web_development/Core/Styling_basics/Sizing#min-_%E5%92%8C_max-_%E5%B0%BA%E5%AF%B8)

除了让万物都有一个确定的大小以外，我们可以让 CSS 给定一个元素的最大或最小尺寸。如果你有一个包含了变化容量的内容的盒子，而且你总是想让它**至少**有个确定的高度，你应该给它设置一个 [`min-height`](https://developer.mozilla.org/zh-CN/docs/Web/CSS/Reference/Properties/min-height) 属性。盒子就会一直保持大于这个最小高度，但是如果有比这个盒子在最小高度状态下所能容纳的更多内容，那么盒子就会变大。

在以下的示例中，你可以看到两个盒子，两个都有 150 像素的确定高度，左边的盒子有 150 像素高，右边的盒子有需要更多空间才能装下的内容，所以它变得比 150 像素高。

htmlCopy[Play](https://developer.mozilla.org/zh-CN/play?uuid=fa0ae17f0b9dfe0e72d7501ed093f7f64d3ca317&state=dZDNTsMwEIRfZbRHlJZSiUsKfQqOuTjxNl7wT%2BR126CKd0duoMCBk6XZmc%2B7cyFXgqeWnqycMHij%2BtzROZtp4tzRvovAn1Gf5o72T%2FdWTv8Nqwy8OFZGn2ZW9Kk4OHNiGASJK8cyugLl0qA4qYYZziiGFAvHAomQgrOTwS20s3iPyGwRUmboZAZGcSaiOIZRlTGyxQJuYKKFpsoYczorDjmF6lxgQaKEY1hf9%2F%2B65PulhgZVaqlP9h2XajmkWFo8rLccoCbqSjnLYdfFjy6uv6panFZ08ua9xcHzvKuK8TLGlRQOuqgrLSaXJfwrvsfdgggmjxJbbDfTfHPVeq7TPmXLucXjNEOTFwtr8lvvj3z97afbFg%2BbhVC7s8VV4g1JDb3WG6mh4jgwteRrij4%2BAQ%3D%3D&srcPrefix=%2Fzh-CN%2Fdocs%2FLearn_web_development%2FCore%2FStyling_basics%2FSizing%2F)

```
<div class="wrapper">
  <div class="box"></div>
  <div class="box">
    These boxes both have a min-height set, this box has content in it which
    will need more space than the assigned height, and so it grows from the
    minimum.
  </div>
</div>
```

cssCopy[Play](https://developer.mozilla.org/zh-CN/play?uuid=fa0ae17f0b9dfe0e72d7501ed093f7f64d3ca317&state=dZDNTsMwEIRfZbRHlJZSiUsKfQqOuTjxNl7wT%2BR126CKd0duoMCBk6XZmc%2B7cyFXgqeWnqycMHij%2BtzROZtp4tzRvovAn1Gf5o72T%2FdWTv8Nqwy8OFZGn2ZW9Kk4OHNiGASJK8cyugLl0qA4qYYZziiGFAvHAomQgrOTwS20s3iPyGwRUmboZAZGcSaiOIZRlTGyxQJuYKKFpsoYczorDjmF6lxgQaKEY1hf9%2F%2B65PulhgZVaqlP9h2XajmkWFo8rLccoCbqSjnLYdfFjy6uv6panFZ08ua9xcHzvKuK8TLGlRQOuqgrLSaXJfwrvsfdgggmjxJbbDfTfHPVeq7TPmXLucXjNEOTFwtr8lvvj3z97afbFg%2BbhVC7s8VV4g1JDb3WG6mh4jgwteRrij4%2BAQ%3D%3D&srcPrefix=%2Fzh-CN%2Fdocs%2FLearn_web_development%2FCore%2FStyling_basics%2FSizing%2F)

```
body {
  font: 1.2em sans-serif;
}
.wrapper {
  display: flex;
  align-items: flex-start;
}

.wrapper > * {
  margin: 20px;
}

.box {
  border: 5px solid darkblue;
  min-height: 100px;
  width: 200px;
}
```

[Play](https://developer.mozilla.org/zh-CN/play?uuid=fa0ae17f0b9dfe0e72d7501ed093f7f64d3ca317&state=dZDNTsMwEIRfZbRHlJZSiUsKfQqOuTjxNl7wT%2BR126CKd0duoMCBk6XZmc%2B7cyFXgqeWnqycMHij%2BtzROZtp4tzRvovAn1Gf5o72T%2FdWTv8Nqwy8OFZGn2ZW9Kk4OHNiGASJK8cyugLl0qA4qYYZziiGFAvHAomQgrOTwS20s3iPyGwRUmboZAZGcSaiOIZRlTGyxQJuYKKFpsoYczorDjmF6lxgQaKEY1hf9%2F%2B65PulhgZVaqlP9h2XajmkWFo8rLccoCbqSjnLYdfFjy6uv6panFZ08ua9xcHzvKuK8TLGlRQOuqgrLSaXJfwrvsfdgggmjxJbbDfTfHPVeq7TPmXLucXjNEOTFwtr8lvvj3z97afbFg%2BbhVC7s8VV4g1JDb3WG6mh4jgwteRrij4%2BAQ%3D%3D&srcPrefix=%2Fzh-CN%2Fdocs%2FLearn_web_development%2FCore%2FStyling_basics%2FSizing%2F)

这在避免溢出的同时并处理变化容量的内容的时候是很有用的。

[`max-width`](https://developer.mozilla.org/zh-CN/docs/Web/CSS/Reference/Properties/max-width) 的常见用法为，在没有足够空间以原有宽度展示图像时，让图像缩小，同时确保它们不会比这一宽度大。

作为示例，如果你设定一个图像的属性为 `width: 100%`，而且它的原始宽度小于容器，图像会被强制拉伸以变大，看起来像素更加明显。如果它的原始宽度大于容器，它则会溢出。两种情形都不是你想要看到的。

如果你使用了 `max-width: 100%`，那么图像可以变得比原始尺寸更小，但是不会大于原始尺寸的 100%。

在下面的示例里，我们使用了两次相同的图片。第一次使用，属性值已设为 `width: 100%`，位于比图片大的容器里，因此图片拉伸到了与容器相同的宽度；第二次的属性值则设为 `max-width: 100%`，因此它并没有拉伸到充满容器；第三个盒子再一次包含了相同的图片，同时设定了 `max-width: 100%` 属性，这时你能看到它是怎样缩小来和盒子大小相适应的。

htmlCopy[Play](https://developer.mozilla.org/zh-CN/play?uuid=24ec69d187f03d6c1be8c56c832a827d58914fee&state=zVLNTsMwDH4VyxIX1DYDaZeO7UlySZeQGpI0irMRNO3dUde10%2BCKEKdE358%2FWT5hn73DFl80HWHvFPNW4kdSMZokcScDwB3VDeUKA7yQt9MPQLm8lchZJYkztsSRzv0N5rTfSuxzjtwK4XVoLOX%2B0DU0CO5VMrpWzCazIK%2BsYWGK8tEZFh3ZehzRxGAlgpjqCU3H3ynqVfnrmp4C1f%2B16%2FxihXtmbLG5XgacRpkmjk59tvDqTNmMiHJkQ03ZeJ7QS3beyHCWQYbFvoPHKcKrZCm08LyKZVF1Q6lkaObVTMpuSNqkFtaxAA%2BONGiV3jt3MJOvWZSXcxsjl8xvUVfB%2BsZfkDvyabV6mM2qzGVL%2FYPGCt%2FG1WCFuTfeYIuObJ%2Fx%2FAU%3D&srcPrefix=%2Fzh-CN%2Fdocs%2FLearn_web_development%2FCore%2FStyling_basics%2FSizing%2F)

```
<div class="wrapper">
  <div class="box">
    <img
      alt="star"
      class="width"
      src="https://mdn.github.io/shared-assets/images/examples/big-star.png" />
  </div>
  <div class="box">
    <img
      alt="star"
      class="max"
      src="https://mdn.github.io/shared-assets/images/examples/big-star.png" />
  </div>
  <div class="mini-box">
    <img
      alt="star"
      class="max"
      src="https://mdn.github.io/shared-assets/images/examples/big-star.png" />
  </div>
</div>
```

cssCopy[Play](https://developer.mozilla.org/zh-CN/play?uuid=24ec69d187f03d6c1be8c56c832a827d58914fee&state=zVLNTsMwDH4VyxIX1DYDaZeO7UlySZeQGpI0irMRNO3dUde10%2BCKEKdE358%2FWT5hn73DFl80HWHvFPNW4kdSMZokcScDwB3VDeUKA7yQt9MPQLm8lchZJYkztsSRzv0N5rTfSuxzjtwK4XVoLOX%2B0DU0CO5VMrpWzCazIK%2BsYWGK8tEZFh3ZehzRxGAlgpjqCU3H3ynqVfnrmp4C1f%2B16%2FxihXtmbLG5XgacRpkmjk59tvDqTNmMiHJkQ03ZeJ7QS3beyHCWQYbFvoPHKcKrZCm08LyKZVF1Q6lkaObVTMpuSNqkFtaxAA%2BONGiV3jt3MJOvWZSXcxsjl8xvUVfB%2BsZfkDvyabV6mM2qzGVL%2FYPGCt%2FG1WCFuTfeYIuObJ%2Fx%2FAU%3D&srcPrefix=%2Fzh-CN%2Fdocs%2FLearn_web_development%2FCore%2FStyling_basics%2FSizing%2F)

```
.box {
  width: 200px;
}
.mini-box {
  width: 50px;
}
.width {
  width: 100%;
}
.max {
  max-width: 100%;
}
```

[Play](https://developer.mozilla.org/zh-CN/play?uuid=24ec69d187f03d6c1be8c56c832a827d58914fee&state=zVLNTsMwDH4VyxIX1DYDaZeO7UlySZeQGpI0irMRNO3dUde10%2BCKEKdE358%2FWT5hn73DFl80HWHvFPNW4kdSMZokcScDwB3VDeUKA7yQt9MPQLm8lchZJYkztsSRzv0N5rTfSuxzjtwK4XVoLOX%2B0DU0CO5VMrpWzCazIK%2BsYWGK8tEZFh3ZehzRxGAlgpjqCU3H3ynqVfnrmp4C1f%2B16%2FxihXtmbLG5XgacRpkmjk59tvDqTNmMiHJkQ03ZeJ7QS3beyHCWQYbFvoPHKcKrZCm08LyKZVF1Q6lkaObVTMpuSNqkFtaxAA%2BONGiV3jt3MJOvWZSXcxsjl8xvUVfB%2BsZfkDvyabV6mM2qzGVL%2FYPGCt%2FG1WCFuTfeYIuObJ%2Fx%2FAU%3D&srcPrefix=%2Fzh-CN%2Fdocs%2FLearn_web_development%2FCore%2FStyling_basics%2FSizing%2F)

这个技术是用来让图片**可响应**的，所以在更小的设备上浏览的时候，它们会合适地缩放。你无论怎样都不应该用这个技术先载入大原始尺寸的图片，再对它们在浏览器中进行缩放。图像应该合适地调整尺寸，以使它们不会比预计中展示时所需要的最大尺寸大。下载过大的图像会造成你的网站变慢，如果用户使用按量收费的网络连接，会让用户花更多钱。

**备注：**了解更多关于[响应式图片技术](https://developer.mozilla.org/zh-CN/docs/Web/HTML/Guides/Responsive_images)的事情。

## [视口单位](https://developer.mozilla.org/zh-CN/docs/Learn_web_development/Core/Styling_basics/Sizing#%E8%A7%86%E5%8F%A3%E5%8D%95%E4%BD%8D)

视口，即你在浏览器中看到的部分页面，也是有尺寸的。在 CSS 中，我们有与视口尺寸相关的度量单位，即意为视口宽度的 `vw` 单位，以及意为视口高度的 `vh` 单位。使用这些单位，你可以把一些东西做得随用户的视口改变大小。

`1vh` 等于视口高度的 1%，`1vw` 则为视口宽度的 1%。你可以用这些单位约束盒子的大小，还有文字的大小。在下面的示例里，我们有一个大小被设为 20vh 和 20vw 的盒子。这个盒子里面有一个字母 `A`，其 [`font-size`](https://developer.mozilla.org/zh-CN/docs/Web/CSS/Reference/Properties/font-size) 属性被设成了 10vh。

htmlCopy[Play](https://developer.mozilla.org/zh-CN/play?uuid=6b13a444211487418d4c45f1a682460ff69cb201&state=PY5LDoMwEEOvMpo19Cd1EyhS75ENIaGZNiRVJuVTxN0rQOrSz7bsGW3qHAosNfXQuJr5JlGFUWJ1L4%2Ba%2Bkp6zLBhRoEq6Alm6QHa4FPe1h25SQDXnnM2kdpC%2BkV66Q8qjHtQhahNFHB9j8DBkQZdx5dyH1Os9kA6WQGXUz9s2hp62LQBW%2FyHmL5GwHlny3bouf7BDJM1nUGBbu3h8gM%3D&srcPrefix=%2Fzh-CN%2Fdocs%2FLearn_web_development%2FCore%2FStyling_basics%2FSizing%2F)

```
<div class="box">A</div>
```

cssCopy[Play](https://developer.mozilla.org/zh-CN/play?uuid=6b13a444211487418d4c45f1a682460ff69cb201&state=PY5LDoMwEEOvMpo19Cd1EyhS75ENIaGZNiRVJuVTxN0rQOrSz7bsGW3qHAosNfXQuJr5JlGFUWJ1L4%2Ba%2Bkp6zLBhRoEq6Alm6QHa4FPe1h25SQDXnnM2kdpC%2BkV66Q8qjHtQhahNFHB9j8DBkQZdx5dyH1Os9kA6WQGXUz9s2hp62LQBW%2FyHmL5GwHlny3bouf7BDJM1nUGBbu3h8gM%3D&srcPrefix=%2Fzh-CN%2Fdocs%2FLearn_web_development%2FCore%2FStyling_basics%2FSizing%2F)

```
body {
  font-family: sans-serif;
}

.box {
  border: 5px solid darkblue;
  width: 20vw;
  height: 20vh;
  font-size: 10vh;
}
```

[Play](https://developer.mozilla.org/zh-CN/play?uuid=6b13a444211487418d4c45f1a682460ff69cb201&state=PY5LDoMwEEOvMpo19Cd1EyhS75ENIaGZNiRVJuVTxN0rQOrSz7bsGW3qHAosNfXQuJr5JlGFUWJ1L4%2Ba%2Bkp6zLBhRoEq6Alm6QHa4FPe1h25SQDXnnM2kdpC%2BkV66Q8qjHtQhahNFHB9j8DBkQZdx5dyH1Os9kA6WQGXUz9s2hp62LQBW%2FyHmL5GwHlny3bouf7BDJM1nUGBbu3h8gM%3D&srcPrefix=%2Fzh-CN%2Fdocs%2FLearn_web_development%2FCore%2FStyling_basics%2FSizing%2F)

如果你改变了 `vh` 和 `vw` 的对应值，盒子和字体的大小也会改变；视口大小的变化也会让它们的大小变化，因为它们是依照视口来定大小的。想看到随着你改变视口大小的时候示例的变化的话，你需要在一个新浏览器视窗里面载入此示例，因为你可以控制该视窗的大小，同时上面示例所在的嵌入的 `<iframe>` 的大小即是对上面示例而言的视口。[打开此示例](https://mdn.github.io/css-examples/learn/sizing/vw-vh.html)，调整浏览器视窗的大小，观察在盒子和文本的大小上所发生的事情。

在你的设计中，根据视口改变物件的大小是很有用的。例如，如果你想要在你其他内容之前，有一个充满整个视口的视觉宣传段落，让你的页面的那个部分有 100vh 高的话，会把剩下的内容推到视口的下面，只有向下滚动文档的时候它们才会出现。

## [小结](https://developer.mozilla.org/zh-CN/docs/Learn_web_development/Core/Styling_basics/Sizing#%E5%B0%8F%E7%BB%93)

本节课，你已经得到了一个对于你可能在约束网站上的内容大小的时候，会遇到的一些关键问题的详细介绍。当你继续学习 [CSS 布局](https://developer.mozilla.org/zh-CN/docs/Learn_web_development/Core/CSS_layout)的时候，约束大小会成为掌握不同布局途径的非常重要的基础，所以在继续之前有必要在这里理解这些概念。