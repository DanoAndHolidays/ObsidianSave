### 回调
---
使用回调的方式来进行异步编程：
```javascript
function loadScript(src, callback) {
    console.log('finished'+src);
    setTimeout(callback, 500);
}

loadScript('1',() => {console.log('callback');});
```
在回调中回调：
```javascript
function loadScript(src, callback) {
    console.log('finished'+src);
    setTimeout(callback, 500);
}
//回调地狱
loadScript(
    '1',
    () => {
        console.log('callback');
        loadScript(
            '2',
            () => {
                console.log('callback');
                loadScript(
                    '3',
                    () => {
                        console.log('callback');
                        loadScript(
                            '4',
                            () => {
                                console.log('callback');
                            }
                        );
                    }
                );
            }
        );
    }
);
/**
 * finished1
callback
finished2
callback
finished3
callback
finished4
callback
 */
```

### Promise
---
是（单线程并发）解决异步编程回调地狱的一种方案。是一个特殊的对象，`Promise`对象代表一个异步操作，有三种状态：`pending`（进行中）、`fulfilled`（已成功）和`rejected`（已失败）。

`Promise`构造函数接受一个函数作为参数，该函数的两个参数分别是`resolve`和`reject`。它们是两个回调函数，由 JavaScript 引擎提供，不用自己部署。
```javascript
function timeout(ms) {
  return new Promise((resolve, reject) => {
    setTimeout(resolve, ms, 'done');
  });
}

timeout(100).then((value) => {
  console.log(value);
});
```
当 executor 获得了结果，无论是早还是晚都没关系，在函数体的内部它应该调用以下回调之一：
- `resolve(value)` —— 如果任务成功完成并带有结果 `value`。
- `reject(error)` —— 如果出现了 error，`error` 即为 error 对象。

由 `new Promise` 构造器返回的 `promise` 对象具有以下内部属性：
- `state` —— 最初是 `"pending"`，然后在 `resolve` 被调用时变为 `"fulfilled"`，或者在 `reject` 被调用时变为 `"rejected"`。
- `result` —— 最初是 `undefined`，然后在 `resolve(value)` 被调用时变为 `value`，或者在 `reject(error)` 被调用时变为 `error`。

其中，pending->fulfilled和pending->rejected是仅有的两种状态转换，代表着异步操作的结果。executor 只能调用一个 `resolve` 或一个 `reject`。任何状态的更改都是最终的。所有其他的再对 `resolve` 和 `reject` 的调用都会被忽略

![[Pasted image 20250628000757.png]]
`resolve`函数的作用是，将`Promise`对象的状态从“未完成”变为“成功”（即从 pending 变为 resolved），在异步操作成功时调用，并将异步操作的结果，作为参数传递出去；

`reject`函数的作用是，将`Promise`对象的状态从“未完成”变为“失败”（即从 pending 变为 rejected），在异步操作失败时调用，并将异步操作报出的错误，作为参数传递出去。
```javascript
//用于随机生成一个图片
function Image() {
    let result = Math.random();
    if (result > 0.5) {
        this.value = true;
    } else {
        this.value = false;
    };
}

let promise = new Promise(function (resolve, reject) {

    let image = new Image();
    console.log(image.value);

    if (image.value) {
        resolve('loaded');
    } else {
        reject(new Error("shit!!!"));
    }
});
```

注意，调用`resolve`或`reject`并不会终结 Promise 的参数函数的执行。一般来说，调用`resolve`或`reject`以后，Promise 的使命就完成了，后继操作应该放到`then`方法里面，而不应该直接写在`resolve`或`reject`的后面。所以，最好在它们前面加上`return`语句，这样就不会有意外。
```javascript
new Promise((resolve, reject) => {
  resolve(1);
  console.log(2);
}).then(r => {
  console.log(r);
});
// 2
// 1
```

Promise 对象的 `state` 和 `result` 属性都是内部的。我们无法直接访问它们。但我们可以对它们使用 `.then`/`.catch`/`.finally` 方法。我们在下面对这些方法进行了描述。

