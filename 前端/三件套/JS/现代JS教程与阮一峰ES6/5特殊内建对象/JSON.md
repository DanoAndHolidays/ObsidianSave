# JSON
---
JavaScript 提供了如下方法：
- `JSON.stringify` 将对象转换为 JSON。
- `JSON.parse` 将 JSON 转换回对象。

JSON 编码的对象与对象字面量有几个重要的区别：
- ==字符串使用双引号==。JSON 中没有单引号或反引号。所以 `'John'` 被转换为 `"John"`。
- 对象==属性名称==也是==双引号==的。这是强制性的。所以 `age:30` 被转换成 `"age":30`。

`JSON.stringify` 也可以应用于原始（primitive）数据类型。
JSON 支持以下数据类型：
- Objects `{ ... }`
- Arrays `[ ... ]`
- Primitives：
    - strings，
    - numbers，
    - boolean values `true/false`，
    - `null`。

JSON 是语言无关的纯数据规范，因此一些特定于 JavaScript 的对象属性会被 `JSON.stringify` 跳过。即：
- 函数属性（方法）。
- Symbol 类型的键和值。
- 存储 `undefined` 的属性。

重要的限制：==不得有循环引用==。
支持嵌套对象转换，并且可以自动对其进行转换。

```javascript
let obj = {
    name: 'dano',
    age: 21,
    foods: {
        apple: 23,
        peal: 34,
        shit: {
            wee: 21,
            ui:8,
        }
    }
}

let json = JSON.stringify(obj);
console.log(json);
//{"name":"dano","age":21,"foods":{"apple":23,"peal":34,"shit":{"wee":21,"ui":8}}}

let json2 = JSON.stringify(obj, ( key,value) => {
    return ((key == 'name')) ? undefined : value;
})
console.log(json2);
//{"age":21,"foods":{"apple":23,"peal":34,"shit":{"wee":21,"ui":8}}}
```

JSON.stringify有三个参数：
- value 要编码的对象。
- replacer 要编码的属性数组或映射函数 `function(key, value)`。
- space 用于格式化的空格数量。
```JSON
{
    "age": 21,
    "foods": {
        "apple": 23,
        "peal": 34,
        "shit": {
            "wee": 21,
            "ui": 8
        }
    }
}
```

使用自定义的toJSON：
像 `toString` 进行字符串转换，对象也可以提供 `toJSON` 方法来进行 JSON 转换。如果可用，`JSON.stringify` 会自动调用它。
 ```javascript
 let obj = {
    name: 'dano',
    age: 21,
    foods: {
        apple: 23,
        peal: 34,
        shit: {
            wee: 21,
            ui:8,
        }
    },

    toJSON() {
        return this.name;  //"dano"
    }
}
```

使用JSON.prase来将JSON转换为对象：
```javascript
let object = JSON.parse(json);
console.log(object);
```

```json
{
  name: 'dano',
  age: 21,
  foods: { apple: 23, peal: 34, shit: { wee: 21, ui: 8 } }
}
```

 此函数有两个参数：
 str
要解析的 JSON 字符串。

reviver
可选的函数 function(key,value)，该函数将为每个 `(key, value)` 对调用，并可以对值进行转换。


从服务器上获取的JSON的data的值是字符串，使用reviver将其转换为Data。其对嵌套的对象也起作用
```javascript
let str = '{"title":"Conference","date":"2017-11-30T12:00:00.000Z"}';

let meetup = JSON.parse(str, function (key, value) {
    if (key == 'date') return new Date(value);
    return value;
});

console.log(meetup.date.getDate());//30
```

