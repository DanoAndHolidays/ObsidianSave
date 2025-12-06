# Vue的双向绑定的原理
## Vue底层实现原理
- vue是采用**数据劫持**+**发布者-订阅者模式**的方式
    - 通过`Object.defineProperty()`来劫持各个属性的getter和setter；
    - 在数据变动时，触发set，在set中调用`dep.notify()`方法,发布消息给**订阅者**（订阅者就是Watcher，依赖收集器dep中的subs），做出对应的回调函数，更新视图

## 1. 原理概述
> vue中每个data数据都有一个dep，当获取数据时会在get方法中添加一个新的订阅者，并将订阅者存放到发布者中。当数据发生改变的时候在set方法中调用`dep.notice`方法，让dep中所有的订阅者执行update函数

- 以**数据劫持** + **发布者-订阅者**模式实现，
- 首先通过`Object.defineproperty()`来劫持各属性的`getter`和`setter`，
- 当获取某个属性值时，会触发该属性的 getter，发布者就可以将该属性加入**订阅者的集合管理数组dep**中，
- 当更新某个属性值时，就会触发该属性的setter，发布者可以调用dep.notice()方法，通知订阅者调用**自身的 update()** 方法进行更新，

### （1）简化版：
- Vue2.x
    - 简单来说，就是**数据劫持** + **发布者-订阅者**模式实现，通过`object.defineproperty()`来劫持各属性的`getter`和`setter`，在数据变更时通知订阅者，触发相应的监听回调，实现视图更新。
- Vue3.0
    - vue.js 是采用数据劫持结合发布者-订阅者模式的方式，通过`new Proxy()`来劫持各个属性的setter，getter，在数据变动时发布消息给订阅者，触发相应的监听回调

2与3都是数据劫持+发布者+订阅者的结构，不过底层实现的原理发生了变化
### （2）详细版：
将mvvm作为数据绑定的入口，整合observer、compile、watcher
- 对每个vue属性使用`objecet.defineproperty()`来劫持各属性的getter和setter，每个属性分配一个**订阅者集合管理数组dep**
- 订阅者来自compile，一旦数据改变，通知watcher绑定更新函数，同时**向dep添加订阅者**
- 当dep接到observer变化时，会通知watcher，watcher调用**update()方法**，触发compile绑定的**回调**，视图更新。

### （3）具体版：
- （1）需要 observe 的数据对象进行**递归遍历**，包括子属性对象的属性，都加上 setter 和 getter , 这样的话，给这个对象的某个值赋值，就会触发 setter，那么就能监听到数据变化
    - Observer的核心是通过`Object.defineProprtty()`来监听数据的变动，这个函数内部可以定义`setter和getter`;
    - 每当数据发生变化，就会触发setter。这时候Observer就要通知订阅者，订阅者就是Watcher
- （2）Compile（指令解析器）主要做的事情是解析模板指令
    - **将模板中变量替换成数据**，然后初始化**渲染页面视图**
    - 并将每个指令对应的节点**绑定更新函数**，添加监听数据的订阅者，**一旦数据有变动，收到通知，更新试图**
- （3）Watcher 订阅者是 Observer 和 Compile 之间通信的桥梁，主要做的事情是:
    - 在自身实例化时往`属性订阅器(dep)`里面添加自己
    - 自身必须有一个`update()`方法
    - 待属性变动调用`dep.notice()`通知时，能**调用自身的`update()`方法，并触发`Compile`中绑定的回调
- MVVM作为绑定的入口，整合Observer,Compile和Watcher三者，
    - Observer 来监听自己的 model 数据变化
    - 通过 Compile 来解析编译模板指令
    - 最终利用 Watcher 搭起 Observer 和 Compile 之间的通信桥梁
    - 达到**数据变化Observer=>视图更新**；**视图交互变化=>数据model变更**的双向绑定效果。 ![image.png](https://p6-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/f2e45bb687764d32b1a51af53486b911~tplv-k3u1fbpfcp-jj-mark:3024:0:0:0:q75.awebp#?w=851&h=81&s=10734&e=png&a=1&b=fdfcfc)
## 2. 数据劫持
检测data变化的核心API：`Object.defindeProperty`

`const dep = new Dep(); // 依赖收集器 // 劫持并监听所有属性 Object.defineProperty(obj, key, {     enumerable: true,     configurable: false,     get() {         console.log('触发get');         // 订阅数据变化时，在Dep中添加订阅者         Dep.target && dep.addSub(Dep.target); //用到这个数据的时候就添加监听         return value;     },     set: newVal => {         console.log('触发set');         if (newVal !== value) {             this.observe(newVal);             value = newVal;         }         // 告诉Dep通知变化，通知视图更新...         dep.notify();     } }); //测试 const data = {}; let name = '张三'; console.log(data.name); // 获取数据的时候会触发get  张三 data.name = '李四'; // 赋值的时候会触发set`

这样就是可以实现数据的获取和赋值的监听

## 3. 发布者-订阅者模式⭐⭐⭐⭐⭐
- data中每一个数据都绑定一个Dep，这个Dep中都存有所有用到该数据的**订阅者**
- 当数据改变时，发布消息给dep（依赖收集器），去通知每一个订阅者，做出对应的回调函数

`// 订阅者 class Watcher {     // name模拟使用属性的地方     constructor(name, cb) {         this.name = name         this.cb = cb     }     update() {//更新         console.log(this.name + "更新了");         this.cb() //做出更新回调     } } // 发布者（依赖收集器） class Dep {     constructor() {         this.subs = [] //订阅者     }     // 添加订阅者     addSubs(watcher) {         this.subs.push(watcher)     }     // 当有数据更新时，通知每一个订阅者做出更新     notify() {         this.subs.forEach(w => {             w.update()//每个订阅者Watcher自身有一个update()方法         });     } } // 假如现在用到age的有三个地方 let w1 = new Watcher("我{{age}}了", () => { console.log("更新age"); }) let w2 = new Watcher("v-model:age", () => { console.log("更新age"); }) let w3 = new Watcher("I am {{age}} years old", () => { console.log("更新age"); }) //添加订阅者 let dep = new Dep() dep.addSubs(w1) dep.addSubs(w2) dep.addSubs(w3) // 在Object.defineProperty 中的 set中运行 ☆ dep.notify()`

## [ 延伸问题 ]

### (1) [Vue是如何监听数组的？](https://link.juejin.cn/?target=https%3A%2F%2Fwenku.baidu.com%2Fview%2F3feb2167bd1e650e52ea551810a6f524cdbfcb41.html "https://wenku.baidu.com/view/3feb2167bd1e650e52ea551810a6f524cdbfcb41.html")⭐⭐⭐⭐⭐
- 首先第一点是要看数组里面是不是还存在对象，如果存在对象的话再进行深层遍历看是否还依然存在对象，再把对象进行 `defineProperty监听`。
- 在将数组处理成响应式数据后，如果使用数组原始方法改变数组时，数组值会发生变化，但是并不会触发数组的setter来通知所有依赖该数组的地方进行更新，
- 为此，vue通过**重写**数组的`push、pop、shift、unshift、splice、sort、reverse`七种方法来监听数组变化，重写后的方法中会手动触发通知该数组的所有依赖进行更新。