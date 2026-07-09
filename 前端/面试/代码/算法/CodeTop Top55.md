# CodeTop Top55
> Last Format Time：7/9/2026 23:46:20

越是靠前，题目的热度越高🔥（筛选条件 岗位：前端）

这里的题目的编号和LeetCode一致，与另一个文档相同的题目只有编号。
据我统计，岗位不限中，前80道题目全部做完，基本上可以覆盖前端常考的题目，前端做前55道就可以了。

---
## 3 无重复字符的最长子串 ⌚️
#双指针 #滑动窗口
https://leetcode.cn/problems/longest-substring-without-repeating-characters/description/

```js
var lengthOfLongestSubstring = function(s) {
    let ans = 0;
    let left = 0;
    const cnt = new Map(); // 维护从下标 left 到下标 right 的字符
    for (let right = 0; right < s.length; right++) {
        const c = s[right];
        cnt.set(c, (cnt.get(c) ?? 0) + 1);
        while (cnt.get(c) > 1) { // 窗口内有重复字母
            cnt.set(s[left], cnt.get(s[left]) - 1); // 移除窗口左端点字母
            left++; // 缩小窗口
        }
        ans = Math.max(ans, right - left + 1); // 更新窗口长度最大值
    }
    return ans;
};
```

---
## 165 比较版本号 ⌚️
#字符串
https://leetcode.cn/problems/compare-version-numbers/description/
给你两个 **版本号字符串** `version1` 和 `version2` ，请你比较它们。版本号由被点 `'.'` 分开的修订号组成。**修订号的值** 是它 **转换为整数** 并忽略前导零。

比较版本号时，请按 **从左到右的顺序** 依次比较它们的修订号。如果其中一个版本字符串的修订号较少，则将缺失的修订号视为 `0`。

```js
// 输入：version1 = "1.2", version2 = "1.10"
var compareVersion = function (version1, version2) {

    const a = version1.split(".");
    const b = version2.split(".");

    console.log(a, b)
    // [ '1', '2' ] [ '1', '10' ]

    const n = a.length, m = b.length;

    for (let i = 0; i < n || i < m; i++) {
        // 越界的可以用空值合并
        const ver1 = i < n ? parseInt(a[i]) : 0;
        const ver2 = i < m ? parseInt(b[i]) : 0;
        if (ver1 !== ver2) {
            return ver1 < ver2 ? -1 : 1;
        }
    }
    return 0;
};
```

---
## 88 合并两个有序数组
#双指针
https://leetcode.cn/problems/merge-sorted-array/description/

两个按 **非递减顺序** 排列的整数数组 `nums1` 和 `nums2`，另有两个整数 `m` 和 `n` ，分别表示 `nums1` 和 `nums2` 中的元素数目。

请你 **合并** `nums2` 到 `nums1` 中，使合并后的数组同样按 **非递减顺序** 排列。

**注意：** 最终，合并后数组不应由函数返回，而是存储在数组 `nums1` 中。为了应对这种情况，`nums1` 的初始长度为 `m + n`，其中前 `m` 个元素表示应合并的元素，后 `n` 个元素为 `0` ，应忽略。`nums2` 的长度为 `n` 。

```js
/**
 Do not return anything, modify nums1 in-place instead.
 */
function merge(nums1: number[], m: number, nums2: number[], n: number): void {
    // 不可以从左到右去覆盖nums1，会丢失后面的项，我们可以从右向左去覆盖

    let index1 = m - 1
    let index2 = n - 1
    let endOfNums1 = m + n - 1

    while (index2 >= 0) {
        if (nums1[index1] >= nums2[index2]) {
            nums1[endOfNums1] = nums1[index1]

            index1--
            endOfNums1--
        } else {
            nums1[endOfNums1] = nums2[index2]

            index2--
            endOfNums1--
        }
    }

    console.log(nums1)
    // 不需要返回值
};
```

---
## 20 有效括号
#栈 #简单
https://leetcode.cn/problems/valid-parentheses/description/

