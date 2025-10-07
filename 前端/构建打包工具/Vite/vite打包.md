#### 打包vue项目的方法和问题
- ==npm run build==
- 出现空白页的问题，路径问题
- 改为相对路径，在vite.config.js中配置路径：==base：'./'==
- 没有报错但也没有页面，是router的原因，使用在router/index.js中history项使用createMemoryHistory函数即可显示，==注意引用这个函数==

