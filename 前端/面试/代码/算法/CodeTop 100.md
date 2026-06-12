# CodeTop 100
越是靠前，题目的热度越高🔥（筛选条件 岗位：前端）

这里的题目的编号和LeetCode一致，与另一个文档相同的题目只有编号。
据我统计，岗位不限中，前80道题目全部做完，基本上可以覆盖前端常考的题目，前端做前60道就可以了。
# 3 无重复字符的最长子串 ⌚️
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
# 165 比较版本号 ⌚️
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
# 88 合并两个有序数组
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
# 20 有效括号
#栈 #简单
https://leetcode.cn/problems/valid-parentheses/description/
# 415 字符串相加 ⌚️
#双指针 
https://leetcode.cn/problems/add-strings/description/
# 1 两数之和
#哈希表 
https://leetcode.cn/problems/two-sum/description/
# 46 全排列
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
# 206 反转链表
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
# 102 二叉树的层序遍历
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
# 53 最大子数组和
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
# 121 买卖股票的最佳时机
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
# 三数之和
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
# 146 LRU缓存机制
https://leetcode.cn/problems/lru-cache/description/
# 141 环形链表
# 112 路径总和
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
# 21 合并两个有序链表
# 215 数组中的第K大
https://leetcode.cn/problems/kth-largest-element-in-an-array/description/
在数组中，随机的选一个数，以它为准，将小于的放在其左侧，大于的在右侧，如果这个数正好是第k个，那么他就是第k大，如果不是，那就在左右两侧继续找
# 912 快排
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
# 5 最长回文子串 ⌚️
https://leetcode.cn/problems/longest-palindromic-substring/
# 70 爬楼梯
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
# 54 螺旋矩阵
https://leetcode.cn/problems/spiral-matrix/description/






# 56 区间合并 ⌚️
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
我还做过呢，艹了。这肯定是没了啊，这题都没搞出来，你。。。