---
## 415 字符串相加 ⌚️
#双指针 
https://leetcode.cn/problems/add-strings/description/

---
## 1 两数之和
#哈希表 
https://leetcode.cn/problems/two-sum/description/

---
## 46 全排列
#回溯 
https://leetcode.cn/problems/permutations/description/
有点忘了，重新做一遍：
```js
function permute(nums: number[]): number[][] {
    let ans = []
    let n = nums.length
    let path = Array(n).fill(0)
    let onPath = Array(n).fill(false)

    // 代表下标为i的位的选择
    function dfs(i) {
        if (i === n) {
            ans.push(path.slice())
            return
        }
        // 遍历nums中的每一项，将每种不在path中的值加入path 
        for (let j = 0; j < n; j++) {
            if (!onPath[j]) {
                path[i] = nums[j]

                // 加入后，再确定下一位
                onPath[j] = true
                dfs(i + 1)

                // 回溯
                onPath[j] = false
            }
        }
    }

    dfs(0)
    return ans
};
```

---
## 206 反转链表
#链表 
https://leetcode.cn/problems/reverse-linked-list/

```js
/**
 * Definition for singly-linked list.
 * function ListNode(val, next) {
 *     this.val = (val===undefined ? 0 : val)
 *     this.next = (next===undefined ? null : next)
 * }
 */
/**
 * @param {ListNode} head
 * @return {ListNode}
 */
var reverseList = function (head) {
    let cur = head
    
    // pre节点始终是头插法的头结点 
    let pre = null
	
    // 使用头插法
    while (cur) {
        // 保存当前节点的下一个
        const nxt = cur.next
		
        // 将当前节点放在pre节点的前面
        cur.next = pre
		
        // pre向前移动一个
        pre = cur
		
        // cur向后移动一个
        cur = nxt
    }
};
```

---
## 102 二叉树的层序遍历
#二叉树 

```js
const levelOrder = (root) => {
    if (root === null) return []
    const ans = []

    let cur = [root]

    while (cur.length) {
        const nxt = []
        const vals = []
        
        for (const node of cur) {
            vals.push(node.val)
            if (node.left) nxt.push(node.left)
            if (node.right) nxt.push(node.right)
        }
        cur = nxt
        ans.push(vals)
    }
    return ans
}
```

---
## 53 最大子数组和
#动态规划 

```js
/**
 * @param {number[]} nums
 * @return {number}
 */
var maxSubArray = function (nums) {
    // dp[i] 表示长度为i的数组的最大子数和
    // dp[i] = Math.max(dp[i - 1], 0) + nums[i]
    // dp[i] = 0
    let n = nums.length
    let dp = Array(n).fill(0)
    dp[0] = nums[0]

    for (let i = 1; i < n; i++) {
        dp[i] = Math.max(dp[i - 1], 0) + nums[i]
    }

    return Math.max(...dp)
};
```

---
## 121 买卖股票的最佳时机
#贪心 
https://leetcode.cn/problems/best-time-to-buy-and-sell-stock/description/

```js
/**
 * @param {number[]} prices
 * @return {number}
 */
var maxProfit = function (prices) {
    // min表示当前价格前面的最小价格
    let min = prices[0]

    let ans = 0

    for (const price of prices) { 
        ans = Math.max(ans, price - min)
        min = Math.min(min, price)
    }

    return ans
};
```

---
## 三数之和
https://leetcode.cn/problems/3sum/description/
#双指针 

这里我在实现的时候是选了一个数，然后去找它后面的数。如果我选择一个数，去找它前面一个、后面一个数会怎么样呢？

