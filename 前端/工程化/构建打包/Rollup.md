# Rollup
---
## Tree Shaking
![[Pasted image 20250908225651.png]]
![[Pasted image 20250908225714.png]]
仅仅打包我们用到的代码，提升应用的性能

## 通过命令行执行
由于Rollup本身设计是使用命令行来使用的：
`rollup -i index.js --file dist.js --format es`

将两个文件打包到一个文件夹
`rollup -i index.js  -i test.js --dir dist`

`--format` 
- `iife` 立即执行函数
- `cjs` commonjs 
- `es` esm
- `umd` 兼容模式

`--watch` 监听文件变化

可以在根目录添加配置文件`rollup.config.js`，使用`rollup --config`或`rollup -c`来按配置编译 【补充：添加了短命令形式】
```javascript
export default {
  input: 'index.js',
  output: {
    file: './dist/bundle.js',
    format: 'iife',
  },
  plugins: [
    // Add any Rollup plugins here
  ]
};
```

环境变量`--environment TEST:123` 
使用`process.env.TEST`来获取 

## 常用插件示例
`plugins`插件，能够实现很丰富的功能 ：
- @rollup/plugin-node-resolve: 解析node_modules中的第三方模块
- @rollup/plugin-commonjs: 将CommonJS模块转换为ES6
- @rollup/plugin-babel: 使用Babel转换代码
- @rollup/plugin-terser: 压缩打包后的代码

## 通过配置文件执行
```javascript
import { defineConfig } from 'rollup';
import resolve from '@rollup/plugin-node-resolve';
import commonjs from '@rollup/plugin-commonjs';
import babel from '@rollup/plugin-babel';

export default defineConfig({
  input: 'src/index.js',
  output: [
    {
      file: 'dist/bundle.cjs.js',
      format: 'cjs',
      exports: 'auto'
    },
    {
      file: 'dist/bundle.esm.js',
      format: 'esm'
    }
  ],
  plugins: [
    resolve(),
    commonjs(),
    babel({ babelHelpers: 'bundled' })
  ],
  external: ['react', 'react-dom'] // 指定不打包的依赖
});
```

也可以使用数组
```javascript
export default [
  {
    input: "index.js",
    output: {
      file: "./dist/bundle.iife.js",
      format: "iife",
      plugins:[terser()],
    },
    plugins: [
      resolve(),
      commomjs()
    ],
    banner:"/** 你好 **/"
  },
  {
    input: "index.js",
    output: {
      file: "./dist/bundle.cjs.js",
      format: "cjs",
    },
  },
  {
    input: "index.js",
    output: {
      file: "./dist/bundle.esm.js",
      format: "esm",
    },
  },
];
```
## 代码分割与动态导入
Rollup支持通过动态import()实现代码分割：
```javascript
// 动态导入示例
const module = await import('./module.js');
```

在配置中启用代码分割：
```javascript
export default {
  input: ['src/index.js', 'src/another.js'],
  output: {
    dir: 'dist',
    format: 'esm',
    chunkFileNames: '[name]-[hash].js' // 分割后的 chunk 命名格式
  }
};
```

## 插件
大部分的Rollup插件可以直接在vite中使用
hook：
- buildStart：配置
- resolveId：解析文件路径
- options：第一个执行的hook，预处理
- transform：对代码进行处理

Rollup插件是一个返回对象的函数，该对象包含各种hook：
```javascript
export default function myPlugin() {
  return {
    name: 'my-plugin', // 插件名称
    // 插件hook
    options(options) {
      // 修改或返回处理后的options
      return options;
    }
  }
}
```

三个官方插件：
- alias：路径转换
```javascript
import alias from '@rollup/plugin-alias';

export default {
  plugins: [
    alias({
      entries: [
        { find: 'utils', replacement: '../../../utils' },
        { find: 'lodash', replacement: 'lodash-es' }
      ]
    })
  ]
};
```

- babel：将es语法转化为其他版本
```javascript
import { babel } from '@rollup/plugin-babel';

export default {
  plugins: [
    babel({
      babelHelpers: 'bundled',
      presets: ['@babel/preset-env'],
      exclude: 'node_modules/**'
    })
  ]
};
```

- replace：替换代码中的字符串
```javascript
import replace from '@rollup/plugin-replace';

export default {
  plugins: [
    replace({
      'process.env.NODE_ENV': JSON.stringify('production'),
      __buildDate__: () => JSON.stringify(new Date()),
      preventAssignment: true // 防止意外替换赋值语句
    })
  ]
};
```

【补充：更多常用hook说明】
- load(id): 自定义加载文件内容
- buildEnd(error): 构建结束时的清理工作
- renderChunk(code, chunk): 处理单个chunk的输出

常用的插件：
- @rollup/plugin-commonjs: 将CommonJS模块转换为ES6模块
- @rollup/plugin-replace: 替换代码中的字符串
- @rollup/plugin-eslint: 集成ESLint检查
- @rollup/plugin-image: 导入图片文件并将其作为base64或文件路径
- @rollup/plugin-strip: 删除代码中的console.log和debugger语句
- @rollup/plugin-wasm: 导入和打包WebAssembly模块
- @rollup/plugin-typescript: TypeScript支持

【补充：插件使用示例】
## 完整插件配置示例
```javascript
import commonjs from '@rollup/plugin-commonjs';
import eslint from '@rollup/plugin-eslint';
import image from '@rollup/plugin-image';
import strip from '@rollup/plugin-strip';
import typescript from '@rollup/plugin-typescript';

export default {
  input: 'src/index.ts',
  output: {
    file: 'dist/bundle.js',
    format: 'esm'
  },
  plugins: [
    eslint({
      include: ['src/**/*.ts']
    }),
    typescript(),
    commonjs(),
    image(),
    strip({
      include: '**/*.(ts|js)',
      functions: ['console.log', 'assert.*', 'debug']
    })
  ]
};
```

【补充：自定义插件示例】
## 自定义简单插件：添加banner
```javascript
function addBannerPlugin(bannerText) {
  return {
    name: 'add-banner',
    renderChunk(code) {
      return `/* ${bannerText} */\n${code}`;
    }
  };
}

// 使用
export default {
  plugins: [
    addBannerPlugin('Build: ' + new Date().toISOString())
  ]
};
```