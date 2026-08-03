# TS类型 extends

这里的：

```ts
<T extends AnatomyEntry>
```

意思是：

> `T` 可以是 `AnatomyEntry`，也可以是任何继承或符合 `AnatomyEntry` 结构的更具体类型。

它的主要作用不是限制参数本身，而是**保留传入值的具体类型**。

原代码：

```ts
const cloneEntry = function <T extends AnatomyEntry>(entry: T): T {
  return JSON.parse(JSON.stringify(entry)) as T;
};
```

## 不使用泛型会怎样

假设直接写成：

```ts
const cloneEntry = function (entry: AnatomyEntry): AnatomyEntry {
  return JSON.parse(JSON.stringify(entry)) as AnatomyEntry;
};
```

再假设有两个具体类型：

```ts
type FileEntry = AnatomyEntry & {
  type: "file";
  extension: string;
};

type DirectoryEntry = AnatomyEntry & {
  type: "directory";
  children: AnatomyEntry[];
};
```

传入一个 `FileEntry`：

```ts
const file: FileEntry = {
  name: "index",
  type: "file",
  extension: "ts",
};

const cloned = cloneEntry(file);
```

此时 `cloned` 的类型只是：

```ts
AnatomyEntry
```

TypeScript 会丢失 `FileEntry` 的具体信息，因此访问：

```ts
cloned.extension;
```

可能会报错，因为 `AnatomyEntry` 不一定有 `extension`。

## 使用泛型之后

```ts
const cloneEntry = function <T extends AnatomyEntry>(entry: T): T {
  return JSON.parse(JSON.stringify(entry)) as T;
};
```

调用时：

```ts
const cloned = cloneEntry(file);
```

TypeScript 会根据参数自动推断：

```ts
T = FileEntry
```

所以返回值类型也是：

```ts
FileEntry
```

于是可以正常访问：

```ts
cloned.extension;
```

也就是说，这个函数表达的是：

> 你传进来什么具体类型，我就返回同样的具体类型。

类型关系可以理解为：

```ts
FileEntry -> FileEntry
DirectoryEntry -> DirectoryEntry
AnatomyEntry -> AnatomyEntry
```

而不是：

```ts
FileEntry -> AnatomyEntry
DirectoryEntry -> AnatomyEntry
```

## 为什么不能只写 `<T>`

也可以写：

```ts
const cloneEntry = function <T>(entry: T): T {
  return JSON.parse(JSON.stringify(entry)) as T;
};
```

这会接受任何类型：

```ts
cloneEntry(123);
cloneEntry("hello");
cloneEntry({ foo: true });
```

但从函数名和业务来看，它只应该克隆 `AnatomyEntry` 类型的数据。

所以加上：

```ts
T extends AnatomyEntry
```

是在给泛型增加约束：

```ts
const cloneEntry = function <T extends AnatomyEntry>(entry: T): T
```

表示：

1. `T` 必须符合 `AnatomyEntry`
2. 同时又保留 `T` 的具体子类型

例如：

```ts
cloneEntry(file); // 可以
cloneEntry(directory); // 可以
cloneEntry(123); // 报错
cloneEntry("hello"); // 报错
```

## 三种写法的区别

### 直接写 `AnatomyEntry`

```ts
function cloneEntry(entry: AnatomyEntry): AnatomyEntry
```

含义：

> 接收一个 `AnatomyEntry`，返回一个普通的 `AnatomyEntry`。

缺点是会丢失具体子类型。

### 只写泛型 `T`

```ts
function cloneEntry<T>(entry: T): T
```

含义：

> 接收任何类型，并返回相同类型。

范围太宽，不符合函数只处理 `AnatomyEntry` 的业务限制。

### 写 `T extends AnatomyEntry`

```ts
function cloneEntry<T extends AnatomyEntry>(entry: T): T
```

含义：

> 只接收 `AnatomyEntry` 及其具体子类型，并保留传入的具体类型。

这是这里最准确的表达。

## 一个更直观的例子

```ts
type Animal = {
  name: string;
};

type Dog = Animal & {
  bark(): void;
};
```

不使用泛型：

```ts
function copyAnimal(animal: Animal): Animal {
  return animal;
}

const dog: Dog = {
  name: "旺财",
  bark() {},
};

const result = copyAnimal(dog);

result.bark(); // 报错，因为 result 只是 Animal
```

使用受约束泛型：

```ts
function copyAnimal<T extends Animal>(animal: T): T {
  return animal;
}

const result = copyAnimal(dog);

result.bark(); // 正常，因为 result 是 Dog
```

## 不过这段克隆代码本身有风险

```ts
JSON.parse(JSON.stringify(entry)) as T
```

这里的 `as T` 只是告诉 TypeScript：“相信我，结果还是 `T`。”

但运行时不一定真的如此。例如下面这些内容会丢失或改变：

```ts
Date
undefined
Map
Set
函数
Symbol
循环引用
```

例如：

```ts
const value = {
  date: new Date(),
};

const cloned = JSON.parse(JSON.stringify(value));
```

克隆后的 `date` 会变成字符串，而不是 `Date` 对象。

现代环境中更适合使用：

```ts
const cloneEntry = function <T extends AnatomyEntry>(entry: T): T {
  return structuredClone(entry);
};
```

前提是 `AnatomyEntry` 中的数据可以被 `structuredClone` 克隆。

所以这里的 `extends` 可以概括为：

> 限制这个函数只能处理 `AnatomyEntry`，同时确保传入具体的子类型时，返回值仍然保持那个具体子类型。
