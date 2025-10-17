# Postcss
## 基础使用
```json
// 常用配置
"devDependencies": {
    "autoprefixer": "^10.4.21",
    "postcss": "^8.5.6",
    "postcss-cli": "^11.0.1"
  }
```

```js
// postcss.config.js 配置文件
export default {
    plugins: {
        autoprefixer: {},
    },
}
```

```css
// 前
.header{
    text-align: center;
    text-decoration: overline;
    scroll-behavior: smooth;
    scroll-margin: 10px;
    user-select: none;
    -webkit-user-drag: none;
    pointer-events: none;
}

// 后
.header{
    text-align: center;
    text-decoration: overline;
    scroll-behavior: smooth;
    scroll-margin: 10px;
    -webkit-user-select: none;
       -moz-user-select: none;
            user-select: none;
    -webkit-user-drag: none;
    pointer-events: none;
}
```

## 在Vite中使用
Vite中集成了Postcss。如果项目包含有效的 PostCSS 配置 (任何受 [postcss-load-config](https://github.com/postcss/postcss-load-config) 支持的格式，例如 `postcss.config.js`)，它将会自动应用于所有已导入的 CSS。
请注意，CSS 最小化压缩将在 PostCSS 之后运行，并会使用 [`build.cssTarget`](https://cn.vitejs.dev/config/build-options.html#build-csstarget) 选项。

```css
// 前
.nav-bar[data-v-498bbd1c]
	height: 2.5rem;
	overflow: hidden;
	color: #e3e3e3a3;
	display: flex;
	justify-content: space-around;
	align-items: center;
	z-index: 11;
	background-image: linear-gradient(to bottom, #0006, #0000);
	backdrop-filter: blur(1px);
	user-select: none;
}

// 后
.nav-bar[data-v-498bbd1c]{
	height: 2.5rem;
	overflow: hidden;
	color: ■#e3e3e3a3;
	display: flex;
	justify-content: space-around;
	align-items: center;
	z-index: 11;
	background-image: linear-gradient(to bottom, #0006, #0000);
	backdrop-filter: blur(1px);
	-webkit-user-select: none;
	   -moz-user-select: none;
			user-select: none;
}
```