`Promise`实例生成以后，可以用`then`方法分别指定`resolved`状态和`rejected`状态的回调函数。`then`方法可以接受两个回调函数作为参数。第一个回调函数是`Promise`对象的状态变为`resolved`时调用，第二个回调函数是`Promise`对象的状态变为`rejected`时调用。这两个函数都是可选的。它们都接受`Promise`对象传出的值作为参数。
```javascript
promise.then(
  function(result) { /* handle a successful result */ },
  function(error) { /* handle an error */ }
);
```

```javascript
promise.then(
    result => { console.log(result) },//loaded
    error => { console.log(error) }//Error: shit!!!
)
```

`.catch(f)` 调用是 `.then(null, f)` 的完全的模拟，它只是一个简写形式。
一般使用then来处理结果，使用catch来处理错误。

`finally` 的功能是设置一个处理程序在前面的操作完成后，执行清理/终结。
```javascript
new Promise((resolve, reject) => {
  return resolve(1);
  // 后面的语句不会执行
  console.log(2);
})
```
```javascript
getJSON('/posts.json').then(function(posts) {
  // ...
}).catch(function(error) {
  // 处理 getJSON 和 前一个回调函数运行时发生的错误
  console.log('发生错误！', error);
});
```
上面代码中，`getJSON()`方法返回一个 Promise 对象，如果该对象状态变为`resolved`，则会调用`then()`方法指定的回调函数；如果异步操作抛出错误，状态就会变为`rejected`，就会调用`catch()`方法指定的回调函数，处理这个错误。另外，`then()`方法指定的回调函数，如果运行中抛出错误，也会被`catch()`方法捕获。
```javascript
p.then((val) => console.log('fulfilled:', val))
  .catch((err) => console.log('rejected', err));

// 等同于
p.then((val) => console.log('fulfilled:', val))
  .then(null, (err) => console.log("rejected:", err));
// 写法二
const promise = new Promise(function(resolve, reject) {
  reject(new Error('test'));
});
promise.catch(function(error) {
  console.log(error);
});
```
如果 Promise 状态已经变成`resolved`，再抛出错误是无效的。
```javascript
const promise = new Promise(function(resolve, reject) {
  resolve('ok');
  throw new Error('test');
});
promise
  .then(function(value) { console.log(value) })
  .catch(function(error) { console.log(error) });
// ok
```
上面代码中，Promise 在`resolve`语句后面，再抛出错误，不会被捕获，等于没有抛出。因为 Promise 的状态一旦改变，就永久保持该状态，不会再变了。一般来说，不要在`then()`方法里面定义 Reject 状态的回调函数（即`then`的第二个参数），总是使用`catch`方法。Promise 对象的错误具有“冒泡”性质，会一直向后传递，直到被捕获为止。也就是说，错误总是会被下一个`catch`语句捕获。
```javascript
getJSON('/post/1.json').then(function(post) {
  return getJSON(post.commentURL);
}).then(function(comments) {
  // some code
}).catch(function(error) {
  // 处理前面三个Promise产生的错误
});
```
跟传统的`try/catch`代码块不同的是，如果没有使用`catch()`方法指定错误处理的回调函数，Promise 对象抛出的错误不会传递到外层代码，即不会有任何反应。
```javascript
const someAsyncThing = function () {
    return new Promise(function (resolve, reject) {
        // 下面一行会报错，因为x没有声明
        resolve(x + 2);
    });
};

someAsyncThing()
    .then(function () {
        console.log('everything is great');
    })
    .catch((err) => {
        console.error(err);
    })
```
经过我的实验，是这样的，这样有bug了也不会报错，嘻嘻
一般总是建议，Promise 对象后面要跟`catch()`方法，这样可以处理 Promise 内部发生的错误。`catch()`方法返回的还是一个 Promise 对象，因此后面还可以接着调用`then()`方法。
```javascript
const someAsyncThing = function() {
  return new Promise(function(resolve, reject) {
    // 下面一行会报错，因为x没有声明
    resolve(x + 2);
  });
};

someAsyncThing()
.catch(function(error) {
  console.log('oh no', error);
})
.then(function() {
  console.log('carry on');
});
// oh no [ReferenceError: x is not defined]
// carry on
```
`finally()`方法用于指定不管 Promise 对象最后状态如何，都会执行的操作。该方法是 ES2018 引入标准的。
```javascript
promise
.then(result => {···})
.catch(error => {···})
.finally(() => {···});
```
---
#### Promise链
使用链式调用来实现对结果和错误的精细处理：
```javascript
let promise = new Promise(function (res,rej) {
    res(1);
})

promise.then((res) => {

    console.log(res);//1
    return res * 2;

}).then((res) => {

    console.log(res);//2
    return res * 2;

}).finally(() => {

    console.log('finished!!!');//finished!!!
    
})
```
![[Pasted image 20250628004354.png]]

