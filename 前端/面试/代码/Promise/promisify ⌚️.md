# promisify
#promise
题目，实现一个
```js
fs.readFile('/path/index.js', (err, data) => {
     // handle err and data
}) ；

const readFile = promisify(fs.readFile);

readFile('/path/index.js').then(data => {
    // handle data
}).catch(err => {
    // handle err
})
```

我的实现：
```js
function promisify(func) {
    return function (url) {
        return new Promise((resolve, reject) => {
            const cb = (err, data) => {
                if (data) {
                    resolve(data)
                } else {
                    reject(err)
                }
            }
            func(url, cb)
        })
    }
}
```

优化后的代码：
```js
function promisify(func) {
    // 1. 使用 ...args 接收任意数量的参数
    return function (...args) { 
        return new Promise((resolve, reject) => {
            const cb = (err, data) => {
	            // 2. 遵循 error-first 规范，仅通过 err 判断失败
                if (err) { 
                    reject(err);
                } else {
                    resolve(data);
                }
            };
			
			// 3. 将回调函数追加到参数列表末尾
            args.push(cb); 
            // 4. 使用 apply 传递参数并保留 this 上下文
            func.apply(this, args); 
        });
    };
}
```