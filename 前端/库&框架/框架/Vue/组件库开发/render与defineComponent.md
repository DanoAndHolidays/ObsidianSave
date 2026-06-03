```javascript
import { defineComponent, h } from 'vue'

const MyComponent = defineComponent({
    name: 'MyComponent',
    props: {
        msg: {
            type: String,
            required: true,
        },
    },
    data() {
        return {
            testNum: 1,
        }
    },
    render() {
        return h('div', this.msg) // 使用 h 函数来创建虚拟 DOM
    },
})

export default MyComponent
```

```javascript
import { h } from 'vue'

export default {
    name: 'MyComponent',
    props: {
        msg: {
            type: String,
            // required: true,
        },
    },
    data() {
        return {
            testNum: 1,
        }
    },
    render() {
        return h('div', this.testNum) // 使用 h 函数来创建虚拟 DOM
    },
}
```
`defineComponent` 提供了更好的开发体验和类型推导，尤其是在 TypeScript 中，而不使用 `defineComponent` 的写法则是一种更简洁的传统方式，两者在功能上并没有本质差异，只是后者缺乏一些 Vue 3 的类型支持和开发便利

在template中使用组件要在components中：
```javascript
import MyComp from '/src/test_render_function_component.js'
import MyComp2 from '/src/test2.js'
export default {
    methods: {
        printff() {
            this.count++
            console.log(this.count)
        },
    },
    data() {
        return {
            count: 3,
            msg: 'Hello World',
        }
    },
    computed: {
        double() {
            return this.count * 2
        },
    },
    template: /*html*/ `
          <div>{{ double }}</div>
          <button @click="printff">click me</button>
          <MyComp :msg="msg"/>
          <MyComp2 />
        `,
    components: {
        MyComp,
        MyComp2,
    },
}

```

### render函数
使用 `h` 函数（即 Vue 内部的 `createElement`）来手动创建虚拟 DOM，`h` 函数的第一个参数是元素的标签名，第二个是属性对象，第三个是子节点。可以将 `template` 中的元素和逻辑转化为 `render` 函数的返回值。
```javascript
// 完整参数签名
function h(
  type: string | Component,
  props?: object | null,
  children?: Children | Slot | Slots
): VNode
```

使用render函数代替template：
``` javascript
template: /*html*/ `
          <div>{{ double }}</div>
          <button @click="printff">click me</button>
          <MyComp :msg="msg"/>
          <MyComp2 />
        `,
```

``` javascript
render() {
        // `h` 是 Vue 提供的渲染函数，用来创建虚拟 DOM
        return h('div', [
            h('div', this.double),  // 渲染计算属性 `double` 的值
            
            h('button', { onClick: this.printff }, 'click me'),  
            // 渲染按钮并绑定 `click` 事件
            
            h(MyComp, { msg: this.msg }),  
            // 渲染 MyComp 组件并传递 `msg` 属性
            
            h(MyComp2),  // 渲染 MyComp2 组件
        ]);
    },
```
