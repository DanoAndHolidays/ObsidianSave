### 构造函数
---
构造函数在技术上是常规函数。不过有两个约定：
1. 它们的命名以==大写字母==开头。
2. 它们==只能由 `"new"`== 操作符来执行。

当一个函数被使用 `new` 操作符执行时，它按照以下步骤：
1. 一个==新的空对象==被创建并==绑定给 `this`==。（如果是内置的对象还要链接到原型链）
2. 函数体执行。通常它会修改 `this`，为其添加新的属性。
3. 返回 `this` 的值。构造器没有 `return` 语句。

但是，如果这有一个 `return` 语句，那么规则就简单了：
- 如果 `return` 返回的是一个对象，则返回这个对象，而不是 `this`。
- 如果 `return` 返回的是一个原始类型，则忽略。

从技术上讲，任何函数（除了箭头函数，它没有自己的 `this`）都可以用作构造器。即可以通过 `new` 来运行，它会执行上面的算法。“首字母大写”是一个共同的约定，以明确表示一个函数将被使用 `new` 来运行。
```javascript
function User(name, age = 0) {
    this.name = name;
    this.age = age;
    this.run = function () {
        console.log('run');
    }
    this.walk = () => {
        console.log('walk');
    }
}

let vipUser = new User('dano', 21);

console.log(vipUser.name);
vipUser.run();
vipUser.walk();
```