```js
function threeSum(nums: number[]): number[][] {
    // 先排序，排序后遍历每一项
    nums.sort((a, b) => a - b)
    const ans = []
    const n = nums.length

    for (let i = 0; i < n - 2; i++) {
        const x = nums[i]

        // 如果当前项和上一项是一样的，那么他们形成的答案肯定是一样的，所以跳过
        if (i > 0 && x === nums[i - 1]) continue

        // 初始化j与k的位置
        let j = i + 1
        let k = n - 1

        while (j < k) {
            let s = x + nums[j] + nums[k]
            if (s > 0) {
                k--
            } else if (s < 0) {
                j++
            } else {
                ans.push([x, nums[j], nums[k]])

                // 这里也是为了保证j与k是不一样的
                j++
                while (j < k && nums[j] === nums[j - 1]) { j++ }

                k--
                while (j < k && nums[k] === nums[k + 1]) { k-- }
            }
        }
    }

    return ans
};
```

---
## 146 LRU缓存机制
https://leetcode.cn/problems/lru-cache/description/

---
## 141 环形链表
---
## 112 路径总和
#链表 
https://leetcode.cn/problems/path-sum/
这道没做过

```js
function hasPathSum(root: TreeNode | null, targetSum: number): boolean {
    if (root === null) return false

    targetSum -= root.val

	// 这种情况下，是叶子节点，就直接返回结果
    if (root.left === null && root.right === null) return targetSum === 0

	// 这种情况下的话，就是原问题类似的子问题，递归的调用
    return hasPathSum(root.left, targetSum) || hasPathSum(root.right, targetSum)
};
```

---
## 21 合并两个有序链表
---
## 215 数组中的第K大
https://leetcode.cn/problems/kth-largest-element-in-an-array/description/
在数组中，随机的选一个数，以它为准，将小于的放在其左侧，大于的在右侧，如果这个数正好是第k个，那么他就是第k大，如果不是，那就在左右两侧继续找

---
## 912 快排
https://leetcode.cn/problems/sort-an-array/solutions/3799866/onlogn-kuai-su-pai-xu-fen-zhi-xie-fa-you-njpq/

```js
// 在子数组 [left, right] 中随机选择一个基准元素 pivot
// 根据 pivot 重新排列子数组 [left, right]
// 重新排列后，<= pivot 的元素都在 pivot 的左侧，>= pivot 的元素都在 pivot 的右侧
// 返回 pivot 在重新排列后的 nums 中的下标
// 特别地，如果子数组的所有元素都等于 pivot，我们会返回子数组的中心下标，避免退化
function partition(nums, left, right) {
    // 1. 在子数组 [left, right] 中随机选择一个基准元素 pivot
    const idx = left + Math.floor(Math.random() * (right - left + 1));
    const pivot = nums[idx];
    // 把 pivot 与子数组第一个元素交换，避免 pivot 干扰后续划分，从而简化实现逻辑
    [nums[idx], nums[left]] = [nums[left], nums[idx]];

    // 2. 相向双指针遍历子数组 [left + 1, right]
    // 循环不变量：在循环过程中，子数组的数据分布始终如下图
    // [ pivot | <=pivot | 尚未遍历 | >=pivot ]
    //   ^                 ^     ^         ^
    //   left              i     j         right

    let i = left + 1, j = right;
    while (true) {
        while (i <= j && nums[i] < pivot) {
            i++;
        }
        // 此时 nums[i] >= pivot

        while (i <= j && nums[j] > pivot) {
            j--;
        }
        // 此时 nums[j] <= pivot

        if (i >= j) {
            break;
        }

        // 维持循环不变量
        [nums[i], nums[j]] = [nums[j], nums[i]];
        i++;
        j--;
    }

    // 循环结束后
    // [ pivot | <=pivot | >=pivot ]
    //   ^             ^   ^     ^
    //   left          j   i     right

    // 3. 把 pivot 与 nums[j] 交换，完成划分（partition）
    // 为什么与 j 交换？
    // 如果与 i 交换，可能会出现 i = right + 1 的情况，已经下标越界了，无法交换
    // 另一个原因是如果 nums[i] > pivot，交换会导致一个大于 pivot 的数出现在子数组最左边，不是有效划分
    // 与 j 交换，即使 j = left，交换也不会出错
    [nums[left], nums[j]] = [nums[j], nums[left]];

    // 返回 pivot 的下标
    return j;
}

// 快速排序子数组 [left, right]
function quickSort(nums, left, right) {
    // 优化：如果子数组已是升序，直接返回
    let ordered = true;
    for (let i = left; i < right; i++) {
        if (nums[i] > nums[i + 1]) {
            ordered = false;
            break;
        }
    }
    if (ordered) {
        return;
    }

    const i = partition(nums, left, right); // 划分子数组
    quickSort(nums, left, i - 1);  // 排序在 pivot 左侧的元素
    quickSort(nums, i + 1, right); // 排序在 pivot 右侧的元素
}

var sortArray = function(nums) {
    quickSort(nums, 0, nums.length - 1);
    return nums;
};
```

