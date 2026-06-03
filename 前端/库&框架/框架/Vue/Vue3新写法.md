# `<script setup>`语法糖
---
如果不使用语法糖，需要进行导出，否则无法使用组件
```javascript
import Helloworld from'./components/Helloworld.vue'

export default {
	name: 'App',
	components:{
		Helloworld
	}
}
```

昨天的报错就是因为我忘记写`setup`了
```txt
Failed to resolve component: NavBar
If this is a native custom element, make sure to exclude it from component resolution via compilerOptions.isCustomElement. 
```

# 动态组件
---
![[Pasted image 20250921230348.png]]

# props与emit
---
![[Pasted image 20250921230716.png]]