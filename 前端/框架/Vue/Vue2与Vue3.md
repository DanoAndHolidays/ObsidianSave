# Vue 2 与 Vue 3 的核心区别
---

##### 响应式系统重构
Vue 3 使用 Proxy 替代 Object.defineProperty
```javascript
// Vue 2 响应式原理
const data = { count: 0 };
Object.defineProperty(data, 'count', {
    get() { /* 依赖收集 */ },
    set(newVal) { /* 触发更新 */ }
});

// Vue 3 响应式原理
const reactiveData = new Proxy(data, {
    get(target, key) { /* 依赖收集 */ },
    set(target, key, newVal) { /* 触发更新 */ }
});
```

[补充说明]：Proxy 的优势：
- 支持数组索引修改、length 变化检测
- 支持动态添加新属性
- 更好的性能表现

##### Composition API 引入
[修正说明]：Vue 3 提供模块化的组合式 API
```javascript
// Vue 2 选项式 API
export default {
    data() {
        return { count: 0 }
    },
    methods: {
        increment() { this.count++ }
    },
    mounted() { /* 生命周期 */ }
}

// Vue 3 组合式 API
import { ref, onMounted } from 'vue';

export default {
    setup() {
        const count = ref(0);
        const increment = () => count.value++;
        
        onMounted(() => { /* 生命周期 */ });
        
        return { count, increment };
    }
}
```

##### 性能优化改进
[补充说明]：Vue 3 在多个层面进行性能优化：
- **Tree-shaking 支持**：按需引入 API，减少打包体积
- **编译器优化**：静态节点提升、补丁标志等
- **源码重构**：使用 TypeScript 重写，更好的类型支持

##### 生命周期变化
[修正说明]：Vue 3 生命周期函数命名和用法调整
```javascript
// Vue 2 生命周期
beforeCreate → 使用 setup()
created → 使用 setup()
beforeMount → onBeforeMount
mounted → onMounted
beforeUpdate → onBeforeUpdate
updated → onUpdated
beforeDestroy → onBeforeUnmount
destroyed → onUnmounted
```

##### 新增内置组件
[补充说明]：Vue 3 引入多个新组件：
- **Teleport**：将组件渲染到 DOM 树的指定位置
- **Suspense**：处理异步组件加载状态
- **Fragment**：支持多根节点模板

---