---
## 5 最长回文子串 ⌚️
https://leetcode.cn/problems/longest-palindromic-substring/

---
## 70 爬楼梯
https://leetcode.cn/problems/climbing-stairs/
f(n) = f(n - 1) + f(n - 2)

```javascript
/**
 * @param {number} n
 * @return {number}
 */
const map = new Map()
var climbStairs = function (n) {
    if (n === 0 || n === 1) {
        return 1
    } else if (n === 2) {
        return 2
    }

    if (map.has(n)) {
        console.log('has', map.get(n))

        return map.get(n)
    } else {
        const temp = climbStairs(n - 1) + climbStairs(n - 2)
        map.set(n, temp)
        return temp
    }
}
```

---
## 54 螺旋矩阵
https://leetcode.cn/problems/spiral-matrix/description/

---
## 200 岛屿的数量
https://leetcode.cn/problems/number-of-islands/description/

---
## 300 最长上升子序列
https://leetcode.cn/problems/longest-increasing-subsequence/description/

---
## 56 区间合并 ⌚️
https://leetcode.cn/problems/merge-intervals/submissions/662938365/
给定一个表示若干个区间的集合数组intervals，每个区间由起始位置start和结束位置end组成。请合并所有重叠的区间，返回一个不重叠的区间数组，该数组需包含输入中的所有区间，并确保区间之间没有重叠。

**我写的一大坨：**

```js
function fn(arr1, arr2) {
    console.log(arr1, arr2);

    if (arr1[1] >= arr2[0]) {
        return true
    }

    return false
}

var merge = function (intervals) {
    let ans = []

    // console.log(intervals)
    intervals.sort((a, b) => a[0] < b[0])
    // console.log(intervals)

    let min = intervals[0][0]
    let max = intervals[0][1]

    for (let i = 0; i < intervals.length - 1; i++) {
        let curArr = intervals[i]
        let nxtArr = intervals[i + 1]

        if (fn(curArr, nxtArr)) {
            min = Math.min(...curArr, ...nxtArr)
            max = Math.max(...curArr, ...nxtArr)
            console.log(fn(curArr, nxtArr), min, max, '777')
        } else {
            console.log([min, max],'666')
            ans.push([min, max])
            min = 0
            max = 0
        }
    }

    ans.push([min, max])

    return ans
}
console.log(
    merge([
        [1, 2],
        [2, 3],
        [4, 6],
        
    ]),
)
// [ 1, 2 ] [ 2, 3 ]
// [ 1, 2 ] [ 2, 3 ]
// true 1 3 777
// [ 2, 3 ] [ 4, 6 ]
// [ 1, 3 ] 666
// [ [ 1, 3 ], [ 0, 0 ] ]
```

