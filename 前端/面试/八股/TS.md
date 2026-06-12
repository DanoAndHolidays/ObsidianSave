# TS

### 【Q676】在 Typescript 中如何实现类型标记 Pick 与 Omit
```typescript
// Pick：从 T 中选取部分属性
type MyPick<T, K extends keyof T> = {
  [P in K]: T[P];
};

// Omit：从 T 中排除部分属性
type MyOmit<T, K extends keyof T> = {
  [P in Exclude<keyof T, K>]: T[P];
};
// 或用 Pick + Exclude
type MyOmit<T, K extends keyof T> = Pick<T, Exclude<keyof T, K>>;
```

### 【Q692】什么是协变与逆变
- **协变（Covariance）**：子类型可以赋值给父类型。如 `Array<Cat>` 是 `Array<Animal>` 的子类型（TS 默认给数组协变）
- **逆变（Contravariance）**：父类型可以赋值给子类型。主要出现在函数参数中。`(Animal) => void` 是 `(Cat) => void` 的子类型
- **双变（Bivariance）**：TS 中方法参数的默认行为（不开启 strictFunctionTypes）

规则总结：返回值协变，参数逆变（严格模式下）。赋值兼容性跟随这个原则。

### 【Q693】在 ts 中如何实现 Partial
```typescript
type MyPartial<T> = {
  [P in keyof T]?: T[P];
};
// Partial<User> → 所有属性变成可选的
```

### 【Q694】在 ts 中什么是 infer，并实现 Parameters 与 ReturnType
`infer` 在条件类型中声明一个待推断的类型变量。
```typescript
// Parameters：获取函数参数类型
type MyParameters<T extends (...args: any) => any> = T extends (...args: infer P) => any ? P : never;

// ReturnType：获取函数返回值类型
type MyReturnType<T extends (...args: any) => any> = T extends (...args: any) => infer R ? R : never;
```

### 【Q706】typescript 中 interface 与 type 有何区别
- **interface**：描述对象结构，支持声明合并（同名 interface 自动合并），可被类 implements
- **type**：类型别名，可为任何类型命名（包括联合类型、交叉类型、元组）。不支持声明合并。
- **共同点**：都可描述对象结构、都可以扩展（interface extends type / type & type）
- **选择**：优先 interface（面向对象场景、声明合并需求），联合/交叉/元组/映射类型用 type

### 【Q707】请简述 typescript 中的 infer
同 Q694。`infer` 在条件类型（`extends`）中引入类型变量，用于从现有类型中提取部分类型信息。例如提取 Promise 的 value 类型 (`Awaited`)、提取函数参数 (`Parameters`)、提取返回值 (`ReturnType`) 等。
