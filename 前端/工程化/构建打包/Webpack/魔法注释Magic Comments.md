# 魔法注释Magic Comments
- 为动态导入的模块指定 chunk 名称
- 控制代码分割后生成的文件名
- 便于调试和长期缓存

```javascript
// Webpack 中的写法
components: {
  List: () => import(/* webpackChunkName: "list" */ './List.vue')
}```

在Vite中支持但标准的做方法是在配置文件中定义
```javascript
// vite.config.js
export default {
  build: {
    rollupOptions: {
      output: {
        chunkFileNames: 'js/[name]-[hash].js',
        entryFileNames: 'js/[name]-[hash].js',
        assetFileNames: 'assets/[name]-[hash].[ext]'
      }
    }
  }
}```