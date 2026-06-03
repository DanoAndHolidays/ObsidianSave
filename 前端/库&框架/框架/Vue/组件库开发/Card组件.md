
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
