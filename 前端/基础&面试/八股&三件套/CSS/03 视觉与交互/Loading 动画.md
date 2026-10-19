# Loading 动画

![[Pasted image 20261019220410.png]]


---
## 圆环
其实是利用一个圆环的 border 来实现的：
```html
<!-- 旋转圆环 -->
<div class="loader"></div>
```

```css
/* 旋转圆环 */
@keyframes spin {
  to { transform: rotate(360deg); }
}

.loader {
  width: 40px; height: 40px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #3498db;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}
```

---
## 弹跳点
```html
<!-- 三个弹跳点 -->
<div class="dots">
  <span class="dot"></span>
  <span class="dot"></span>
  <span class="dot"></span>
</div>
```

```css
/* 弹跳点 */
@keyframes bounce {
  0%, 80%, 100% { transform: scale(0); }
  40% { transform: scale(1); }
}

.dot { 
	display: inline-block; 
	width: 12px; 
	height: 12px; 
	border-radius: 50%; 
	background: #333; 
	animation: bounce 1.4s infinite ease-in-out both; 
}

.dot:nth-child(1) { animation-delay: -0.32s; }
.dot:nth-child(2) { animation-delay: -0.16s; }
```
