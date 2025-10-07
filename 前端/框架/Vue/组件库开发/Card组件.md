[从零开始撸一个 Vue 组件库，搬砖效率提升404倍！]([测试组件_哔哩哔哩_bilibili](https://www.bilibili.com/video/BV1Zf4y1u75o?spm_id_from=333.788.videopod.episodes&vd_source=47c9acd507be61251cd2bb730416395c&p=7))
# 脚手架
---
使用vue-cil做脚手架，但是现在已经官方推荐使用vue create

##### 使用脚手架初始化项目并修改项目结构
![[Pasted image 20250913103350.png]]
将src修改为examples，并配置vue.confi.js

##### 设计Card组件
![[Pasted image 20250913104550.png]]
![[Pasted image 20250913104639.png]]
这些属性使用props来传递
```javascript
props:{
	width:{
		type:Number,
		default:0,
	},
	imgSrc:{
		type:String,
		default:'',
	}
	//...
}
```

建立HTML的结构
```html

```

##### 前端模块化过程
![[Pasted image 20250913112022.png]]

##### 搭建文档站点
使用[VuePress]([首页 | VuePress](https://vuepress.vuejs.org/zh/))使用md来构建一个静态的网页
[Pages自动部署]([将文档站点部署到github.io_哔哩哔哩_bilibili](https://www.bilibili.com/video/BV1Zf4y1u75o?spm_id_from=333.788.videopod.episodes&vd_source=47c9acd507be61251cd2bb730416395c&p=18))
[视频参考]([9分钟零成本搭建自动化部署个人博客(Hexo + Github Action + Page)_哔哩哔哩_bilibili](https://www.bilibili.com/video/BV1xTgTemEDU/?spm_id_from=333.337.search-card.all.click&vd_source=47c9acd507be61251cd2bb730416395c))