参考答案：
```js
/**
 * @param {number[][]} intervals - 输入的区间数组
 * @return {number[][]} - 合并后的区间数组
 */
var merge = function(intervals) {
    // 1. 边界处理：如果数组为空或长度小于2，无需合并
    if (!intervals || intervals.length < 2) {
        return intervals;
    }
	
    // 2. 排序：按照区间的起始位置（start）进行升序排序
    // a[0] 代表当前区间的 start，b[0] 代表下一个区间的 start
    intervals.sort((a, b) => a[0] - b[0]);
	
    // 3. 初始化结果数组，先放入第一个区间
    const merged = [intervals[0]];
	
    // 4. 遍历剩余的区间
    for (let i = 1; i < intervals.length; i++) {
        const currentInterval = intervals[i];
        
        // 获取结果数组中最后一个区间（即当前正在构建的合并区间）
        const lastMergedInterval = merged[merged.length - 1];
		
        // 5. 判断是否重叠
        // 如果当前区间的 start <= 上一个合并区间的 end，说明有重叠
        if (currentInterval[0] <= lastMergedInterval[1]) {
            // 合并操作：更新上一个合并区间的 end 为两者的最大值
            // Math.max 确保我们取到最远的结束点（例如 [1, 10] 和 [2, 6] 合并应为 [1, 10]）
            lastMergedInterval[1] = Math.max(lastMergedInterval[1], currentInterval[1]);
        } else {
            // 6. 无重叠：直接将当前区间推入结果数组
            merged.push(currentInterval);
        }
    }

    return merged;
};
```

![[Pasted image 20260608172622.png]]
我还做过呢，艹了。这肯定是没了啊，这题都没搞出来，你。。。这道好像是美团的，挂了已经

---
## 704 二分查找
https://leetcode.cn/problems/binary-search/description/

```js
function search(nums: number[], target: number): number {
    const n = nums.length
    let left = 0
    let right = n - 1

    while (left <= right) {
        let mid = Math.floor((left + right) / 2)
        if(nums[mid] === target){
            return mid
        }else if(nums[mid] > target){
            right = mid - 1
        }else{
            left = mid + 1
        }
    }

    return -1
};
```

---
## 129 求根到叶子节点的路径值和
https://leetcode.cn/problems/sum-root-to-leaf-numbers/description/

```js
var sumNumbers = function(root, x = 0) {
    if (root === null) {
        return 0;
    }
    x = x * 10 + root.val;
    if (root.left === null && root.right === null) { // root 是叶子节点
        return x;
    }
    return sumNumbers(root.left, x) + sumNumbers(root.right, x);
};
```

---
## 93 复原IP地址
https://leetcode.cn/problems/restore-ip-addresses/

```js
function restoreIpAddresses(s: string): string[] {
    // 这题的本质是选.合理的位置
    let n = s.length
    let ans = []
    let path = []
	
    if (n < 4 || n > 12) return ans
	
    // 表示从i开始进行划分的所有可能性
    function dfs(i) {
        if (path.length === 3) {
            // 1. 获取最后一段字符串
            const lastSegment = s.slice(i)
            
            // 2. 对最后一段进行合法性校验
            // 长度不能超过3
            if (lastSegment.length > 3) return 
            // 不能有前导零（长度大于1且首位是'0'）
            if (lastSegment.length > 1 && lastSegment[0] === '0') return 
            // 数值不能大于255
            if (Number(lastSegment) > 255) return 
			
            ans.push(`${s.slice(0, path[0])}.${s.slice(path[0], path[1])}.${s.slice(path[1], path[2])}.${s.slice(path[2])}`)
            return
        }
		
        for (const len of [1, 2, 3]) {
            if (i + len > n) break
            if (len > 1 && s[i] === '0') break
            if (Number(s.slice(i, i + len)) > 255) break
			
            const remainingSegments = 3 - path.length;
            const remainingChars = n - (i + len);
            if (remainingChars < remainingSegments || remainingChars > remainingSegments * 3) {
                continue; // 当前长度不合适，尝试下一个长度
            }
            path.push(i + len)
            dfs(i + len)
            path.pop()
			
        }
    }
    dfs(0)
    return ans
}
```

---
## 322 零钱兑换
https://leetcode.cn/problems/coin-change/description/

---
## 104 二叉树的最大深度
https://leetcode.cn/problems/maximum-depth-of-binary-tree/description/

---
## 22 括号生成
https://leetcode.cn/problems/generate-parentheses/description/