如果将一个promise对象上添加多个then，他们是彼此独立的，并不是一个链式的结构。
![[Pasted image 20250628004333.png]]

`.then(handler)` 中所使用的处理程序（handler）可以创建并返回一个 promise。

确切地说，处理程序返回的不完全是一个 promise，而是返回的被称为 “thenable” 对象 —— 一个具有方法 `.then` 的任意对象。它会被当做一个 promise 来对待。

这个想法是，第三方库可以实现自己的“promise 兼容（promise-compatible）”对象。它们可以具有扩展的方法集，但也与原生的 promise 兼容，因为它们实现了 `.then` 方法。

---
```javascript
let promise = fetch(url);
```
执行这条语句，向 `url` 发出网络请求并返回一个 promise。当远程服务器返回 header（是在 **全部响应加载完成前**）时，该 promise 使用一个 `response` 对象来进行 resolve。

```javascript
fetch('/article/promise-chaining/user.json')
  // 当远程服务器响应时，下面的 .then 开始执行
  .then(function(response) {
    // 当 user.json 加载完成时，response.text() 会返回一个新的 promise
    // 该 promise 以加载的 user.json 为 result 进行 resolve
    return response.text();
  })
  .then(function(text) {
    // ……这是远程文件的内容
    alert(text); // {"name": "iliakan", "isAdmin": true}
  });
```

从 `fetch` 返回的 `response` 对象还包含 `response.json()` 方法，该方法可以读取远程数据并将其解析为 JSON。
```javascript
// 同上，但使用 response.json() 将远程内容解析为 JSON
fetch('/article/promise-chaining/user.json')
  .then(response => response.json())
  .then(user => alert(user.name)); // iliakan，获取到了用户名
```

---
```javascript
promise.then(f1, f2);

promise.then(f1).catch(f2);
```
这两个例子是不一样的：
不同之处在于，如果 `f1` 中出现 error，那么在这儿它会被 `.catch` 处理
`.then` 将 result/error 传递给下一个 `.then/.catch`。所以在第一个例子中，在下面有一个 `catch`，而在第二个例子中并没有 `catch`，所以 error 未被处理。

---
#### 错误处理
正如我们已经注意到的，链尾端的 `.catch` 的表现有点像 `try..catch`。我们可能有许多个 `.then` 处理程序，然后在尾端使用一个 `.catch` 处理上面的所有 error。

在常规的 `try..catch` 中，我们可以分析 error，如果我们无法处理它，可以将其再次抛出。对于 promise 来说，这也是可以的。

如果我们在 `.catch` 中 `throw`，那么控制权就会被移交到下一个最近的 error 处理程序。如果我们处理该 error 并正常完成，那么它将继续到最近的成功的 `.then` 处理程序。

```javascript
new Promise(function(resolve, reject) {
  setTimeout(() => {
    throw new Error("Whoops!");
  }, 1000);
}).catch(alert);
```
不会进行处理，这里的错误并不是在 executor 运行时生成的，而是在稍后生成的。因此，promise 无法处理它。


# Promise的静态方法（API）
---
##### all
**如果任意一个 promise 被 reject，由 `Promise.all` 返回的 promise 就会立即 reject，并且带有的就是这个 error。**
假设我们希望并行执行多个 promise，并等待所有 promise 都准备就绪。
```javascript
let promise = Promise.all(iterable);
```
`Promise.all` 接受一个可迭代对象（通常是一个==数组项为 promise 的数组==），并返回一个新的 promise。

