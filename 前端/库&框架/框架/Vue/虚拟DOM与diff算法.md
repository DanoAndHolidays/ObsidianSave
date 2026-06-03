# 虚拟DOM(基于Vue)
---
DOM操作的速度介于JS原生的API和基于DOM的库(Vue)
优点：
- 减少操作次数：虚拟DOM可以将多个DOM操作合并成一个，减少了操作DOM的次数，以此来增速。
- 减少更新的范围：借助DOM diff来实现更新真正需要更新的DOM
- 跨平台：其本质是JS对象，能够转换为其他的形式。
缺点：
- 使用额外的函数创建，但是可以使用jsx和xml来简化写法。
- 要使用其他的工具再次进行转换为JS

原生的DOM操作本质其实很快，但是浏览器的渲染速度并不能跟上(存在不可交互的时间)

一般情况下，在规模较小时，虚拟DOM更快，在超大规模时，由于虚拟DOM存在额外的优化操作，反而是DOM更快

##### 虚拟 DOM 详解
[补充说明]：虚拟 DOM 的核心概念
```javascript
// 真实 DOM 对象（浏览器原生）
const actualDOM = document.createElement('div');
actualDOM.className = 'container';
actualDOM.innerHTML = 'Hello World';

// 虚拟 DOM 对象（普通 JS 对象）
const virtualDOM = {
    tag: 'div',
    props: { class: 'container' },
    children: ['Hello World']
};

// Vue 3 的虚拟节点（VNode）
const vnode = {
    type: 'div',
    props: { class: 'container' },
    children: 'Hello World',
    el: null, // 对应的真实 DOM 元素
    key: null,
    __v_isVNode: true
};
```
Actual DOM：Browser Native Object
Virtual DOM：Plain JS Object, to represent what the actual DOM should look like

可以使用vue-template-explorer来将template转换为render函数
# DOM diff
---
虚拟DOM对比算法，得到要运行的DOM操作。使用key的原因也和算法有关