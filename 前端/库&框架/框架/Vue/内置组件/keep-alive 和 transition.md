# Vue 内置组件 keep-alive 和 transition 的实现原理
## keep-alive 组件原理
### 核心机制
```javascript
// keep-alive 本质上是一个抽象组件
export default {
  name: 'keep-alive',
  abstract: true, // 标记为抽象组件，不会出现在 DOM 中
  
  props: {
    include: [String, RegExp, Array],
    exclude: [String, RegExp, Array],
    max: [String, Number]
  },

  created() {
    this.cache = Object.create(null) // 缓存组件实例
    this.keys = [] // 缓存组件的 key
  },
  
  destroyed() {
    for (const key in this.cache) {
      pruneCacheEntry(this.cache, key, this.keys)
    }
  },
}
```
### 缓存策略
```javascript
render() {
  const slot = this.$slots.default
  const vnode = getFirstComponentChild(slot) // 获取第一个子组件
  
  if (vnode) {
    const { componentOptions } = vnode
    const key = vnode.key == null
      ? componentOptions.Ctor.cid + (componentOptions.tag ? `::${componentOptions.tag}` : '')
      : vnode.key
    
    // 检查是否需要缓存
    if (this.cache[key]) {
      vnode.componentInstance = this.cache[key].componentInstance
    } else {
      this.cache[key] = vnode
      this.keys.push(key)
      // 检查最大缓存数量
      if (this.max && this.keys.length > parseInt(this.max)) {
        pruneCacheEntry(this.cache, this.keys[0], this.keys)
      }
    }
    
    vnode.data.keepAlive = true // 标记为 keep-alive 组件
  }
  
  return vnode || (slot && slot[0])
}
```
### 生命周期处理
```javascript
// 激活时调用 activated 钩子
function activated() {
  callHook(this, 'activated')
}

// 停用时调用 deactivated 钩子  
function deactivated() {
  callHook(this, 'deactivated')
}
```
## transition 组件原理
### 核心结构
```javascript
export default {
  name: 'transition',
  props: {
    name: String,
    mode: String, // in-out / out-in
    appear: Boolean
  },
  
  render(h) {
    // 获取子元素
    let children = this.$slots.default
    if (!children) return
    
    // 过滤掉文本节点
    children = children.filter(c => c.tag || c.isComment)
    if (!children.length) return
    
    // 处理模式
    const mode = this.mode
    if (mode && mode !== 'in-out' && mode !== 'out-in') {
      mode = 'in-out'
    }
    
    const rawChild = children[0]
    return rawChild
  }
}
```
### CSS 过渡实现
```javascript
export function enter(vnode, toggleDisplay) {
  const el = vnode.elm
  
  // 调用 before-enter 钩子
  callHook(vnode, 'before-enter')
  
  // 添加 enter 类名
  addClass(el, enterClass)
  addClass(el, enterActiveClass)
  
  nextFrame(() => {
    removeClass(el, enterClass)
    addClass(el, enterToClass)
    
    if (!vnode.data.show) {
      removeClass(el, enterToClass)
      removeClass(el, enterActiveClass)
    }
  })
}
```
### JavaScript 钩子实现
```javascript
function callHook(vnode, hook) {
  const handlers = vnode.data && vnode.data.transition
  if (handlers && handlers[hook]) {
    handlers[hook]()
  }
}

function enter(vnode, done) {
  const el = vnode.elm
  
  callHook(vnode, 'before-enter')
  
  // CSS 过渡
  addClass(el, enterClass)
  addClass(el, enterActiveClass)
  
  nextFrame(() => {
    removeClass(el, enterClass)
    addClass(el, enterToClass)
    
    if (!userWantsControl) {
      whenTransitionEnds(el, type => {
        removeClass(el, enterToClass)
        removeClass(el, enterActiveClass)
        callHook(vnode, 'after-enter')
        done()
      })
    }
  })
}
```
### 类名管理
```javascript
// 自动添加的 CSS 类名
const transitionProps = {
  name: 'fade',
  // 对应的类名：
  // .fade-enter-active, .fade-leave-active
  // .fade-enter, .fade-enter-to
  // .fade-leave, .fade-leave-to
}

function resolveTransitionClass(name, state) {
  return name + '-' + state
}

function addClass(el, cls) {
  if (cls && !hasClass(el, cls)) {
    el.classList.add(cls)
  }
}

function removeClass(el, cls) {
  if (cls) {
    el.classList.remove(cls)
  }
}
```
## 关键实现细节
### keep-alive 的 LRU 算法
```javascript
function pruneCacheEntry(cache, key, keys) {
  const cached = cache[key]
  if (cached && (!filter || filter(key))) {
    cached.componentInstance.$destroy() // 销毁实例
  }
  cache[key] = null
  remove(keys, key)
}
```
### transition 的动画帧处理
```javascript
function nextFrame(fn) {
  const frame = requestAnimationFrame
    ? requestAnimationFrame
    : setTimeout
  
  frame(() => {
    frame(fn)
  })
}

function whenTransitionEnds(el, expectedType, cb) {
  const { type, timeout, propCount } = getTransitionInfo(el, expectedType)
  
  if (!type) return cb()
  
  const event = type === TRANSITION ? transitionEndEvent : animationEndEvent
  let ended = 0
  
  const end = () => {
    el.removeEventListener(event, onEnd)
    cb()
  }
  
  const onEnd = e => {
    if (e.target === el) {
      if (++ended >= propCount) {
        end()
      }
    }
  }
  
  setTimeout(() => {
    if (ended < propCount) {
      end()
    }
  }, timeout + 1)
  
  el.addEventListener(event, onEnd)
}
```
## 使用示例
### keep-alive 使用
```vue
<template>
  <keep-alive :include="['ComponentA']" :max="10">
    <component :is="currentComponent"></component>
  </keep-alive>
</template>
```
### transition 使用
```vue
<template>
  <transition 
    name="fade"
    mode="out-in"
    @before-enter="beforeEnter"
    @enter="enter"
    @after-enter="afterEnter">
    <div v-if="show" key="content">内容</div>
  </transition>
</template>

<style>
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.5s;
}
.fade-enter, .fade-leave-to {
  opacity: 0;
}
</style>
```