当所有给定的 promise 都 resolve 时，新的 promise 才会 resolve，并且其结果数组将成为新 promise 的结果。
```javascript
let names = ['iliakan', 'remy', 'jeresig'];

let requests = names.map(name => fetch(`https://api.github.com/users/${name}`));

Promise.all(requests)
  .then(responses => {
    // 所有响应都被成功 resolved
    for(let response of responses) {
      alert(`${response.url}: ${response.status}`); // 对应每个 url 都显示 200
    }

    return responses;
  })
  // 将响应数组映射（map）到 response.json() 数组中以读取它们的内容
  .then(responses => Promise.all(responses.map(r => r.json())))
  // 所有 JSON 结果都被解析："users" 是它们的数组
  .then(users => users.forEach(user => alert(user.name)));
```
如果其中一个 promise 被 reject，`Promise.all` 就会立即被 reject，==完全忽略==列表中==其他的 promise==。它们的结果也被忽略。

例如，像上面那个例子，如果有多个同时进行的 `fetch` 调用，其中一个失败，其他的 `fetch` 操作仍然会继续执行，但是 `Promise.all` 将不会再关心（watch）它们。它们可能会 settle，但是它们的结果将被忽略。

`Promise.all` 没有采取任何措施来取消它们，因为 promise 中没有“取消”的概念。在 [另一个章节](https://zh.javascript.info/fetch-abort) 中，我们将介绍可以帮助我们解决这个问题（译注：指的是“取消” promise）的 `AbortController`，但它不是 Promise API 的一部分。
##### allSettled:
`Promise.allSettled` 等待所有的 promise 都被 settle，无论结果如何。结果数组会是这样的：
- 对成功的响应，结果数组对应元素的内容为 `{status:"fulfilled", value:result}`，
- 对出现 error 的响应，结果数组对应元素的内容为 `{status:"rejected", reason:error}`。
```javascript
let urls = [
  'https://api.github.com/users/iliakan',
  'https://api.github.com/users/remy',
  'https://no-such-url'
];

Promise.allSettled(urls.map(url => fetch(url)))
  .then(results => { // (*)
    results.forEach((result, num) => {
      if (result.status == "fulfilled") {
        alert(`${urls[num]}: ${result.value.status}`);
      }
      if (result.status == "rejected") {
        alert(`${urls[num]}: ${result.reason}`);
      }
    });
  });

[
  {status: 'fulfilled', value: ...response...},
  {status: 'fulfilled', value: ...response...},
  {status: 'rejected', reason: ...error object...}
]
```

没看完

---
### Promisification
指将一个接受回调的函数转换为一个返回 promise 的函数。
```javascript
//改造前
function loadScript(src, callback) {
  let script = document.createElement('script');
  script.src = src;

  script.onload = () => callback(null, script);
  script.onerror = () => callback(new Error(`Script load error for ${src}`));

  document.head.append(script);
}

// 用法：
// loadScript('path/script.js', (err, script) => {...})


//改造后
let loadScriptPromise = function(src) {
  return new Promise((resolve, reject) => {
    loadScript(src, (err, script) => {
      if (err) reject(err);
      else resolve(script);
    });
  });
};

// 用法：
// loadScriptPromise('path/script.js').then(...)
```

在实际开发中，我们可能需要 promise 化很多函数，所以使用一个 helper（辅助函数）很有意义。
我们将其称为 `promisify(f)`：它接受一个需要被 promise 化的函数 `f`，并返回一个包装（wrapper）函数。
```javascript
function promisify(f) {

  return function (...args) { // 返回一个包装函数（wrapper-function） (*)
  
    return new Promise((resolve, reject) => {
      function callback(err, result) { // 我们对 f 的自定义的回调 (**)
        if (err) {
          reject(err);
        } else {
          resolve(result);
        }
        
      }

      args.push(callback); // 将我们的自定义的回调附加到 f 参数（arguments）的末尾
      f.call(this, ...args); // 调用原始的函数
    });

  };
  
}

