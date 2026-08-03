# 用neverthrow进行错误处理
这个模式来自 Rust 的 Result 枚举。核心思路是：用返回值代替 throw。                                  

传统的 try-catch 是这样的：                                                                         
```ts
  // 传统写法 — 错误被"扔"出去                                                              
  try {                                                       
    const data = await someService();  // 你不知道它会扔什么
    return { data };
  } catch (error) {
    // error 是 unknown 类型，也不知道到底是谁扔的
  }
```

  neverthrow 的做法是让函数 **主动返回** Ok 或 Err，不扔异常：
```ts
  // neverthrow 写法 — 错误是函数的正常返回值
  async function createRule(input) {
    if (!input.name) {
      return err(new Error('名称不能为空'));  // 返回 Err，不 throw
    }
    return ok(await db.insert(rule).values(input));  // 返回 Ok
  }
```

  .match() 是这个类型的"分叉处理"方法。它强制你必须同时处理成功和失败两种情况：
```ts
  const result = await createRule(input);

  return result.match(
    // 第一个回调：成功分支，data 就是 ok() 里的值
    (data) => ({ data }),
    // 第二个回调：失败分支，error 就是 err() 里的 Error
    (error) => { throw new TRPCError({ code: 'BAD_REQUEST', message: error.message }) }
  );
```

  为什么这样做？ 拆开看：
  1. 函数不可能"意外崩溃" — Result 把错误变成了类型系统的一部分，用 err() 返回的错误照样会被 .match()接收到
  2. .match() 强制两个分支都写 — 你无法忘记处理错误，TypeScript 会让你编译不过
  3. 错误信息不丢失 — 一路传到 router 再转成 tRPC 的 TRPCError，最终变成前端能理解的 HTTP 错误响应

  数据流向：DAO err() → Service 透传 → Router .match() → TRPCError → 前端