# esbuild
---
使用go语言编写，需要使用命令行来使用

`npx esbuild index.js --outfile=dist.js --format=cjs  --platform=node`

【补充：常用命令行选项】
##### 常用命令行选项
- `--bundle`: 打包所有依赖
- `--minify`: 压缩代码
- `--sourcemap`: 生成sourcemap文件
- `--target`: 指定目标环境（如es2015, chrome58, node12等）
- `--loader`: 指定文件类型加载方式（如`.jsx=jsx, .ts=ts`）

【补充：配置文件使用】
##### 配置文件使用
可以在项目根目录创建`esbuild.config.js`文件：
```javascript
require('esbuild').build({
  entryPoints: ['src/index.js'],
  bundle: true,
  outfile: 'dist/bundle.js',
  format: 'cjs',
  platform: 'node',
  minify: true,
  sourcemap: true,
  target: 'node14',
}).catch(() => process.exit(1))
```

【补充：package.json脚本配置】
```json
{
  "scripts": {
    "build": "esbuild src/index.js --bundle --outfile=dist.js --minify --sourcemap",
    "dev": "esbuild src/index.js --bundle --outfile=dist.js --watch"
  }
}
```

##### 插件开发
【补充：插件开发详细说明和示例】
esbuild插件是一个带有name和setup函数的对象：
```javascript
const myPlugin = {
  name: 'my-plugin',
  setup(build) {
    // 在解析阶段拦截导入路径
    build.onResolve({ filter: /^example$/ }, args => {
      return { path: args.path, namespace: 'example-ns' }
    })
    
    // 在加载阶段处理特定命名空间的文件
    build.onLoad({ filter: /.*/, namespace: 'example-ns' }, () => {
      return {
        contents: `export const message = 'Hello from plugin'`,
        loader: 'js',
      }
    })
  }
}

// 使用插件
require('esbuild').build({
  entryPoints: ['app.js'],
  bundle: true,
  outfile: 'out.js',
  plugins: [myPlugin],
})
```

【补充：插件常用API】
- `onResolve`: 拦截导入路径
- `onLoad`: 拦截加载内容
- `onStart`: 构建开始时调用
- `onEnd`: 构建结束时调用

【补充：完整插件示例】
##### 完整插件示例：替换环境变量
```javascript
const envPlugin = {
  name: 'env',
  setup(build) {
    // 拦截所有以 ENV_ 开头的导入
    build.onResolve({ filter: /^ENV_/ }, args => {
      return { path: args.path, namespace: 'env-ns' }
    })
    
    // 加载被拦截的模块
    build.onLoad({ filter: /.*/, namespace: 'env-ns' }, args => {
      const envVar = args.path.replace(/^ENV_/, '')
      const value = process.env[envVar] || ''
      
      return {
        contents: `export default ${JSON.stringify(value)}`,
        loader: 'js',
      }
    })
  }
}

// 使用方式：import apiKey from 'ENV_API_KEY'
```