---
## LCR 126 斐波那契数列
https://leetcode.cn/problems/fei-bo-na-qi-shu-lie-lcof/description/

```js
function fib(n: number): number {
    const mod = Math.pow(10, 9) + 7
    const map = new Map<number, number>()

    const helper = (n: number): number => {
        if (n === 0) return 0
        if (n === 1) return 1

        if (map.has(n)) return map.get(n)

        // 核心改造：在相加的同时就进行取模，防止中间结果溢出
        const ans = (helper(n - 1) + helper(n - 2)) % mod

        map.set(n, ans)
        return ans
    };

    return helper(n)
}
```

---
## 695 岛屿的最大面积
https://leetcode.cn/problems/max-area-of-island/

```js
function maxAreaOfIsland(grid: number[][]): number {
    const n = grid.length
    const m = grid[0].length

    let ans = 0

    // 这个函数的作用是将包含i, j坐标的岛屿的面积找出来
    const dfs = (i, j) => {
        // 如果是越界或者不是岛屿(海洋、遍历过的岛)
        if (i >= n || i < 0 || j >= m || j < 0 || grid[i][j] !== 1) return 0

        // 标记岛屿
        grid[i][j] = 2

        // 递归调用
        return dfs(i - 1, j) + dfs(i, j - 1) + dfs(i + 1, j) + dfs(i, j + 1) + 1
    }

    for (let i = 0; i < n; i++) {
        for (let j = 0; j < m; j++) {
            ans = Math.max(dfs(i, j), ans)
            console.log(i, j, dfs(i, j),ans)
        }
    }

    console.log(grid)
    return ans
};
```

---
## LCR 140 训练计划 II
#双指针
https://leetcode.cn/problems/lian-biao-zhong-dao-shu-di-kge-jie-dian-lcof/

灵神的脑子怎么这么聪明啊

```js
/**
 * Definition for singly-linked list.
 * class ListNode {
 *     val: number
 *     next: ListNode | null
 *     constructor(val?: number, next?: ListNode | null) {
 *         this.val = (val===undefined ? 0 : val)
 *         this.next = (next===undefined ? null : next)
 *     }
 * }
 */

var trainingPlan = function(head, k) {
    let left = head, right = head;
    while (k--) right = right.next; // 右指针先向右走 k 步
    // 然后左右指针一起走，右指针走到空节点时，左指针正好就在倒数第 k 个节点
    while (right) {
        left = left.next;
        right = right.next;
    }
    return left;
};
```

---
## 94 二叉树的中序遍历
左跟右

---
## 42 接雨水
#双指针 
https://leetcode.cn/problems/trapping-rain-water/description/

使用前缀最大值与后缀最大值来标记：
```js
function trap(height: number[]): number {
    let ans = 0

    const n = height.length
    const preMax = Array(n)  
    const sufMax = Array(n)

    preMax[0] = height[0]
    for (let i = 1; i < n; i++) {
        preMax[i] = Math.max(preMax[i - 1], height[i])
    }

    sufMax[n - 1] = height[n - 1]
    for (let i = n - 2; i >= 0; i--) {
        sufMax[i] = Math.max(sufMax[i + 1], height[i])
    }

    for (let i = 0; i < n; i++) {
        ans += Math.min(preMax[i], sufMax[i]) - height[i]
    }

    console.log(preMax, sufMax)
    return ans
};
```

---
## 1143 最长公共子序列
#动态规划
https://leetcode.cn/problems/longest-common-subsequence/description/

```js
function longestCommonSubsequence(text1: string, text2: string): number {
    let m = text1.length
    let n = text2.length

    // dfs(i, j)表示以text1[i]与text2[j]结尾的两个子串的最长公共子序列
    const memo = new Array(m).fill('').map(i => new Array(n).fill(-1))

    const dfs = (i, j) => {
        if (i < 0 || j < 0) return 0

        if (memo[i][j] !== -1) return memo[i][j]
        if (text1[i] === text2[j]) {
            memo[i][j] = dfs(i - 1, j - 1) + 1
            return memo[i][j]
        }

        memo[i][j] = Math.max(dfs(i - 1, j), dfs(i, j - 1))

        return memo[i][j]
    }

    return dfs(m - 1, n - 1)
};
```

