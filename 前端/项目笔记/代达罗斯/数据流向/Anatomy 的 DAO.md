# Anatomy 的 DAO
❯ createWithTx 与普通的create的区别是什么呢，为什么要这样去写呢                                                                                         
  ⎿  ⧉ Selected 1 lines from packages\db\src\dao\anatomies-dao.ts in Visual Studio Code

● Thinking for 6s… (ctrl+o to expand)

● 这是个非常关键的问题，理解了它才能真正会用事务。
     
  ---
  create vs createWithTx 的区别
     
  两者做的都是同一张表的 INSERT，唯一的区别是：它们在不在同一个事务里执行。

  // 普通 create：直接拿全局 db 连接插入，自己就是一个独立事务
  async create(input: AnatomyInsert): Promise<AnatomyRecord> {
    const rows = await db.insert(anatomiesTable).values(input).returning();
    return rows[0]!;
  }

  // createWithTx：用调用方传进来的 tx 插入，参与到调用方的事务里
  async createWithTx(
    tx: DatabaseTransaction,
    input: AnatomyInsert,
  ): Promise<AnatomyRecord> {
    const rows = await tx.insert(anatomiesTable).values(input).returning();
    return rows[0]!;
  }

  ---
  为什么要这样写？

  因为 Repository 需要把多张表的操作打包成一个原子操作。原子性的意思是：要么全部成功，要么全部回滚，不能出现“一半成功、一半失败”。

  以 createDraft 为例，它必须同时做两件事：

  1. 在 anatomies 表插入一条身份记录
  2. 在 anatomy_drafts 表插入一条 Draft 记录

  如果第一步成功了，第二步失败了，数据库里就会留下一个“没有 Draft 的 Anatomy”——这是脏数据。

  所以 Repository 会这样写：

  return db.transaction(async (tx) => {
    const anatomy = await anatomiesDao.createWithTx(tx, { id: crypto.randomUUID() });
    const draft = await draftsDao.createWithTx(tx, { anatomyId: anatomy.id, ... });
    return { anatomyId: anatomy.id, draftId: draft.id };
  });

  db.transaction(...) 开启一个事务，生成 tx。然后：

  - anatomiesDao.createWithTx(tx, ...) 用 tx 插入 anatomies
  - draftsDao.createWithTx(tx, ...) 用同一个 tx 插入 drafts

  如果中途任何一步报错，Drizzle 会自动回滚整个事务，两张表都不会留下数据。

  ---
  如果不用 createWithTx 会怎样？

  假设你错误地混用了 db 和 tx：

  return db.transaction(async (tx) => {
    const anatomy = await anatomiesDao.create({ id: crypto.randomUUID() }); // ❌ 用 db，不在事务里！
    const draft = await draftsDao.createWithTx(tx, { anatomyId: anatomy.id, ... });
    return { anatomyId: anatomy.id, draftId: draft.id };
  });

  这时候：

  - anatomy 已经立刻提交到数据库了
  - draft 还在事务里
  - 如果 draft 插入失败回滚，anatomy 仍然留在表里

  这就破坏了原子性。

  ---
  项目里的固定模式

  你去看 packages/db/src/dao/crates-dao.ts，它也有 create / createWithTx、update / updateWithTx、delete / deleteWithTx。这是项目里的标准写法：

  - DAO：同时提供普通版和 WithTx 版
  - Repository：需要跨表原子操作时，用 db.transaction(...) 开事务，然后把 tx 传给 DAO 的 WithTx 方法

  所以记住一条规则：

  ▎ 在 db.transaction(...) 的回调里，所有数据库操作都必须用 tx，不能再用 db。

  ---
  我接着把 repository/index.ts 的导出加上，然后跑类型检查。你还有什么想问的随时打断我。