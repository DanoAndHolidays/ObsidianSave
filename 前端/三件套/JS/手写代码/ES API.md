##### sleep/delay
基于promise实现的
```javascript
const sleep = (time) => {
  return new Promise((resolve) => {
    setTimeout(resolve(`sleep: ${time}ms`), time);
  });
};

sleep(23).then((message) => {
  console.log(message); // sleep: 23ms
})
```
##### Promise.All
```javascript
Promise.fakeAll = function (promises) {
    return new Promise((resolve, reject) => {
        let results = []
        for (let p of promises) {
            Promise.resolve(p)
                .then((value) => {
                    results.push(value)
                    if (results.length === promises.length) {
                        resolve(results)
                    }
                })
                .catch((reason) => {
                    reject(reason)
                })
        }
    })
}

const sleep = (seconds) =>
    new Promise((resolve) => setTimeout(() => resolve(seconds), seconds))

Promise.fakeAll([sleep(2), sleep(3), sleep(4)])
    .then((res) => console.log(res))
    .catch((err) => console.log(err))
// [2, 3, 4]

Promise.fakeAll([sleep(2), sleep(3), Promise.reject("fail"), sleep(4)])
    .then((res) => console.log(res))
    .catch((err) => console.log(err))
// fail
```
这里为什么会报错呢？promise.all是一个静态方法，并不应该定义为实例方法
##### 数组扁平化flat
```javascript
/**
 * 数组扁平化函数
 * @param {Array} list - 输入数组
 * @param {number} depth - 扁平化深度，默认为1
 * @returns {Array} 扁平化后的数组
 */
function flatten(list, depth = 1) {
    // 深度为0时直接返回
    if (depth === 0) return list;
    
    // 使用reduce进行递归扁平化
    return list.reduce((accumulator, current) => {
        // [修正语法]：判断当前元素是否为数组
        if (Array.isArray(current)) {
            // 递归扁平化子数组，深度减1
            return accumulator.concat(flatten(current, depth - 1));
        } else {
            return accumulator.concat(current);
        }
    }, []);
}
```
##### isArray
```javascript
// [补充说明]：兼容的数组检测方法
function myIsArray(obj) {
    return Object.prototype.toString.call(obj) === '[object Array]';
}
```

```javascript
// 示例数组
const nestedArray = [1, [2, [3, [4]]], 5];

// 扁平化一级
console.log(flatten(nestedArray)); 
// 输出: [1, 2, [3, [4]], 5]

// 完全扁平化
console.log(flatten(nestedArray, Infinity)); 
// 输出: [1, 2, 3, 4, 5]
```

##### reduce
```javascript
function fakeReduce(callback, init) {
    const arr = this
    function next(acc, index) {
        if (index >= arr.length) {
            return acc
        }
        let result = callback(acc, arr[index], index, arr)
        return next(result, index + 1)
    }

    let res
    if (init !== undefined) {
        res = next(init, 0)
    } else {
        res = next(arr[0], 1)
    }

    return res
}

Array.prototype.fakeReduce = fakeReduce

let arr = [1, 3, 4, 5]
console.log(arr.fakeReduce((sum, item) => sum + item))
// 13
```
---