---
## 14 最长公共前缀
---
## 226 翻转二叉树
---
## 1556 千位分割数
---
## 62 不同路径
#动态规划 
https://leetcode.cn/problems/unique-paths/submissions/728284503/

```js
function uniquePaths(m: number, n: number): number {
    const memo = new Array(m).fill('').map(i => new Array(n).fill(-1))
    console.log(memo)
	
    const dfs = (i, j) => {
        console.log(i,j)
        if (i < 0 || j < 0) return 0
        if (i === 0 && j === 0) return 1
        if (memo[i][j] !== -1) return memo[i][j]
		
        let ans = dfs(i - 1, j) + dfs(i, j - 1)
        memo[i][j] = ans
        return ans
    }
    return dfs(m - 1, n - 1)
};
```

---
## 25 K个一组反转链表
这道题我认为在前端就几乎不会考了。。。

---
## 283 移动零
https://leetcode.cn/problems/move-zeroes/description/
简单来讲，就是将非零的元素全部都移动到数组的前面，再根据数组中非零元素的个数与数组的长度，将剩余的零补上就可以了

```js
/**
 * @param {number[]} nums
 * @return {void} Do not return anything, modify nums in-place instead.
 */
var moveZeroes = function (nums) {
    let stackSize = 0
    // 遍历每一个元素，如果非零就直接进入数组（可能会覆盖掉自己）
    // 0的位置不用考虑，等所有的非零元素进入后，再将0填入
    for (const num of nums) {
        if (num !== 0) {
            nums[stackSize] = num
            stackSize++
        }
    }
    nums.fill(0, stackSize)
}
```

---
## 236 二叉树的最近公共祖先
没看懂哈。。。

答案只有两种情况：
- 这两个点是某个节点的子孙。直接返回，因为下面肯定没有，在另一个子树上。
- 这两个点互为爷孙。那么遍历到这两个点就可以直接返回了，应为爷爷就是答案
```js
var lowestCommonAncestor = function(root, p, q) {
    if (root === null || root === p || root === q) {
        return root; // 找到 p 或 q 就不往下递归了，原因见上面答疑
    }
    const left = lowestCommonAncestor(root.left, p, q);
    const right = lowestCommonAncestor(root.right, p, q);
    if (left && right) { // 左右都找到
        return root; // 当前节点是最近公共祖先
    }
    // 如果只有左子树找到，就返回左子树的返回值
    // 如果只有右子树找到，就返回右子树的返回值
    // 如果左右子树都没有找到，就返回 null（注意此时 right = null）
    return left ?? right;
};
```

---
##   103 二叉树的锯齿形层序遍历
https://leetcode.cn/problems/binary-tree-zigzag-level-order-traversal/description/

这道题和深度遍历很像

---
## 199 二叉树的右视图
https://leetcode.cn/problems/binary-tree-right-side-view/description/
套用 102 题的 BFS 模板，把每一层的最后一个节点值保存到答案中。

---
## 2 两数相加
https://leetcode.cn/problems/add-two-numbers/description/

```js
/**
 * @param {ListNode} l1
 * @param {ListNode} l2
 * @return {ListNode}
 */
var addTwoNumbers = function (l1, l2, carry=0) {
    if (l1 === null && l2 === null && carry === 0) {
        return null
    }

    let sum = carry;
    if (l1) {
        sum += l1.val;
        l1=l1.next
    }
    if (l2) {
        sum += l2.val
        l2 = l2.next
    }

    return new ListNode(sum%10,addTwoNumbers(l1,l2,Math.floor(sum/10)))
}
```