// 用法：
let loadScriptPromise = promisify(loadScript);
loadScriptPromise(...).then(...);
```

---
#### 微任务
promise 的处理程序 `.then`、`.catch` 和 `.finally` 都是异步的。
即便一个 promise 立即被 resolve，`.then`、`.catch` 和 `.finally` 在promise后的代码也会在这些处理程序之前被执行：
```javascript
let promise = Promise.resolve();

promise.then(() => alert("promise done!"));

alert("code finished"); // 这个 alert 先显示
```

异步任务需要适当的管理。为此，ECMA 标准规定了一个内部队列 `PromiseJobs`，通常被称为“微任务队列（microtask queue）”（V8 术语）:
- 队列（queue）是先进先出的：首先进入队列的任务会首先运行。
- 只有在 JavaScript 引擎中没有其它任务在运行时，才开始执行任务队列中的任务。

当一个 promise 准备就绪时，它的 `.then/catch/finally` 处理程序就会被放入队列中：但是它们不会立即被执行。当 JavaScript 引擎执行完当前的代码，它会从队列中获取任务并执行它。
![[Pasted image 20250628135940.png]]

**如果一个 promise 的 error 未被在微任务队列的末尾进行处理，则会出现“未处理的 rejection”。**

---
#### async/await
promise在解决地狱回调的同时，但在使用时有一些不优雅
async/await 是以更舒适的方式使用 promise 的一种特殊语法，同时它也非常易于理解和使用。

使用async关键字在函数前，函数就会总是返回一个promise对象。其他值将自动被包装在一个 resolved 的 promise 中。

**await只在 async 函数内工作**，关键字 `await` 让 JavaScript 引擎等待直到 promise 完成（settle）并返回结果

像 `promise.then` 那样，`await` 允许我们使用 thenable 对象（那些具有可调用的 `then` 方法的对象）。这里的想法是，第三方对象可能不是一个 promise，但却是 promise 兼容的：如果这些对象支持 `.then`，那么就可以对它们使用 `await`。

要声明一个 class 中的 async 方法，只需在对应方法前面加上 `async` 即可：
```javascript
class Waiter {
  async wait() {
    return await Promise.resolve(1);
  }
}

new Waiter()
  .wait()
  .then(alert); // 1（alert 等同于 result => alert(result)）
```

```javascript
async function f() {

  try {
    let response = await fetch('http://no-such-url');
  } catch(err) {
    alert(err); // TypeError: failed to fetch
  }
}

f();

async function f() {
  let response = await fetch('http://no-such-url');
}

// f() 变成了一个 rejected 的 promise
f().catch(alert); // TypeError: failed to fetch // (*)
```
当我们使用 `async/await` 时，几乎就不会用到 `.then` 了，因为 `await` 为我们处理了等待。并且我们使用常规的 `try..catch` 而不是 `.catch`。这通常更加方便。

使用同步的写法来实现异步的效果，十分的优雅
![[Pasted image 20250830122151.png]]


![[Pasted image 20250830122623.png]]
这个函数中使用 `await` 是因为 `axios(...)` 会返回一个 **Promise 对象**，而 `await` 的作用正是等待这个 Promise 完成（成功或失败），并获取其返回结果。

具体原因如下：
1. `axios` 是基于 Promise 的请求库，调用 `axios(...)` 后会立即返回一个 Promise（此时请求正在异步执行），而非直接返回接口响应数据。
    
2. 若不使用 `await`，代码会继续执行后续的 `list.value = res.data.list`，但此时 `res` 还未获取到真正的响应结果（因为请求还没完成），会导致 `res` 是一个未完成的 Promise，进而报错。
    
3. 使用 `await` 后，函数会暂停执行，等待 `axios` 的请求完成并拿到响应结果后，再将结果赋值给 `res`，确保后续代码能正确使用接口返回的数据。
    

简单说，`await` 是为了**将异步请求的结果 “同步化” 处理**，让代码按照 “发送请求→等待结果→处理结果” 的逻辑顺序执行，避免异步操作导致的数据获取时机问题。