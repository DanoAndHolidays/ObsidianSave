# Hello React
## 1 React是什么
React是一个用于编写用户界面的JS库，也就是说，它并不限于Web应用。

>React is a JavaScript library for rendering user interfaces (UI). UI is built from small units like buttons, text, and images. React lets you combine them into reusable, nestable _components._ From web sites to phone apps, everything on the screen can be broken down into components. In this chapter, you’ll learn to create, customize, and conditionally display React components.
## 2 构建项目
使用create-react-app脚手架工具快速构建项目：
```shell
npx create-react-app [项目名]
```

结果如下：
```shell
Success! Created hello-react at G:\Save\Grogramming\React\hello-react
Inside that directory, you can run several commands:

  npm start
    Starts the development server.

  npm run build
    Bundles the app into static files for production.

  npm test
    Starts the test runner.

  npm run eject
    Removes this tool and copies build dependencies, configuration files
    and scripts into the app directory. If you do this, you can’t go back!

We suggest that you begin by typing:

  cd hello-react
  npm start

Happy hacking!
```

## 3 项目结构
![[Pasted image 20251202221851.png]]

```js
// 目前代码中似乎没有使用到react库，但是当JSX经过babel编译后，就会使用react.createElement()
import React from 'react'

// ReactDOM负责在浏览器渲染
import ReactDOM from 'react-dom/client'

// 根结点
const root = ReactDOM.createRoot(document.getElementById('root'))
root.render(<p>Hello React</p>)
```
React Element一但初始化是不可以被修改的