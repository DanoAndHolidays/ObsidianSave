封装了Node.js的API，简化了搭建后端的操作流程

#### 初始化
```
npm init //创建package.json文件
npm i express //安装
```
---
#### 简单的运用
```
const experss = require('express')
const app = experss()

app.get('/', function (req, res) {
    res.send('你好')
})

app.get('/uesr', function (req, res) {
    res.send('你好用户')
})

app.listen(3000, function () {
    console.log('服务已经启动')
}) 

node server.js //来运行js
```
---
#### Nodemon
```
//安装，能够方便的启动服务
npm install nodemon --save--dev

{
  "name": "express",
  "version": "1.0.0",
  "description": "",
  "main": "index.js",
  "scripts": {
    "test": "echo \"Error: no test specified\" && exit 1",
    "start": "nodemon server.js" //修改配置文件package.json
  },
  "author": "",
  "license": "ISC",
  "dependencies": {
    "express": "^5.1.0",
    "nodemon": "^3.1.10"
  }
}
```
---

#### 路由
访问的接口由路由判断。'/'是路由部分，function是回调函数部分
常用的路由方法有post，get，put，delete等
```
const experss = require('express')
const app = experss()
  
app.get('/', function (req, res) {
    console.log(req.query);
    res.send('你好')
})
```
有一种的特殊的
```
app.all() //会响应所有的路由
```
可以使用postman来模拟请求

路由路径： 
- 字符模式路由路径：
	- '/ab?cd'支持abcd和acd
	- '/ab+cd'支持ab（0-多个b）cd
	- '/ab*cd'通配符
- 正则路由路径：/在两个规范斜杠里书写/
	- /a/ 表示有a就行
	- /.**fiy$/ .通配符*$以其结尾