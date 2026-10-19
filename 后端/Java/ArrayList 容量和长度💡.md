# ArrayList 容量和长度
你这里遇到的是 Java `ArrayList` 中一个非常重要的区别：容量（capacity）≠ 长度（size）
```
List<Integer> ans = new ArrayList<Integer>(equsl);

System.out.println(ans.size()); // 0
```

即使你传入了 `equsl`，`ans.size()` 仍然是 `0`

|概念|含义|获取方式|
|---|---|---|
|`size`|当前实际存储的元素数量|`list.size()`|
|`capacity`|底层数组当前能够容纳的元素数量|没有公开的获取方法|

例如：
```
List<Integer> list = new ArrayList<>(10);

System.out.println(list.size()); // 0

list.add(100);
list.add(200);

System.out.println(list.size()); // 2
```

这里的 `10` 只是初始容量，表示底层数组可以容纳 10 个元素，而不需要扩容。

并不是说已经存在 10 个元素

实际上，`ArrayList` 底层使用数组存储元素，简化后可以理解为：
```
class ArrayList<E> {
    Object[] elementData; // 底层数组
    int size;             // 实际元素数量
}
```

假设：
```
ArrayList<Integer> list = new ArrayList<>(5);
```

点击 add()，观察 size 增长，而底层容量不变。`capacity` 是内部实现细节，Java 的 `ArrayList` 没有提供公开的 `capacity()` 方法。

可以使用：
```
List<Integer> list = new ArrayList<>(
    Collections.nCopies(5, 0)
);

System.out.println(list.size()); // 5
```

初始化的时候就有指定数量的元素

这样列表中就真的存在 5 个元素，初始值全部为 `0`。

