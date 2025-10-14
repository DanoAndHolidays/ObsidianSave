# 简介
---
##### 组成部分
它主要由两部分组成：
- 一个开发服务器，它基于 [原生 ES 模块](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Modules) 提供了 [丰富的内建功能](https://cn.vitejs.dev/guide/features.html)，如速度快到惊人的 [模块热替换（HMR）](https://cn.vitejs.dev/guide/features.html#hot-module-replacement)。
- 一套构建指令，它使用 [Rollup](https://cn.rollupjs.org/) 打包你的代码，并且它是预配置的，可输出用于生产环境的高度优化过的静态资源。

也就是说，平时我就已经在使用Vite了，在创建Vue项目的时候，就已经在使用Vite了。构建的是时候用的其实是vue create

##### Vite
是基于已有的构建工具的高级封装
# Vite 编译与缓存机制
---

##### 预编译与缓存
[修正术语]：将模块在第一次启动之前编译后放入 `cache` 缓存，让 Vite 读取缓存，不再重复编译。  
[补充说明]：Vite 在预编译阶段将 CommonJS/UMD 模块转换为 ESM 模块（`entry → ESM`），以优化加载性能。

##### 优化选项（optimizeDeps）
```javascript
optimizeDeps: {
  // [修正语法]：entries 指定预编译入口
  entries: ["src/main.js"],
  // [补充说明]：exclude 排除不需要预编译的依赖
  exclude: ["unpkg-module"],
  // [修正术语]：include 强制包含需要预编译的依赖
  include: ["lodash-es"]
}
```
[补充说明]：Vite 会将小模块合并成大区块（chunk），减少请求数量。未使用的模块在 `build` 阶段会被 Tree Shaking 移除，避免冗余代码。

##### 服务端缓存控制
[补充说明]：开发服务器（Server）通过 `Cache-Control: no-cache` 和 WebSocket 实现热更新，阻止浏览器缓存过期资源。

---

# 热更新机制
---

##### 实现方式
```javascript
export const render = () => {
  // [修正语法]：使用 import.meta.hot 检测热更新接口
  if (import.meta.hot) {
    import.meta.hot.accept((newModule) => {
      // [补充说明]：回调函数接收更新后的模块
      newModule.render();
    });
  }
};
```

##### 服务端更新策略
[补充说明]：Vite Server 通过重写 `import` 语句与全局导入（glob import）实现模块替换，无需重启服务。  
[修正示例]：
```javascript
// [修正语法]：使用 import.meta.glob 动态导入模块
const modules = import.meta.glob('./modules/*.js');
// modules 是一个 Map，键为路径，值为异步加载函数
```

##### 注意事项
[补充说明]：需关注全局状态管理，避免热更新导致状态丢失。

---

# 环境变量与模式
---

##### 环境变量使用
[修正术语]：通过 `import.meta.env` 访问环境变量（非 `import_menu.env`）。  
常用变量：
- `import.meta.env.MODE`：当前模式（development/production）
- `import.meta.env.BASE_URL`：部署基础路径
- `import.meta.env.PROD`：是否生产环境
- `import.meta.env.DEV`：是否开发环境
- `import.meta.env.SSR`：是否服务端渲染

##### 编译时替换
[补充说明]：在编译过程中，`import.meta.env` 会被静态替换为字符串，生产环境不存在该对象。

##### 自定义环境变量
[修正示例]：  
1. 创建 `.env` 文件：
```bash
VITE_TITLE=Hello
```
2. 代码中访问：
```javascript
console.log(import.meta.env.VITE_TITLE); // "Hello"
```
[补充说明]：需以 `VITE_` 前缀暴露变量，支持多环境（development/production/test）。

---

# TypeScript 与静态资源处理
---

##### TypeScript 支持
[补充说明]：Vite 仅编译 TypeScript，不执行类型检查（需通过 `tsc --noEmit` 或 IDE 单独校验）。

##### 静态资源导入
```javascript
// [修正语法]：使用 ?url 获取资源 URL
import testUrl from './test.png?url';
// [补充说明]：使用 ?raw 获取资源字符串内容
import shaderSource from './shader.glsl?raw';
// 直接导入 JSON
import pkg from './package.json';
import { version } from './package.json'; // 支持解构
```

##### WebAssembly 支持
[补充说明]：Vite 支持 `.wasm` 文件导入，默认返回初始化函数。

##### 配置文件
[补充说明]：  
- `vite.config.ts`：主配置文件（支持 TS）
- `prettier`：代码格式化配置
- `package.json` 脚本示例：
```json
{
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build"
  }
}
```

---

# CSS 与预处理配置
---

##### CSS 变量与模块
[修正术语]：推荐使用 CSS Variables（非 `cases`）和 CSS Modules（非 `fracas`）。  
示例：
```css
:root {
  --main-bg-color: red;
}
.component {
  background: var(--main-bg-color);
}
```

##### 路径映射（alias）
[补充说明]：在 `vite.config.js` 中配置别名：
```javascript
export default {
  resolve: {
    alias: {
      '@styles': '/src/styles'
    }
  }
};
```
CSS 中使用：
```css
@import url('@styles/variables.css');
```

##### CSS 预处理器
[补充说明]：支持 Sass、Less、Stylus，需安装对应预处理器：
```bash
npm install -D sass
```
配置示例：
```javascript
export default {
  css: {
    preprocessorOptions: {
      scss: { additionalData: `@import "@styles/vars.scss";` }
    }
  }
};
```

---
# Vite 项目结构与构建
---

##### 构建工具对比
[补充说明]：Vite 使用**ESBuild（开发环境）** 和 **Rollup（生产构建）**，相比 Webpack 启动更快。

##### 创建 Vue 3 项目
[修正版本]：Vite 5 默认支持 Vue 3（非版本10/20）。  
创建命令：
```bash
npm create vite@latest
# 选择框架：vanilla / vue / react 等
```

##### 目录结构
```
project/
├── public/          # 静态资源（不经过编译）
├── src/
│   ├── assets/      # 需 import 引入的资源
│   └── main.js      # 入口文件
├── index.html       # HTML 入口（包含 <script type="module">）
└── vite.config.js   # 配置文件
```

##### 开发服务器原理
[补充说明]：浏览器通过 `index.html` 中的模块脚本发起请求，Vite Server 拦截请求并按需编译返回。

---
# 非Node环境服务集成
---
# Node集成Vite的SSR
---
# Vite插件开发
---
本质是受限制的Rollup插件：
- 没有使用moduleParsed钩子
- 打包和输出没有强耦合

仅在服务dev server启动时
- options
- buildStart

每个模块：
- resolveld
- load
- transform

服务关闭时
- buildEnd
- closeBundle

modulePased是不会被调用的
Rollup插件可以在build中配置

Vite特有的钩子
- config
- configResolved
- configureServer
- transformIndexHtml
- handleHotUpdate

##### 执行时机
- pre：
- normal：
- post：