---
## 209 长度最小的子数组
https://leetcode.cn/problems/minimum-size-subarray-sum/description/
https://www.bilibili.com/video/BV1tZ4y1q7XE?spm_id_from=333.788.recommend_more_video.1&trackid=web_related_0.router-related-2589621-48s8n.1782031683220.519&vd_source=47c9acd507be61251cd2bb730416395c

这道题的思路是不断的枚举右端点，当和大于目标值的时候，移动左端点，直到小于，然后移动右端点，再左端点：
```js
function minSubArrayLen(target: number, nums: number[]): number {
    const n = nums.length
    let ans = n + 1
    let sum = 0
    let left = 0
    for (let right = 0; right < n; right++) {
        sum += nums[right]
        while(sum >= target){
            sum -= nums[left]
            ans = Math.min(ans, right - left +1)
            left ++
        }
    }

    return ans <= n ? ans : 0
};
```

---
## 125 验证回文串
---
## 394 字符串解码
https://leetcode.cn/problems/decode-string/

有点难度哈。。。

```js
var decodeString = function(s) {
    const stack = []; // 用于模拟计算机的递归
    let res = '';
    let k = 0;
    for (const c of s) {
        if ('a' <= c && c <= 'z') {
            res += c;
        } else if ('0' <= c && c <= '9') {
            k = k * 10 + parseInt(c);
        } else if (c === '[') {
            // 模拟递归
            // 在递归之前，把当前递归函数中的局部变量 res 和 k 保存到栈中
            stack.push([res, k]);
            // 递归，初始化 res 和 k
            res = '';
            k = 0;
        } else { // ']'
            // 递归结束，从栈中恢复递归之前保存的局部变量
            const [pre_res, pre_k] = stack.pop();
            // 此时 res 是下层递归的返回值，将其重复 pre_k 次，拼接到递归前的 pre_res 之后
            res = pre_res + res.repeat(pre_k);
        }
    }
    return res;
};
```

---
## 101 对称二叉树
---
## 155 最小栈
---
## 43 字符串相乘
---
## 198 打家劫舍
https://leetcode.cn/problems/house-robber/description/

```js
var rob = function(nums) {
    const n = nums.length;
    const memo = Array(n).fill(-1); // -1 表示没有计算过

    // dfs(i) 表示从 nums[0] 到 nums[i] 最多能偷多少
    function dfs(i) {
        if (i < 0) { // 递归边界（没有房子）
            return 0;
        }
        if (memo[i] !== -1) { // 之前计算过
            return memo[i];
        }
        const res = Math.max(dfs(i - 1), dfs(i - 2) + nums[i]);
        memo[i] = res; // 记忆化：保存计算结果
        return res;
    }

    return dfs(n - 1); // 从最后一个房子开始思考
};

作者：灵茶山艾府
链接：https://leetcode.cn/problems/house-robber/solutions/2102725/ru-he-xiang-chu-zhuang-tai-ding-yi-he-zh-1wt1/
来源：力扣（LeetCode）
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
```

---
## 160 相交链表
---
## 718 最长重复子数组
![[Pasted image 20260621171215.png]]

```js
var findLength = function(nums1, nums2) {
    const n = nums1.length, m = nums2.length;
    const f = Array.from({ length: n + 1 }, () => Array(m + 1).fill(0));
    let ans = 0;
    for (let i = 0; i < n; i++) {
        for (let j = 0; j < m; j++) {
            if (nums1[i] === nums2[j]) {
                f[i + 1][j + 1] = f[i][j] + 1;
                ans = Math.max(ans, f[i + 1][j + 1]);
            }
        }
    }
    return ans;
};

作者：灵茶山艾府
链接：https://leetcode.cn/problems/maximum-length-of-repeated-subarray/solutions/866328/on-hou-zhui-shu-zu-by-endlesscheng-jwr2/
来源：力扣（LeetCode）
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
```

---
## 122 买股票的最佳时机

> 6/21/2026 
> 已经将CodeTop中频度大于10的全部搞完了，LeedCode100也是，