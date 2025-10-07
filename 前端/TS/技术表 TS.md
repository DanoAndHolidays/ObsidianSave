# TypeScript 基础语法
---
##### 环境配置
```bash
# [修正命令]：安装 TypeScript
npm install typescript -g

# 编译 TS 文件
tsc filename.ts
```

##### 基本类型注解
```typescript
// 基本类型
let a: string = 'abc';
let b: number = 3;
let c: boolean = true;

// 数组类型
let d: string[] = ['a', 'b', 'c'];
let e: Array<number> = [1, 2, 3];

// 元组类型 [修正术语：无组→元组]
let f: [number, string] = [2, 'c'];

// 特殊类型
let g: any = 1;      // 任意类型
let h: void = undefined; // 无类型
let i: null = null;  // null
let j: undefined = undefined; // undefined
```

##### 函数类型注解
```typescript
// 函数返回值类型注解
function hello(name: string): string {
    return 'hello ' + name;
}

// 无返回值函数
function log(message: string): void {
    console.log(message);
}
```

---