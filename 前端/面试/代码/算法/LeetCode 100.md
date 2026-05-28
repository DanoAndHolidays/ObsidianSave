# 1两数之和算法实现
[修正术语]：给定数组 `nums` 和目标值 `target`，找出数组中两数之和等于目标值的下标。
```javascript
/**
 * 暴力解法 - 时间复杂度 O(n²)
 * @param {number[]} nums - 输入数组
 * @param {number} target - 目标值
 * @returns {number[]} 满足条件的下标数组
 */
const twoSum = function(nums, target) {
    for (let i = 0; i < nums.length; i++) {
        for (let j = i + 1; j < nums.length; j++) {
            if (nums[i] + nums[j] === target) {
                return [i, j];
            }
        }
    }
    return [];
};
```
hash表：
```javascript
/**
 * 哈希表解法 - 时间复杂度 O(n)
 * @param {number[]} nums - 输入数组
 * @param {number} target - 目标值
 * @returns {number[]} 满足条件的下标数组
 */
const twoSum = function(nums, target) {
    const map = new Map(); // 存储值到下标的映射
    
    for (let i = 0; i < nums.length; i++) {
        const complement = target - nums[i];
        
        // 检查补数是否存在于哈希表中
        if (map.has(complement)) {
            return [map.get(complement), i];
        }
        
        // 将当前值存入哈希表
        map.set(nums[i], i);
    }
    
    return [];
};
```
# 2两数相加
---
```javascript
// Definition for singly-linked list.
function ListNode(val, next) {
    this.val = val === undefined ? 0 : val
    this.next = next === undefined ? null : next
}

/** 使用递归的方式实现
 * @param {ListNode} l1
 * @param {ListNode} l2
 * @return {ListNode}
 */
var addTwoNumbers = function (l1, l2, carry = 0) {
    // 默认值为0，没有默认值递归会出现问题
    if (l1 === null && l2 === null && carry === 0) {
        return null
        // 递归的边界条件
    }

    let sum = carry
    // 求和

    if (l1) {
        sum += l1.val
        l1 = l1.next
    }
    if (l2) {
        sum += l2.val
        l2 = l2.next
    }

    return 
    new ListNode(sum % 10, addTwoNumbers(l1, l2, Math.floor(sum / 10)))
    // Math.floor向下取整
}
```

# 49字母异位词分组
**示例 1:**

**输入:** strs = ["eat", "tea", "tan", "ate", "nat", "bat"]

**输出:** [["bat"],["nat","tan"],["ate","eat","tea"]]

**解释：**

- 在 strs 中没有字符串可以通过重新排列来形成 `"bat"`。
- 字符串 `"nat"` 和 `"tan"` 是字母异位词，因为它们可以重新排列以形成彼此。
- 字符串 `"ate"` ，`"eat"` 和 `"tea"` 是字母异位词，因为它们可以重新排列以形成彼此。
---
```javascript
/**
 * @param {string[]} strs
 * @return {string[][]}
 */
var groupAnagrams = function (strs) {
    const hashMap = new Map()
    //遍历字符串数组以其中每项排序后的字符串为键，字符串加入数组作为值
    for (const item of strs) {
        const resort = item.split('').sort().join('')
        if (!hashMap.has(resort)) {
            hashMap.set(resort, [])
        }

        hashMap.get(resort).push(item)
    }
    return Array.from(hashMap.values())
}
```

# 128最长连续序列
给定一个未排序的整数数组 `nums` ，找出数字连续的最长序列（不要求序列元素在原数组中连续）的长度。

请你设计并实现时间复杂度为 `O(n)` 的算法解决此问题。
**示例 1：**
输入：nums = [100,4,200,1,3,2]
输出：4

---
```javascript
const arr = [100, 4, 200, 1, 3, 2]

/**
 * @param {number[]} nums
 * @return {number}
 */
var longestConsecutive = function (nums) {
    const set = new Set(nums)
    let result = 0
    for (const item of set) {
        // 如果当前的数的前面还有比它小一个的数字
        // 那么他一定不是最长的
        if (set.has(item - 1)) {
            continue
        }
        let start = item + 1
        while (set.has(start)) {
            start++
        }

        result = Math.max(result, start - item)

        // 如果发现一条链的长度大于了数组长度的一般
        // 那么就不可有比它还大的链了，直接返回结果
        if (result >= nums.length) {
            break
        }
    }
    return result
}

console.log(longestConsecutive(arr))
// 4
```

# 283移动零
---
#栈 #双指针
```javascript
const nums = [0, 1, 0, 3, 12]

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

moveZeroes(nums)
console.log(nums)
// [ 1, 3, 12, 0, 0 ]

```
# 11盛水最多的容器
---
#双指针
暴力循环就不解释了，灵神确实NB
```javascript
height = [1, 8, 6, 2, 5, 4, 8, 3, 7]

/**
 * @param {number[]} height
 * @return {number}
 */
var maxArea = function (height) {
    let result = 0
    let lift = 0
    let right = height.length - 1
    // 这里要要减一，不然就越界
    while (lift < right) {
        let area = (right - lift) * Math.min(height[right], height[lift])
        result = Math.max(result, area)
        if (height[right] < height[lift]) {
            right--
        } else {
            lift++
        }
    }
    return result
}

console.log(maxArea(height))
// 49
```
# 15三数之和
---
#双指针 
```javascript
nums = [-1, 0, 1, 2, -1, -4, -2, -3, 3, 0, 4]

var threeSum = function (nums) {
    let result = []
    const twoSum = function (nums, target) {
        const map = new Map() // 存储值到下标的映射

        for (let i = 0; i < nums.length; i++) {
            const complement = target - nums[i]

            // 检查补数是否存在于哈希表中
            if (map.has(complement)) {
                return [nums[map.get(complement)], nums[i]]
            }

            // 将当前值存入哈希表
            map.set(nums[i], i)
        }

        return []
    }

    for (let index = 0; index < nums.length; index++) {
        let fixedSum = 0 - nums[index]
        // console.log(nums[index], 'fixedSum', fixedSum)

        let fixedArr = Array.from(nums)
        fixedArr.splice(index, 1)
        // console.log(fixedArr, nums)

        let res = twoSum(fixedArr, fixedSum)

        if (res.length !== 0) {
            // console.log('res:',res);

            res.push(nums[index])
            res.sort()

            result.push(res)
        }
    }
    const seen = new Set()

    return result.filter((item) => {
        const str = JSON.stringify(item)

        if (seen.has(str)) {
            return false
        }
        seen.add(str)
        return true
    })
}

console.log(threeSum(nums))
// [[-1, 0, 1], [-1, -1, 2], [-4, 1, 3], [-2, 0, 2], [-3, 1, 2], [-4, 0, 4]]
// 如果只有一种可能得情况下是完全没问题的，但是[-3, -1, 4]没有，因为在选中-3的情况下
// 只在剩余的数组中找到了最先出现的一对，但其实后面还有
```

```javascript
nums = [0, 0, 0, 0, 0, 0, 0]
/** 灵神无敌好吧
 * @param {number[]} nums
 * @return {number[][]}
 */
var threeSum = function (nums) {
    nums.sort((a, b) => a - b)
    let result = []
    // console.log(nums);
    for (let i = 0; i < nums.length - 2; i++) {
        let j = i + 1
        let k = nums.length - 1
        if (i > 0 && nums[i] === nums[i - 1]) continue

        // 第一处优化，如果枚举的数字与剩下的最近两个就已经大于零了
        // 后面不可能比这种情况更小直接break
        if (nums[i] + nums[i + 1] + nums[i + 2] > 0) break
        // 第二处
        if (nums[i] + nums[nums.length - 1] + nums[nums.length - 2] < 0)
            continue
        while (j < k) {
            if (nums[i] + nums[j] + nums[k] > 0) {
                k--
            } else if (nums[i] + nums[j] + nums[k] < 0) {
                j++
            } else {
                result.push([nums[i], nums[j], nums[k]])
                for (j++; j < k && nums[j] === nums[j - 1]; j++) {}
                for (k--; j < k && nums[k] === nums[k + 1]; k--) {}
            }
        }
    }
    return result
}

console.log(threeSum(nums))
```
# 42接雨水
---
#双指针 
```javascript
height = [0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]

/**
 * @param {number[]} height
 * @return {number}
 */
var trap = function (height) {
    let arrSum = height.reduce((acc, curr) => acc + curr)

    let lift = 0,
        right = height.length-1

    while (lift < right) {
        let min = Math.min(height[lift], height[right])
        // console.log(min);
        console.log(lift,right,height[lift], height[right],min)
        
        for (let i = lift; i < right; i++) {
            if (height[i] < min) {
                height[i] = min
            }
        }

        if (height[lift] < height[right]) {
            lift++
        } else {
            right--
        }
    }
    console.log(height)

    let sum = height.reduce((acc, curr) => acc + curr)
    return sum - arrSum
}

console.log(trap(height))
// 6
```
![[Pasted image 20250912223122.png]]
我好不容易自己想出来的一个算法，结果倒在了最后一个测试用例上，这诗人啊？

😅
这个算法的问题在于重复的填入，那么我用求出“极大值”将极大值之间填满，就能极大的缩短填充的时间，可能就过了...

不对，这思路不对

[idea]([盛最多水的容器 接雨水【基础算法精讲 02】_哔哩哔哩_bilibili](https://www.bilibili.com/video/BV1Qg411q7ia/?vd_source=47c9acd507be61251cd2bb730416395c))
```javascript
height = [0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]
/**
 * @param {number[]} height
 * @return {number}
 */
var trap = function (height) {
    let arrSum = height.reduce((acc, curr) => acc + curr)

    let lift = 0
    let right = height.length - 1

    let liftMax = height[lift]
    let rightMax = height[right]

    while (lift < right) {
        liftMax = Math.max(liftMax, height[lift])
        rightMax = Math.max(rightMax, height[right])

        if (liftMax < rightMax) {
            height[lift] = liftMax
            console.log(`将左侧index=${lift}的${height[lift]}设置为${liftMax}`)
            lift++
        } else {
            console.log(`将右侧index=${right}的${height[right]}设置为${rightMax}`)
            height[right] = rightMax
            right--
        }
    }
    console.log(height)

    let sum = height.reduce((acc, curr) => acc + curr)
    console.log(sum)

    return sum - arrSum
}

console.log(trap(height))
// 6
```
![[Pasted image 20250912231932.png]]
不是哥们，这前面的也太猛了吧

# 3 字符的最长无重复子串 ⌚️
---
#双指针 #第一道自己做出来的  到目前为止的==第一道自己写出来的==Hot100，我这个是直接暴力去移动的，只移动一个
```javascript
s = 'afddd'

/**
 * @param {string} s
 * @return {number}
 */
var lengthOfLongestSubstring = function (s) {
    let lift = 0
    let right = lift

    let result = 0
    const seen = new Set()

    while (right < s.length) {
        if (seen.has(s[right])) {
            result = Math.max(result, right - lift)
            lift++
            right=lift
            seen.clear()
        } else {
            seen.add(s[right])
            right++
        }
    }
    result = Math.max(result, right - lift)
    return result
}

console.log(lengthOfLongestSubstring(s))
// 3
```

这是优化的做法：
abcabcbb
abca
bca
bcab
cab
cabc
abc
abcb
bcb
cb
cbb
bb
b

这个东西的思路就是，我右边的指针会右移，右指针指着的符号一旦出现在窗口中有多个，那就需要将左边的向右移动，直到右指针指着的字符不再重复。
```js
var lengthOfLongestSubstring = function(s) {
    let ans = 0;
    let left = 0;
    // 以字符为键，值为其数量
    const cnt = new Map(); 
    // 维护从下标 left 到下标 right 的字符
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
# 438找到字符串中所有字母异位词
---
```javascript
s = 'beeaaedcbc'
p = 'ee'

/**
 * @param {string} s
 * @param {string} p
 * @return {number[]}
 */
var findAnagrams = function (s, p) {
    let result = []

    if (!s.includes(p)) {
        return result
    }

    let hash = new Set()
    let sublength = p.length
    let fixedSub = p.split('').sort().join('')
    // console.log(fixedSub)

    hash.add(fixedSub)

    for (let index = 0; index < s.length - sublength + 1; index++) {
        let res = s.slice(index, sublength + index)
        // console.log(s, '->', res)
        let fixedRes = res.split('').sort().join('')

        if (hash.has(fixedRes)) {
            result.push(index)
        }
    }

    return result
}

console.log(findAnagrams(s, p))
// [ 1 ]
```
![[Pasted image 20250913150922.png]]
这玩应有9.8kb大

```javascript
s = 'afdsa'
p = 'a'

var findAnagrams = function (s, p) {
    const ans = []
    const cntP = new Array(26).fill(0) // 统计 p 的每种字母的出现次数
    const cntS = new Array(26).fill(0) // 统计 s 的长为 len(p) 的子串 s' 的每种字母的出现次数

    for (const item of p) {
        cntP[item.charCodeAt() - 'a'.charCodeAt()]++
        // console.log(item.charCodeAt())
    }
console.log(cntP);

    for (let right = 0; right < s.length; right++) {
        cntS[s[right].charCodeAt() - 'a'.charCodeAt()]++
        let left = right - p.length + 1

        if (left < 0) {
            continue
        }

        if (JSON.stringify(cntP) === JSON.stringify(cntS)) {
            ans.push(left)
        }
        cntS[s[left].charCodeAt() - 'a'.charCodeAt()]--
    }

    return ans
}

console.log(findAnagrams(s, p))
// [(0, 4)]

```

# 560和为k的子数组
---
#前缀 #中等 这哪里是中等，相当困难的了

如果全是着正数就可以💧，没考虑负数的情况
```javascript
/**
 * @param {number[]} nums
 * @param {number} k
 * @return {number}
 */
var subarraySum = function (nums, k) {
    let result = 0
    const leftSum = []
    let sum = 0
    for (let index = 0; index < nums.length; index++) {
        sum += nums[index]

        leftSum[index] = sum
    }
    console.log(leftSum)

    let left = 0
    let right = 0

    while (right<nums.length) {
        if (leftSum[right] - leftSum[left]+nums[left] < k) {
            console.log(
                `当前小于k，右侧为${right}，左侧${left}，值${
                    leftSum[right] - leftSum[left]+nums[left]
                }`
            )

            right++
        } else if (leftSum[right] - leftSum[left]+nums[left] > k) {
            console.log(
                `当前大于k，右侧为${right}，左侧${left}，值${
                    leftSum[right] - leftSum[left]+nums[left]
                }`
            )
            left++
        } else if ((leftSum[right] - leftSum[left] + nums[left]) == k) {
            console.log(
                `当前等于k，右侧为${right}，左侧${left}，值${
                    leftSum[right] - leftSum[left] + nums[left]
                }`
            )
            result++
            right++
        } else {
            right++
        }
    }

    return result
}
```

暴力循环居然能过
![[Pasted image 20250913170011.png]]
``` javascript
nums = [-1, -1, 1]
k = 0

/**
 * @param {number[]} nums
 * @param {number} k
 * @return {number}
 */
var subarraySum = function (nums, k) {
    let result = 0
    const leftSum = []
    let sum = 0
    for (let index = 0; index < nums.length; index++) {
        sum += nums[index]

        leftSum[index] = sum
    }
    console.log(leftSum)

    for (let left = 0; left < nums.length; left++) {
        for (let right = left; right < nums.length; right++){
            if (leftSum[right] - leftSum[left] + nums[left] == k) {
                result++
            }
        }
    }

    return result
}

console.log(subarraySum(nums, k))
```

```javascript
nums = [1, -1, 0]
k = 0

/**
 * @param {number[]} nums
 * @param {number} k
 * @return {number}
 */
var subarraySum = function (nums, k) {
    const n = nums.length
    const s = Array(n + 1).fill(0)

    // 前缀的第一项一定是0，n长的数组的前缀有n+1项
    for (let i = 0; i < n; i++) {
        s[i + 1] = s[i] + nums[i]
    }
    console.log(s)
    // [ 0, 1, 3, 6 ]

    let ans = 0
    const cnt = new Map()
    for (const sj of s) {
        // ??空值合并 如果第一个参数不是null/undefined，则??返回第一个参数。否则，返回第二个参数。
        // ???这里是什么万银
        ans += cnt.get(sj - k) ?? 0

        console.log(`${sj}-${k}，在`)
        console.log(cnt)
        console.log(`中寻找s[i]=${sj - k},${cnt.get(sj - k) ?? '没有'}`)

        // 这里使用Set实现不是更好吗，这样的写法我感觉有点迷惑
        // 这里+1是干嘛？加一就是将前方出现的次数记录下来了
        cnt.set(sj, (cnt.get(sj) ?? 0) + 1)
        console.log(`将${sj}加入`)
    }
    console.log(cnt)

    return ans
}

console.log(subarraySum(nums, k))
```
害得是我的灵神

# 239滑动窗口最大值
---
#滑动窗口
```javascript
nums = [1, 3, 1, 2, 0, 5]
k = 3

var maxSlidingWindow = function (nums, k) {
    const result = []
    const queue = [] // 存储索引
    for (let right = 0; right < nums.length; right++) {
        // 维护队列递减性：弹出所有小于当前元素的队列尾索引
        while (
            queue.length > 0 &&
            nums[right] >= nums[queue[queue.length - 1]]
        ) {
            queue.pop()
        }
        queue.push(right)

        // 检查队列头索引是否超出窗口左边界
        if (queue[0] <= right - k) {
            queue.shift()
        }

        // 当窗口大小达到k时，记录最大值
        if (right >= k - 1) {
            result.push(nums[queue[0]])
        }
    }
    return result
}

console.log('result:', maxSlidingWindow(nums, k))
```
简单来说就是维护一个递减的窗口，不满足递减的时候就清空，这样最左侧始终就是最大值
![[Pasted image 20250914211618.png]]
# 76最小覆盖子串
---
#滑动窗口 
```javascript
s = 'ADOBECODEBANC'
t = 'ABC'

function isCovered(cntS, cntT) {
    for (let i = 'A'.charCodeAt(0); i <= 'Z'.charCodeAt(0); i++) {
        if (cntS[i] < cntT[i]) {
            return false
        }
    }
    for (let i = 'a'.charCodeAt(0); i <= 'z'.charCodeAt(0); i++) {
        if (cntS[i] < cntT[i]) {
            return false
        }
    }
    return true
}

var minWindow = function (s, t) {
    const cntS = Array(128).fill(0) // s 子串字母的出现次数
    const cntT = Array(128).fill(0) // t 中字母的出现次数
    for (const c of t) {
        cntT[c.codePointAt(0)]++
    }

    let ansLeft = -1
    let ansRight = s.length
    let left = 0
    for (let right = 0; right < s.length; right++) {
        // 移动子串右端点
        cntS[s[right].codePointAt(0)]++ // 右端点字母移入子串
        while (isCovered(cntS, cntT)) {
            // 涵盖
            if (right - left < ansRight - ansLeft) {
                // 找到更短的子串
                ansLeft = left // 记录此时的左右端点
                ansRight = right
            }
            cntS[s[left].codePointAt(0)]-- // 左端点字母移出子串
            left++
        }
    }
    return ansLeft < 0 ? '' : s.substring(ansLeft, ansRight + 1)
}

console.log('result:', minWindow(s, t))
```

# 53最大子数组和
---
#前缀 #贪心
思路就是维护一个最小的前缀和，用当前的前缀和减去，取最小值为结果返回
```javascript
let nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]

let nums2 = [-1, 0, -2]
/**
 * @param {number[]} nums
 * @return {number}
 */
var maxSubArray = function (nums) {
    let minSum = 0
    let curSum = 0
    let result = []

    for (let index = 0; index < nums.length; index++) {
        minSum = Math.min(minSum, curSum)

        curSum += nums[index]

        result.push(curSum - minSum)

        console.log(`前缀和:${curSum}最小和:${minSum}值:${result}`)
    }

    return Math.max(...result)
}
console.log('result:', maxSubArray(nums2))
```

# 48旋转图像
---
#矩阵
旋转一个矩阵：先转置（交换主对角线的元素），再行翻转
也有规律，就是列变行，行与矩阵的length的差作为新的列，其实就是==先转置、再行翻转==
```javascript
let matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9],
]
/**
 * @param {number[][]} matrix
 * @return {void} Do not return anything, modify nums in-place instead.
 */
const rotate = function (matrix) {
    for (let i = 0; i < matrix.length; i++) {
        for (let j = 0; j < i; j++) {
            const tmp = matrix[i][j]
            matrix[i][j] = matrix[j][i]
            matrix[j][i] = tmp
        }
    }

    for (const element of matrix) {
        element.reverse()
    }
}

rotate(matrix)
console.log('result:', matrix)
// result: [ [ 7, 4, 1 ], [ 8, 5, 2 ], [ 9, 6, 3 ] ]
```

# 54螺旋矩阵
---
#矩阵
```javascript
let matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9],
]
/**
 * @param {number[][]} matrix
 * @return {void} Do not return anything, modify nums in-place instead.
 */
const rotate = function (matrix) {
    const DIRS = [
        [0, 1],
        [1, 0],
        [0, -1],
        [-1, 0],
    ]
    const m = matrix.length
    const n = matrix[0].length
    const result = Array(m * n)

    let i = 0,
        j = 0,
        di = 0

    for (let k = 0; k < m * n; k++) {
        result[k] = matrix[i][j]
        matrix[i][j] = Infinity

        // 判断下一个位置，越界就换方向
        const i_next = i + DIRS[di][0]
        const j_next = j + DIRS[di][1]
        if (
            i_next < 0 ||
            i_next >= m ||
            j_next < 0 ||
            j_next >= n ||
            matrix[i_next][j_next] === Infinity
        ) {
            di = (di + 1) % 4
        }

        i += DIRS[di][0]
        j += DIRS[di][1]
    }

    return result
}

console.log('result:', rotate(matrix))
// result: [ [ 7, 4, 1 ], [ 8, 5, 2 ], [ 9, 6, 3 ] ]
```

# 41寻找缺失的第一个正数
---
这是我的思路：遍历数组，寻找到最大最小值，并且将数组存入hash表，再从1-max中遍历，如果hash表中么有，就返回这个缺失值，都有就返回max+1
```javascript
let nums = [7, 8, 9, 11, 12]
/**
 * @param {number[]} nums
 * @return {number}
 */
var firstMissingPositive = function (nums) {
    let min = 0
    let max = 0
    const set = new Set()

    for (item of nums) {
        min = Math.min(min, item)
        max = Math.max(max, item)
        set.add(item)
    }
    console.log(min, max, set)

    for (let i = 1; i < max + 1; i++){
        if (!set.has(i)) {
            return i
        }
    }

    return max+1
}

console.log('result:', firstMissingPositive(nums))
// result: 1
```
![[Pasted image 20250917171136.png]]
过了！
```javascript
var firstMissingPositive = function(nums) {
    const n = nums.length;
    for (let i = 0; i < n; i++) {
        // 如果当前学生的学号在 [1,n] 中，但（真身）没有坐在正确的座位上
        while (1 <= nums[i] && nums[i] <= n && nums[i] !== nums[nums[i] - 1]) {
            // 那么就交换 nums[i] 和 nums[j]，其中 j 是 i 的学号
            const j = nums[i] - 1; // 减一是因为数组下标从 0 开始
            [nums[i], nums[j]] = [nums[j], nums[i]];
        }
    }

    // 找第一个学号与座位编号不匹配的学生
    for (let i = 0; i < n; i++) {
        if (nums[i] !== i + 1) {
            return i + 1;
        }
    }

    // 所有学生都坐在正确的座位上
    return n + 1;
};
```

# 240 搜索二维矩阵
---
```javascript
var searchMatrix = function(matrix, target) {
    const m = matrix.length, n = matrix[0].length;
    let i = 0, j = n - 1; // 从右上角开始
    while (i < m && j >= 0) { // 还有剩余元素
        if (matrix[i][j] === target) {
            return true; // 找到 target
        }
        if (matrix[i][j] < target) {
            i++; // 这一行剩余元素全部小于 target，排除
        } else {
            j--; // 这一列剩余元素全部大于 target，排除
        }
    }
    return false;
};
```
![[Pasted image 20250918194616.png]]
# 206 翻转链表
---
#链表
这道题有点烦，因为js没有指针这种说法，实现起来也有点奇怪
```javascript
let head = [1, 2, 3, 4, 5]

function ListNode(val, next) {
    this.val = val === undefined ? 0 : val
    this.next = next === undefined ? null : next
}
/**
 * @param {ListNode} head
 * @return {ListNode}
 */
var reverseList = function (head) {
    let pre = null,
        cur = head
    while (cur) {
        const nxt = cur.next
        cur.next = pre // 把 cur 插在 pre 链表的前面（头插法）
        pre = cur // 将头转换为刚插入的结点
        cur = nxt
    }
    return pre
}

console.log('result:', reverseList(head))
```


# 70 爬楼梯
---
#动态规划
```js
/**
 * @param {number} n
 * @return {number}
 */

// 使用额外的空间来减少同样的计算
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

console.log(climbStairs(10))
// has 3
// has 5
// has 8
// has 13
// has 21
// has
```

# 118 杨辉三角
---
这个使用通项公式的思路的问题就是：在计算阶乘时，即使使用了缓存，对于较大的n（比如30），阶乘值已经非常大，Number超出了安全整数范围，所以会出现精度丢失（如：377.99999999999994。
```js
// 阶乘函数
const map1 = new Map()
function factorial(n) {
    if (n < 0) return NaN
    if (n === 0 || n === 1) return 1

    if (map1.has(n)) {
        return map1.get(n)
    } else {
        let result = 1
        for (let i = 2; i <= n; i++) {
            result *= i
        }
        map1.set(n.result)
        return result
    }
}

// 杨辉三角通项公式
function yanghuiTerm(n, k) {
    return factorial(n) / (factorial(k) * factorial(n - k))
}

// 生成杨辉三角的某一行
function generateYanghuiRow(rowIndex) {
    const row = []
    for (let k = 0; k <= rowIndex; k++) {
        row.push(yanghuiTerm(rowIndex, k))
    }
    return row
}

var generate = function (numRows) {
    const result = []
    for (let index = 0; index < numRows; index++) {
        result.push(generateYanghuiRow(index))
    }
    return result
}

console.log(generate(23))
// [ [ 1 ], [ 1, 1 ], [ 1, 2, 1 ], [ 1, 3, 3, 1 ], [ 1, 4, 6, 4, 1 ] ]
```

灵神的这个思路我最开始也是这样想的，但感觉通项会快
```js
var generate = function(numRows) {
    const c = Array(numRows);
    for (let i = 0; i < numRows; i++) {
        c[i] = Array(i + 1);
        c[i][0] = c[i][i] = 1;
        for (let j = 1; j < i; j++) {
            // 左上方的数 + 正上方的数
            c[i][j] = c[i - 1][j - 1] + c[i - 1][j];
        }
    }
    return c;
};

```

# 198 打家劫舍
---
#动态规划
从问题规模最小的时候考虑，一般是最后一个或开始的时候。如果做后一个n没有偷，那么n-
就要偷了，n偷了，n-2就偷`dfs(i) = Math.max(dfs(i - 1), dfs(i - 2) + nums[i])`
```js
 /**
 * @param {number[]} nums
 * @return {number}
 */

var rob = function (nums) {
    const len = nums.length
    
	// 使用缓存减少重复的计算
    const map = new Map()

    function dfs(i) {
        if (i < 0) {
            return 0
        }
        if (map.has(i)) {
            return map.get(i)
        } else {
            const t = Math.max(dfs(i - 1), dfs(i - 2) + nums[i])
            map.set(i, t)
            return t
        }
    }
    return dfs(len - 1)
}
```
# 146LRU 缓存
请你设计并实现一个满足  [LRU (最近最少使用) 缓存](https://baike.baidu.com/item/LRU) 约束的数据结构。

实现 `LRUCache` 类：
- `LRUCache(int capacity)` 以 **正整数** 作为容量 `capacity` 初始化 LRU 缓存
- `int get(int key)` 如果关键字 `key` 存在于缓存中，则返回关键字的值，否则返回 `-1` 。
- `void put(int key, int value)` 如果关键字 `key` 已经存在，则变更其数据值 `value` ；如果不存在，则向缓存中插入该组 `key-value` 。如果插入操作导致关键字数量超过 `capacity` ，则应该 **逐出** 最久未使用的关键字。

函数 `get` 和 `put` 必须以 `O(1)` 的平均时间复杂度运行。

这道题的思路就是维护一个有先后顺序的哈希表，JS中的Map就有这种特性，用来实现这个简直在合适不过：
```js
class LRUCatch {
    constructor(capacity, map = new Map()) {
        this.capacity = capacity
        this.map = map
    }

    get(key) {
        if (this.map.has(key)) {
            let tempValue = this.map.get(key)
            this.map.delete(key)
            this.map.set(key, tempValue)
            return tempValue
        }
        return undefined
    }

    set(key, value) {
        if (this.map.has(key)) {
            this.map.delete(key)
        } else if (this.map.size >= this.capacity) {
            this.map.delete(this.map.keys().next().value)
        }
        this.map.set(key, value)
    }
}
```
# 142环形链表 II
给定一个链表的头节点  `head` ，返回链表开始入环的第一个节点。 _如果链表无环，则返回 `null`。_

如果链表中有某个节点，可以通过连续跟踪 `next` 指针再次到达，则链表中存在环。 为了表示给定链表中的环，评测系统内部使用整数 `pos` 来表示链表尾连接到链表中的位置（**索引从 0 开始**）。如果 `pos` 是 `-1`，则在该链表中没有环。**注意：`pos` 不作为参数进行传递**，仅仅是为了标识链表的实际情况。

**不允许修改** 链表。

这道题我的思路是用哈希表将遍历过的节点存起来，next的时候检查是否有。但是这不能以O(1)的空间复杂度完成。pos只会有一个，我先遍历得到链表的长度，得不到啊。。。

这道题要使用双指针，一个快一个慢，详细的解析见[把环形链表讲清楚！ 如何判断环形链表？如何找到环形链表的入口？ LeetCode：142.环形链表II_哔哩哔哩_bilibili](https://www.bilibili.com/video/BV1if4y1d7ob/?spm_id_from=333.337.search-card.all.click&vd_source=47c9acd507be61251cd2bb730416395c)

核心的结论就是快慢指针相遇的点距离环的入口的距离和头距离环入口的距离是一样的
```js
var detectCycle = function (head) {
    if (!head) return null

    let slow = head,
        fast = head

    while (fast && fast.next) {
        slow = slow.next
        fast = fast.next.next

        if (slow === fast) break
    }

    if (!fast || !fast.next) return null

    let slow2 = head
    while (slow2 !== slow) {
        slow = slow.next
        slow2 = slow2.next
    }
    return slow
}
```
# 21 合并两个有序链表
将两个升序链表合并为一个新的 **升序** 链表并返回。新链表是通过拼接给定的两个链表的所有节点组成的。

使用两个指针，分别指向两个链表的头，将两个指针中较小的值插入新的链表中，这个较小的指针向后移动一个。

当一个指针为null时，将另一个指针的剩余结点全部插入新的链表

如果两个链表是null，直接返回
```js
/**
 * Definition for singly-linked list.
 * function ListNode(val, next) {
 *     this.val = (val===undefined ? 0 : val)
 *     this.next = (next===undefined ? null : next)
 * }
 */
/**
 * @param {ListNode} list1
 * @param {ListNode} list2
 * @return {ListNode}
 */
var mergeTwoLists = function (list1, list2) {
    if (!list1 && !list2) return null

    let p1 = list1
    let p2 = list2
    let res = []

    while (p1 && p2) {
        if (p1.val >= p2.val) {
            res.push(p2.val)
            p2 = p2.next
        } else {
            res.push(p1.val)
            p1 = p1.next
        }
    }

    // 将非空的指针的剩余部分接上
    let p3 = p1 || p2

    while (p3) {
        res.push(p3.val)
        p3 = p3.next
    }

    return res
}
```
数据结构不对，返回的数组，不管了

```js
function mergeTwoLists(list1, list2) {
    const dummy = new ListNode(); // 用哨兵节点简化代码逻辑
    let cur = dummy; // cur 指向新链表的末尾
    while (list1 && list2) {
        if (list1.val < list2.val) {
            cur.next = list1; // 把 list1 加到新链表中
            list1 = list1.next;
        } else { // 注：相等的情况加哪个节点都是可以的
            cur.next = list2; // 把 list2 加到新链表中
            list2 = list2.next;
        }
        cur = cur.next;
    }
    cur.next = list1 ?? list2; // 拼接剩余链表
    return dummy.next;
}
```
# 19 删除链表的倒数第N个节点
给你一个链表，删除链表的倒数第 `n` 个结点，并且返回链表的头结点。

使用双指针，第一个next了n+1个节点后，第二个出发，当第一个的next为null的时候，第二个为倒数第n个节点的前一个节点，将这个节点的next设置为next的next就行了。

返回最开始的链表就可了
```js
/**
 * @param {ListNode} head
 * @param {number} n
 * @return {ListNode}
 */
var removeNthFromEnd = function (head, n) {
    let p1 = head
    let p2 = head

    for (let i = 0; i < n; i++) {
        p1 = p1.next
    }

    // 特殊的，在这种情况下，需要移除的就是第一个节点，直接返回head.next就可以了
    if (p1 === null) {
        return p2.next
    }

    while (p1.next) {
        p1 = p1.next
        p2 = p2.next
    }

    p2.next = p2.next.next

    return head
}
```
# 24 两两交换链表中的节点
两两交换其中相邻的节点，并返回交换后链表的头节点。你必须在不修改节点内部的值的情况下完成本题（即，只能进行节点交换）。写的意义不明，能过就行了。
```js
/**
 * @param {ListNode} head
 * @return {ListNode}
 */
var swapPairs = function (head) {
    if (head === null || head.next === null) {
        return head
    }

    let p0 = new ListNode(0, head)
    p0.next = head
    let p1 = head
    let p2 = p1.next

    let newHead = head
    let haveSwapped = false
    let tempHead = head.next

    while (p1 && p1.next) {
        p0.next = p2
        p1.next = p2.next
        p2.next = p1

        if (!haveSwapped) {
            newHead = tempHead
        }

        if (p1.next && p2.next.next.next) {
            p0 = p0.next.next
            p1 = p1.next
            p2 = p2.next.next.next
        } else {
            break
        }
    }

    return newHead
}
```
# 25 K个一组翻转链表
给你链表的头节点 `head` ，每 `k` 个节点一组进行翻转，请你返回修改后的链表。

`k` 是一个正整数，它的值小于或等于链表的长度。如果节点总数不是 `k` 的整数倍，那么请将最后剩余的节点保持原有顺序。

你不能只是单纯的改变节点内部的值，而是需要实际进行节点交换。

这个实现的问题是当k=2的时候，会丢数字，这是由于我使用的算法不能再n<=2的时候正确的处理这三个指针之间的关系，所以我直接用了24题的实现，哈哈哈
```js
/**
 * @param {ListNode} head
 * @param {number} k
 * @return {ListNode}
 */
const swap666 = (start, k) => {
    if (!start.next || !start || k === 1) return 0

    let end = start
    let nextStart = start.next

    for (let i = 0; i < k - 1; i++) {
        if (!end.next) return 0
        end = end.next
    }

    for (let i = 0; i < k - 1; i++) {
        start.next = end.next
        end.next = start
        start = nextStart
        nextStart = nextStart.next
    }
    return end
}

/**
 * @param {ListNode} head
 * @return {ListNode}
 */
var swapPairs = function (head) {
    if (head === null || head.next === null) {
        return head
    }

    let p0 = new ListNode(0, head)
    p0.next = head
    let p1 = head
    let p2 = p1.next

    let newHead = head
    let haveSwapped = false
    let tempHead = head.next

    while (p1 && p1.next) {
        p0.next = p2
        p1.next = p2.next
        p2.next = p1

        if (!haveSwapped) {
            newHead = tempHead
        }

        if (p1.next && p2.next.next.next) {
            p0 = p0.next.next
            p1 = p1.next
            p2 = p2.next.next.next
        } else {
            break
        }
    }

    return newHead
}

var reverseKGroup = function (head, k) {
    if (k === 1) return head
    if (k === 2) {
        return swapPairs(head)
    }
    let pre = new ListNode(0, head)
    let start = head

    while (1) {
        let end = swap666(start, k)
        if (pre.next === head) {
            pre.next = end
        }
        for (let i = 0; i < k - 1; i++) {
            if (start.next === null) return pre.next
            start = start.next
        }
    }

    return pre.next
}
```

```js
var reverseKGroup = function(head, k) {
    let n = 0;
    for (let cur = head; cur; cur = cur.next) {
        n++;
    }

    const dummy = new ListNode(0, head);
    let p0 = dummy;
    let pre = null;
    let cur = head;

    // k 个一组处理
    for (; n >= k; n -= k) {
        for (let i = 0; i < k; i++) {
            const nxt = cur.next;
            cur.next = pre;
            pre = cur;
            cur = nxt;
        }
        
        const nxt = p0.next;
        p0.next.next = cur;
        p0.next = pre;
        p0 = nxt;
    }
    return dummy.next;
};
```
# 148 链表排序
```js
function getMiddleNode(head) {
    if (!head) return
    let fast = head
    let slow = head
    let pre = head

    while (fast && fast.next) {
        pre = slow
        slow = slow.next
        fast = fast.next.next
    }

    // 将前后两个链表断开
    pre.next = null

    return slow
}

// 21. 合并两个有序链表（双指针）
function mergeTwoLists(list1, list2) {
    const dummy = new ListNode(); // 用哨兵节点简化代码逻辑
    let cur = dummy; // cur 指向新链表的末尾
    while (list1 && list2) {
        if (list1.val < list2.val) {
            cur.next = list1; // 把 list1 加到新链表中
            list1 = list1.next;
        } else { // 注：相等的情况加哪个节点都是可以的
            cur.next = list2; // 把 list2 加到新链表中
            list2 = list2.next;
        }
        cur = cur.next;
    }
    cur.next = list1 ?? list2; // 拼接剩余链表
    return dummy.next;
}

/**
 * @param {ListNode} head
 * @return {ListNode}
 */
var sortList = function (head) {
    // 分治
    if (head === null || head.next === null) return head
    let middleNode = getMiddleNode(head)
    middleNode = sortList(middleNode)
    head = sortList(head)
    return mergeTwoLists(middleNode, head)
}

```
# 23 合并K有序链表
```js
// 21. 合并两个有序链表（双指针）
function mergeTwoLists(list1, list2) {
    const dummy = new ListNode() // 用哨兵节点简化代码逻辑
    let cur = dummy // cur 指向新链表的末尾
    while (list1 && list2) {
        if (list1.val < list2.val) {
            cur.next = list1 // 把 list1 加到新链表中
            list1 = list1.next
        } else {
            // 注：相等的情况加哪个节点都是可以的
            cur.next = list2 // 把 list2 加到新链表中
            list2 = list2.next
        }
        cur = cur.next
    }
    cur.next = list1 ?? list2 // 拼接剩余链表
    return dummy.next
}

var mergeKLists = function (lists) {
	// 分治
    if (lists.length === 0) return null
    if (lists.length === 1) return lists[0]

    const mid = Math.floor(lists.length / 2)
    const left = mergeKLists(lists.slice(0, mid))
    const right = mergeKLists(lists.slice(mid))

    return mergeTwoLists(left, right)
}

```
# 226 翻转二叉树
```js
/**
 * @param {TreeNode} root
 * @return {TreeNode}
 */
var invertTree = function (root) {
    if (!root) return root
	
	// 交换root的两个节点
    let tempTreeNode = null
    tempTreeNode = root.right
    root.right = root.left
    root.left = tempTreeNode
	
	// 递归调用
    invertTree(root.right)
    invertTree(root.left)
	
    return root
}
```
# 160 相交链表
给你两个单链表的头节点 `headA` 和 `headB` ，请你找出并返回两个单链表相交的起始节点。如果两个链表不存在相交节点，返回 `null` 。

```js
/**
 * Definition for singly-linked list.
 * function ListNode(val) {
 *     this.val = val;
 *     this.next = null;
 * }
 */

var getIntersectionNode = function(headA, headB) {
    let p = headA, q = headB;
    while (p !== q) {
        p = p ? p.next : headB;
        q = q ? q.next : headA;
    }
    return p;
};
```

核心的思路就是，一个指针先走A链再走B，另一个反之：
- 设链表A长度为 `a + c`，链表B长度为 `b + c`，其中 `c` 是公共部分长度
- 指针A走完链表A后走链表B：`a + c + b`
- 指针B走完链表B后走链表A：`b + c + a`
- 两者都会在第一个公共节点相遇
# 101 对称二叉树
给你一个二叉树的根节点 `root` ， 检查它是否轴对称。

我的思路是先根遍历，一个优先遍历左孩子，另一个是右孩子，如果这两个节点的类型是不同的（相同： 都存在，或者都不存在）
- p.val 等于 q.val。
- p 的左儿子与 q 的右儿子互为镜像，递归判断。
- p 的右儿子与 q 的左儿子互为镜像，递归判断。

```js
/**
 * @param {TreeNode} root
 * @return {boolean}
 */
var isSymmetric = function (root) {
    function isSameTree(l, r) {
        if (l === null || r === null) {
            return l === r
        }
        return (
            l.val === r.val &&
            isSameTree(l.left, r.right) &&
            isSameTree(l.right, r.left)
        )
    }

    return isSameTree(root.left, root.right)
}
```

这个和灵神的思路是一样的，二叉树的题基本上就是递归了
# 543 二叉树的直径
给你一棵二叉树的根节点，返回该树的 **直径** 。
二叉树的 **直径** 是指树中任意两个节点之间最长路径的 **长度** 。这条路径可能经过也可能不经过根节点 `root` 。
两节点之间路径的 **长度** 由它们之间边数表示。

我的想法是，不过根结点的可能性就是没有另一科子树，如果有另一棵子树就一定过根结点

我们要将这个转化为求取子树的深度，将两个深度相加，没有子树，也就是深度为零。
```js
function deep(root) {
    if (root === null) return 0
    return Math.max(deep(root.left), deep(root.right)) + 1
}

/**
 * @param {TreeNode} root
 * @return {number}
 */
var diameterOfBinaryTree = function (root) {
    return deep(root.left) + deep(root.right)
}
// [4,-7,-3,null,null,-9,-3,9,-7,-4,null,6,null,-6,-6,null,null,0,6,5,null,9,null,null,-1,-4,null,null,null,-2]，会在这个例子中报错，原因是我只考虑了过root的情况，没过root，不代表不过子树中的root，也就是这个最大的直径产生在一个子树的内部
```
代码只计算了**经过根节点 `root`** 的最长路径，即 `根节点左子树的深度 + 根节点右子树的深度`。
然而，二叉树的直径定义是**任意两个节点之间**的最长路径。这条最长路径**不一定**会经过整棵树的根节点。它可能完全位于某个子树内部。

在计算每个节点深度的同时，也计算一下**经过该节点**的最长路径，并用一个全局变量来记录所有节点中这个路径长度的最大值。
```js
/**
 * @param {TreeNode} root
 * @return {number}
 */
var diameterOfBinaryTree = function (root) {
    // 1. 定义全局变量来记录最大直径
    let maxDiameter = 0

    // 2. 定义一个辅助函数来计算深度，并在过程中更新最大直径
    function deep(node) {
        if (node === null) return 0

        // 3. 递归计算左右子树的深度
        const leftDepth = deep(node.left)
        const rightDepth = deep(node.right)

        // 4. 【核心】更新最大直径
        // 经过当前节点的最长路径 = 左子树深度 + 右子树深度
        maxDiameter = Math.max(maxDiameter, leftDepth + rightDepth)

        // 5. 返回当前子树的深度，供父节点使用
        return Math.max(leftDepth, rightDepth) + 1
    }

    deep(root) // 启动递归
    return maxDiameter
};
```

至于我个人的实现，可以将其改造一下，将原来的必过根的算法，对每个节点都应用一下：
```js
function deep(root) {
    if (root === null) return 0
    return Math.max(deep(root.left), deep(root.right)) + 1
}

/**
 * @param {TreeNode} root
 * @return {number}
 */
var diameterOfBinaryTree1 = function (root) {
    return deep(root.left) + deep(root.right)
}

function diameterOfBinaryTree(root) {
    let max = 0
	
    const getMax = (root) => {
        if(root===null) return 0
        return Math.max(
            diameterOfBinaryTree1(root),
            getMax(root.left),
            getMax(root.right),
        )
    }
	
    max = Math.max(max, getMax(root))
	
    return max
}

```
![[Pasted image 20260426165236.png]]
数据不太好看

```js
var diameterOfBinaryTree = function(root) {
    let ans = 0;

    // 返回 node 子树的最大链长
    function dfs(node) {
        if (node === null) {
            return -1; // 对于叶子来说，链长就是 -1+1=0
        }
        const lLen = dfs(node.left) + 1; // 左子树最大链长+1
        const rLen = dfs(node.right) + 1; // 右子树最大链长+1
        ans = Math.max(ans, lLen + rLen); // 两条链拼成路径
        return Math.max(lLen, rLen); // 当前子树最大链长
    }

    dfs(root);
    return ans;
};
```
#  124 二叉树中的最大路径和
这题和上一道很像
```js
var maxPathSum = function(root) {
    let ans = -Infinity;
    function dfs(node) {
        if (node === null) {
            return 0; // 没有节点，和为 0
        }
        const lVal = dfs(node.left); // 左子树最大链和
        const rVal = dfs(node.right); // 右子树最大链和
        ans = Math.max(ans, lVal + rVal + node.val); // 两条链拼成路径
        return Math.max(Math.max(lVal, rVal) + node.val, 0); 
        // 当前子树最大链和（注意这里和 0 取最大值了）
    }
    dfs(root);
    return ans;
};
```

# 102 二叉树的层序遍历
给你二叉树的根节点 `root` ，返回其节点值的 **层序遍历** 。 （即逐层地，从左到右访问所有节点）。

我的思路是，保存两个数组，一个当前层，一个是下一层，当前层的直接子节点就是下一层的内容，不断地将下一层换到当前层，直到下一层什么都没有的时候：
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
# 230 二叉树中获取第K小
#二叉树
描述：
思路：
中序遍历的情况下，第一个返回的就是最小值，返回K次后，就是目标值
代码：
```js
/**
 * @param {TreeNode} root
 * @param {number} k
 * @return {number}
 */

var kthSmallest = function(root, k) {
    let c = k
    let ans = 0
    function dfs(node){
        if(!node) return

        dfs(node.left)
        c -= 1
        if(c === 0) ans = node.val
        dfs(node.right)
    }

    dfs(root)
    return ans
};
```
# 98 检验搜索二叉树合规性
#二叉树 
二叉搜索树，则要求左子树所有节点小于根，右子树所有节点大于根。不能只判断根节点和其孩子节点的值，要遍历一个节点的全部孩子：
```js
/**
 * Definition for a binary tree node.
 * class TreeNode {
 *     val: number
 *     left: TreeNode | null
 *     right: TreeNode | null
 *     constructor(val?: number, left?: TreeNode | null, right?: TreeNode | null) {
 *         this.val = (val===undefined ? 0 : val)
 *         this.left = (left===undefined ? null : left)
 *         this.right = (right===undefined ? null : right)
 *     }
 * }
 */

function isValidBST(root: TreeNode | null): boolean {
    if (!root) return true

    if (!(dfsR(root.right, root.val) && dfsL(root.left, root.val))
        || !isValidBST(root.left)
        || !isValidBST(root.right)) {
        return false
    }
    return true
};

const dfsL = (Lch, value) => {
    if (!Lch) return true
    if (!dfsL(Lch.left, value) || !dfsL(Lch.right, value)) return false

    if (Lch.val >= value) return false

    return true
}

const dfsR = (Rch, value) => {
    if (!Rch) return true
    if (!dfsR(Rch.left, value) || !dfsR(Rch.right, value)) return false

    if (value >= Rch.val) return false

    return true
}
```
我是递归去做的，这个就比较低效了，可以使用中序遍历，返回的值如果是严格递增的就是一棵合规的搜索二叉树了：
```js
/**
 * Definition for a binary tree node.
 * class TreeNode {
 *     val: number
 *     left: TreeNode | null
 *     right: TreeNode | null
 *     constructor(val?: number, left?: TreeNode | null, right?: TreeNode | null) {
 *         this.val = (val===undefined ? 0 : val)
 *         this.left = (left===undefined ? null : left)
 *         this.right = (right===undefined ? null : right)
 *     }
 * }
 */

function isValidBST(root: TreeNode | null): boolean {
    let arr = []

    function dfs(node) {
        if (!node) return
        dfs(node.left)
        arr.push(node.val)
        dfs(node.right)
    }

    dfs(root)
    console.log(arr)

    for (let i = 0; i < arr.length - 1; i++) {
        if (arr[i] >= arr[i + 1]) return false
    }

    return true
};
```
# 199 二叉树右视图
就是广度优先遍历，将每一层的最后一个节点的值加入数组即可
```js
/**
 * Definition for a binary tree node.
 * class TreeNode {
 *     val: number
 *     left: TreeNode | null
 *     right: TreeNode | null
 *     constructor(val?: number, left?: TreeNode | null, right?: TreeNode | null) {
 *         this.val = (val===undefined ? 0 : val)
 *         this.left = (left===undefined ? null : left)
 *         this.right = (right===undefined ? null : right)
 *     }
 * }
 */

function rightSideView(root: TreeNode | null): number[] {
    if(!root) return []
	
    const ans =[]
    let cur = [root]
	
    while(cur.length){
        // 放入最后一个
        ans.push(cur[cur.length - 1].val)
		
        const nxt = []
        for(let node of cur){
            if(node.left) nxt.push(node.left)
            if(node.right) nxt.push(node.right)
        }
        cur = nxt
    }
	
    return ans
};
```
# 114 二叉树转链表 ⌚️
采用头插法构建链表，也就是从节点 6 开始，在 6 的前面插入 5，在 5 的前面插入 4，依此类推。

为此，要按照 6→5→4→3→2→1 的顺序访问节点。如何遍历这棵树，才能实现这个顺序？

按照右子树 - 左子树 - 根的顺序 DFS 这棵树。

DFS 的同时，记录当前链表的头节点为 head。一开始 head 是空节点。

具体来说：
如果当前节点为空，返回。
递归右子树。
递归左子树。
把 root.left 置为空。
头插法，把 root 插在 head 的前面，也就是 root.right=head。
现在 root 是链表的头节点，把 head 更新为 root。
```js
/**
 * Definition for a binary tree node.
 * class TreeNode {
 *     val: number
 *     left: TreeNode | null
 *     right: TreeNode | null
 *     constructor(val?: number, left?: TreeNode | null, right?: TreeNode | null) {
 *         this.val = (val===undefined ? 0 : val)
 *         this.left = (left===undefined ? null : left)
 *         this.right = (right===undefined ? null : right)
 *     }
 * }
 */

/**
 Do not return anything, modify root in-place instead.
 */
function flatten(root: TreeNode | null): void {
    let head = null

    function dfs(node){
        if(!node) return 

        dfs(node.right)
        dfs(node.left)

        node.left = null
        node.right = head

        head = node

    }

    dfs(root)
};
```
# 108 有序数组转平衡二叉树
```js
/**
 * Definition for a binary tree node.
 * class TreeNode {
 *     val: number
 *     left: TreeNode | null
 *     right: TreeNode | null
 *     constructor(val?: number, left?: TreeNode | null, right?: TreeNode | null) {
 *         this.val = (val===undefined ? 0 : val)
 *         this.left = (left===undefined ? null : left)
 *         this.right = (right===undefined ? null : right)
 *     }
 * }
 */

function sortedArrayToBST(nums: number[]): TreeNode | null {

    function dfs(left, right) {
        if (left === right) return null
        let m = Math.floor((left + right) / 2)
        return new TreeNode(nums[m], dfs(left, m), dfs(m+1, right))
    }

    return dfs(0, nums.length)
};
```
# 105 前序+中序=>构造二叉树
这道题就是可以使用
```js
/**
 * Definition for a binary tree node.
 * class TreeNode {
 *     val: number
 *     left: TreeNode | null
 *     right: TreeNode | null
 *     constructor(val?: number, left?: TreeNode | null, right?: TreeNode | null) {
 *         this.val = (val===undefined ? 0 : val)
 *         this.left = (left===undefined ? null : left)
 *         this.right = (right===undefined ? null : right)
 *     }
 * }
 */

var buildTree = function(preorder, inorder) {
    const n = preorder.length;
    if (n === 0) { // 空节点
        return null;
    }
    const leftSize = inorder.indexOf(preorder[0]); // 左子树的大小
    const pre1 = preorder.slice(1, 1 + leftSize);
    const pre2 = preorder.slice(1 + leftSize);
    const in1 = inorder.slice(0, leftSize);
    const in2 = inorder.slice(1 + leftSize, n);
    const left = buildTree(pre1, in1);
    const right = buildTree(pre2, in2);
    return new TreeNode(preorder[0], left, right);
};
```
# 236 二叉树的最近公共祖先
答案只有两种情况：
- 这两个点是某个节点的子孙。也直接返回，因为下面肯定没有，在另一个子树上。
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
# 994 寻找腐烂橘子
每次将上下左右的橘子变为2
```js
function orangesRotting(grid: number[][]): number {
    let m = grid.length
    let n = grid[0].length
    let count = 0
    let fresh = 0
    let rotted = []
    let rottedNext = []

    function rot(i, j) {
        console.log(i, j)
        grid[i][j] = 0
        for (const [x, y] of [[i - 1, j], [i, j - 1], [i + 1, j], [i, j + 1]]) {
            if (0 <= x && x < m && 0 <= y && y < n && grid[x][y] === 1) {
                grid[x][y] = 2
                rottedNext.push([x, y])
                fresh--
            }
        }
    }

    function findRot() {
        for (let i = 0; i < m; i++) {
            for (let j = 0; j < n; j++) {
            // console.log('666', grid[i][j])
                if (grid[i][j] === 2) {
                    rotted.push([i, j])
                }
                if (grid[i][j] === 1) {
                    
                    fresh++
                }
            }
        }


    }

    findRot()
    console.log(fresh, rotted.length)
    if (fresh && rotted.length === 0) return -1

    while (rotted.length !== 0 && fresh) {
        console.log(rotted)
        rotted.forEach((item, index) => {
            rot(item[0], item[1])
        })
        rotted = Array.from(rottedNext)
        rottedNext = []
        count++
    }


    return fresh ? -1 : count
};
```
# 46 全排列
#回溯
```js
function permute(nums: number[]): number[][] {
    const n = nums.length
    const path = Array(n).fill(0)
    const onPath = Array(n).fill(false)
    let ans = []

    function dfs(i){
        if(i === n){
            ans.push(path.slice())
            return
        }

        for(let j = 0; j<n; j++){
            if(!onPath[j]){
                path[i] = nums[j]

                onPath[j]=true
                dfs(i+1)
                onPath[j]=false
            }
        }
    }

    dfs(0)
    return ans
};
```
# 78 子集
给你一个整数数组 `nums` ，数组中的元素 **互不相同** 。返回该数组所有可能的子集（幂集）。

解集 **不能** 包含重复的子集。你可以按 **任意顺序** 返回解集。
```js
function subsets(nums: number[]): number[][] {
    const n = nums.length
    const path = []
    // const onPath = Array(n).fill(false)
    let ans = []

    function dfs(i){
        if(i === n){
            ans.push(path.slice())
            return
        }

        // 不选，什么都不做
        dfs(i+1)

        // 选了，加入数组，递归后，恢复现场 
        path.push(nums[i])
        dfs(i+1)
        path.pop()
    }

    dfs(0)
    return ans
};
```
# 22 括号生成
数字 `n` 代表生成括号的对数，请你设计一个函数，用于能够生成所有可能的并且 **有效的** 括号组合。
```js
function generateParenthesis(n: number): string[] {
    let ans = []
    let m = 2 * n
    let path = Array(m)


    function dfs(i, open) {
        if (i === m) {
            ans.push(path.join(""))
            return
        }

        if (open < n) {
            path[i] = "("
            dfs(i + 1, open + 1)
        }
        if (i - open < open) {
            path[i] = ")"
            dfs(i + 1, open)
        }
    }

    dfs(0, 0)
    return ans
};
```
# 131 分割回文串
#回溯 
给你一个字符串 `s`，请你将 `s` 分割成一些 子串，使每个子串都是 **回文串** 。返回 `s` 所有可能的分割方案
```js
function partition(s: string): string[][] {
    // 这道题和78 子集很像，78是选或者不选，这道是在这里分割或不分割
    // 长为n的串可以分0到n-1次

    // dfs(i)表示在s[i]后面这里的分割情况，从i到n-1

    let ans = []
    let n = s.length
    let path = []

    function dfs(i) {
        if (i === n) {
            ans.push(path.slice())
            return
        }

        for(let j = i; j<n; j++){
            if(Palindrome(s, i, j)){
                path.push(s.substring(i, j + 1)); // 分割！
                // 现在 s 未被分割的部分为 [j+1, n-1]
                dfs(j + 1);
                path.pop(); // 恢复现场
            }
        }
    }

    dfs(0)

    return ans
};

// function Palindrome(s, left, right) {
//     while (left < right) {
//         if (s.charAt(left++) !== s.charAt(right--)) {
//             return false;
//         }
//     }
//     return true;
// }

function Palindrome (s, l, r){
    while(l<r){
        // console.log(s[l],s[r],s[l]!==s[r])
        if(s[l]!==s[r]){
            return false
        }
        l++
        r--
    }
    return true
}

// s = "aab"
// [["a","a","b"],["aa","b"]]
```
# 51 N皇后
#回溯 
```js
function solveNQueens(n: number): string[][] {
    // 在棋盘的每一行上尝试去放且只放一个，不能与之前的皇后在同一列，或者斜着的位置

    let ans = []

    // 长为n，path[i]的位置为0至n-1，标记皇后的位置
    let path = Array(n).fill(null)

    // 对于列与斜着的判断，path[]中如果有的数组就是不可以放的列号
    // 对于 ↗ 方向的格子，行号加列号是不变的。对于 ↖ 方向的格子，行号减列号是不变的。
    // 用两个辅助数组记录

    // const col = []
    const diag1 = []
    const diag2 = []

    // dfs(i) 表示第i行（第i个）皇后的处理
    function dfs(i) {
        if (i === n) {
            ans.push(path.map(c => '.'.repeat(c) + 'Q' + '.'.repeat(n - 1 - c)))
            return
        }

        // 遍历可能的位置
        for (let j = 0; j < n; j++) {
            const ij = i - j + n - 1;
            if (path.indexOf(j) == -1 && !diag1[i + j] && !diag2[ij]) {
                path[i] = j; // 直接覆盖，无需恢复现场
                diag1[i + j] = diag2[ij] = true; // 皇后占用了 j 列和两条斜线
                dfs(i + 1);
                diag1[i + j] = diag2[ij] = false; // 恢复现场
                path[i] = null // 恢复现场
            }

        }

    }

    dfs(0)

    return ans
};
```
# 35 数组插入的位置
#二分查找
给定一个排序数组和一个目标值，在数组中找到目标值，并返回其索引。如果目标值不存在于数组中，返回它将会被按顺序插入的位置。
```js
function searchInsert(nums: number[], target: number): number {
    // 这里我使用的是闭区间的写法
    let left = 0
    let right = nums.length - 1

    while (left <= right) {
        const mid = Math.floor((left + right) / 2)
        // 如果所有数都小于 target，那么循环中更新的只有 left，无论下面哪种二分写法，最后都一定会返回数组长度，所以无需特判这种情况。
        if(nums[mid]<target){
            left = mid + 1
        }else{
            right = mid - 1
        }
    }

    return left
};
```
# 74 搜索二维数组
#二分查找 
```js
function searchMatrix(matrix: number[][], target: number): boolean {
    for (let arr of matrix) {
        console.log(arr, searchInsert(arr, target))
        if (searchInsert(arr, target)) return true

    }

    return false
};

function searchInsert(arr, target) {
    // 将35题的函数进行改造，如果mid是target就返回true
    let left = 0
    let right = arr.length - 1

    while (left <= right) {
        console.log(left, right)
        const mid = Math.floor((left + right) / 2)
        if (arr[mid] === target) return true
        if (arr[mid] < target) {
            left = mid + 1
        } else {
            right = mid - 1
        }
    }

    return false
}
```
# 34 在排序数组中寻找元素的第一个位置与最后一个位置
给你一个按照非递减顺序排列的整数数组 `nums`，和一个目标值 `target`。请你找出给定目标值在数组中的开始位置和结束位置。

如果数组中不存在目标值 `target`，返回 `[-1, -1]`。
```js
function searchRange(nums: number[], target: number): number[] {
    let start = searchInsert(nums, target)
    // searchInsert(nums, target)          寻找 >= target的第一个位置
    // searchInsert(nums, target + 1)      寻找 >  target的第一个位置
    // searchInsert(nums, target) - 1      寻找 <  target的第一个位置
    // searchInsert(nums, target + 1) -1   寻找 <= target的第一个位置

    // 这里就具体情况具体分析吧，反正都可以通过 lower_bound() 来解决
    if(start===nums.length || nums[start] !== target){
        return [-1, -1]
    }

    let end = searchInsert(nums, target + 1) - 1

    return [start, end]
};

function searchInsert(nums: number[], target: number): number {
    // 这里我使用的是闭区间的写法
    let left = 0
    let right = nums.length - 1

    while (left <= right) {
        const mid = Math.floor((left + right) / 2)
        // 如果所有数都小于 target，那么循环中更新的只有 left，无论下面哪种二分写法，最后都一定会返回数组长度，所以无需特判这种情况。
        if(nums[mid]<target){
            left = mid + 1
        }else{
            right = mid - 1
        }
    }

    return left
};
```
# 153 寻找旋转排序数组中的最小值
将旋转排序数组中的最后一个数与mid比较：
- 如果mid > 最后一个数，代表最小值在mid右侧
- 反之，最小值在mid右侧
	可以画图来分析一下
```js
// 寻找旋转排序数组中的最小值
function findMin(nums) {
    // 开区间(-1, n-1)
    let left = -1
    let right = nums.length - 1

    while (left + 1 < right) {
        const mid = Math.floor((left + right) / 2)

        if (nums[mid] < nums[nums.length - 1]) {
            right = mid
        } else {
            left = mid
        }
    }
    return nums[right]
}
```
# 33 搜索旋转数组
在传递给函数之前，`nums` 在预先未知的某个下标 `k`（`0 <= k < nums.length`）上进行了 **向左旋转**，使数组变为 `[nums[k], nums[k+1], ..., nums[n-1], nums[0], nums[1], ..., nums[k-1]]`（下标 **从 0 开始** 计数）。例如， `[0,1,2,4,5,6,7]` 下标 `3` 上向左旋转后可能变为 `[4,5,6,7,0,1,2]` 。

给你 **旋转后** 的数组 `nums` 和一个整数 `target` ，如果 `nums` 中存在这个目标值 `target` ，则返回它的下标，否则返回 `-1` 。

	输入：nums = [4,5,6,7,0,1,2], target = 0
	输出：4

```js
// 寻找旋转排序数组中的最小值（返回的是下标）
function findMin(nums) {
    // 开区间(-1, n-1)
    let left = -1
    let right = nums.length - 1

    while (left + 1 < right) {
        const mid = Math.floor((left + right) / 2)

        if (nums[mid] < nums[nums.length - 1]) {
            right = mid
        } else {
            left = mid
        }
    }
    return right
}

// 有序数组中找 target 的下标
var lowerBound = function (nums, left, right, target) {
    while (left + 1 < right) { // 开区间不为空
        // 循环不变量：
        // nums[right] >= target
        // nums[left] < target
        const mid = Math.floor((left + right) / 2);
        if (nums[mid] >= target) {
            right = mid; // 范围缩小到 (left, mid)
        } else {
            left = mid; // 范围缩小到 (mid, right)
        }
    }
    return nums[right] === target ? right : -1;
};

function search(nums: number[], target: number): number {
    let minIndex = findMin(nums)
    if (target > nums[nums.length - 1]) {
        return lowerBound(nums, -1, minIndex, target)
    } else {
        return lowerBound(nums, minIndex - 1, nums.length, target)
    }

};
```
# 4 寻找两个正序数组的中位数
没做
# 20 有效括号
#栈 
```js
function isValid(s: string): boolean {
    let stack = []

    for(let i = 0; i<s.length; i++){
        // 遍历s

        // 左括号直接入栈
        if(s[i]==='('||s[i]==='{'||s[i]==='['){
            stack.push(s[i])
        }

        // 右括号就从栈中弹出一个，检查是否匹配
        if(s[i]===')'){
            let char = stack.pop()
            if(char!=='(') return false
        }
        if(s[i]===']'){
            let char = stack.pop()
            if(char!=='[') return false
        }
        if(s[i]==='}'){
            let char = stack.pop()
            if(char!=='{') return false
        }
    }

    // 最后检查栈是否为空
    if(stack.length !== 0) return false

    // 空栈就返回true 
    return true
};
```
# 155 最小栈
#栈 
设计两个站，一个是普通的栈，另一个为最小栈：
- 当num<=最小栈顶的数，num压入
- 反之，压入最小栈顶的值
弹出的时候要同步的弹出
```js
class MinStack {
    stack:number[] = [];
    minStack:number[] = [];

    push(val: number): void {
        this.stack.push(val);
        this.minStack.push(Math.min(val, this.getMin() ?? val));
    }

    pop(): void {
        this.stack.pop();
        this.minStack.pop();
    }

    top(): number {
        return this.stack[this.stack.length - 1];
    }

    getMin(): number {
        return this.minStack[this.minStack.length - 1];
    }
}
```
# 394 字符串接吗
#栈 #递归
```js
function decodeString(s: string): string {
    // 遇到字母直接加入结果
    // 数字n便开始读取[str]中的内容str
    // 重复n次str加入结果

    // 上述实现没有考虑到嵌套的情况


    if (s.length === 0) {
        return s;
    }

    // s[0] 是字母
    if ('a' <= s[0] && s[0] <= 'z') {
        // 分离出 s[0]，解码剩下的
        return s[0] + decodeString(s.slice(1));
    }

    // s[0] 是数字，后面至少有一对括号
    const i = s.indexOf('['); // 找左括号
    let balance = 1; // 左括号个数减去右括号个数
    for (let j = i + 1; ; j++) {
        if (s[j] === '[') {
            balance++;
        } else if (s[j] === ']') {
            balance--;
            if (balance === 0) { // 左右括号个数相等，找到与 s[i] 匹配的右括号 s[j]
                const k = parseInt(s.slice(0, i));
                return decodeString(
	                s.slice(i + 1, j)).repeat(k) + decodeString(s.slice(j + 1)
	            );
            }
        }
    }
}
```
# 739 每日气温
给定一个整数数组 `temperatures` ，表示每天的温度，返回一个数组 `answer` ，其中 `answer[i]` 是指对于第 `i` 天，下一个更高温度出现在几天后。如果气温在这之后都不会升高，请在该位置用 `0` 来代替。

使用单调栈来实现：
- 从左到右：栈中始终维护着当前没有找到下一个更大的值的数
- 从右到左：维护着可以成为下一个更大值的数
```js
function dailyTemperatures(temperatures: number[]): number[] {
    // ans最后一个一定是0

    // 我的思路是，遍历这个temperatures，如果curIndex的值小于nxtIndex，那就ans中加入1，否则加入标记
    // 之后遍历ans，在对应的标记处去寻找其后大于他的值，更新ans
    // 这个思路其实就是一个双层循环暴力，时间O(n^2)，而且实现起来，起来更加麻烦

    // 从左到右的实现
    let n = temperatures.length
    let ans = Array(n).fill(0)

    // 维护着没有找到下一个更大的值的下标
    let stack = []

    for(let i = 0 ;i<n; i++){
        const temperature = temperatures[i]

        while(stack.length && temperature > temperatures[stack[stack.length - 1]]){
            const j =  stack.pop()
            ans[j] = i - j
        }

        stack.push(i)
    }
    
    return ans
};
```

```js
// 还是上面👆的实现更加易懂
function dailyTemperatures(temperatures: number[]): number[] {
    // 从右到左的实现
    let n = temperatures.length
    let ans = Array(n).fill(0)

    // 记录下一个更大元素的「候选项」的下标。
    let stack = []

    for (let i = n - 1; i >= 0; i--) {
        const temperature = temperatures[i]

        while (stack.length && temperature >= temperatures[stack[stack.length - 1]]) {
            stack.pop()
        }

        if (stack.length) {
            ans[i] = stack[stack.length - 1] - i
        }

        stack.push(i)
    }

    return ans
};
```
# 84 柱状图中的最大值
https://leetcode.cn/problems/largest-rectangle-in-histogram/description/?envType=study-plan-v2&envId=top-100-liked

```js
var largestRectangleArea = function(heights) {
    const n = heights.length;
    const left = Array(n).fill(-1);
    const st = [];
	
    // 一个单调递增的栈，在push一个值之前，栈顶的index就是这个左侧更小的下标
    for (let i = 0; i < n; i++) {
        const h = heights[i];
        while (st.length && heights[st[st.length - 1]] >= h) {
            st.pop();
        }
        if (st.length) {
            left[i] = st[st.length - 1];
        }
        st.push(i);
    }
	
    // 反方向遍历
    const right = Array(n).fill(n);
    st.length = 0;
    for (let i = n - 1; i >= 0; i--) {
        const h = heights[i];
        while (st.length && heights[st[st.length - 1]] >= h) {
            st.pop();
        }
        if (st.length) {
            right[i] = st[st.length - 1];
        }
        st.push(i);
    }
	
	console.log(left, right)
	
    let ans = 0;
    for (let i = 0; i < n; i++) {
        ans = Math.max(ans, heights[i] * (right[i] - left[i] - 1));
    }
    return ans;
};
```
# 215 数组中的第K个最大元素
https://www.bilibili.com/video/BV1hTfBBuE4T/?spm_id_from=333.337.search-card.all.click&vd_source=47c9acd507be61251cd2bb730416395c
```js
// 快速选择解法
function findKthLargest(nums: number[], k: number): number {
    // 随便选一个数，以这个数为准，将数组分为大于，小于，等于这个数的三个数组
    let pivot = nums[Math.floor(Math.random() * (nums.length - 1))]
    console.log(pivot)

    let left = nums.reduce((acc, cur) => {
        if (cur > pivot) {
            acc.push(cur)
        }
        return acc
    }, [])
    console.log(left)

    let mid = nums.reduce((acc, cur) => {
        if (cur === pivot) {
            acc.push(cur)
        }
        return acc
    }, [])
    console.log(mid)

    let right = nums.reduce((acc, cur) => {
        if (cur < pivot) {
            acc.push(cur)
        }
        return acc
    }, [])
    console.log(right)

    // left.length + 1的长度代表了pivot在数组中第k大的k
    if (k <= left.length) {
        // 这种情况下，答案在left中
        return findKthLargest(left, k)
    } else if (k <= left.length + mid.length) {
        // 这种情况其实就是说，如果你的pivot落在mid数组中，那就是第k大
        return pivot
    } else {
        // 答案在右侧，此时前面有left.length + mid.length个数，
        // 也就是转为在right中寻找k - left.length - mid.length
        return findKthLargest(right, k - left.length - mid.length)
    }
};
```
# 347 前K个高频元素
给你一个整数数组 `nums` 和一个整数 `k` ，请你返回其中出现频率前 `k` 高的元素。你可以按 **任意顺序** 返回答案。
```js
var topKFrequent = function(nums, k) {
    // 第一步：统计每个元素的出现次数
    const cnt = new Map();
    for (const x of nums) {
        cnt.set(x, (cnt.get(x) ?? 0) + 1);
    }
    const maxCnt = Math.max(...cnt.values());
    console.log(cnt)

    // 第二步：把出现次数相同的元素，放到同一个桶中
    const buckets = Array.from({ length: maxCnt + 1 }, () => []);
    for (const [x, c] of cnt.entries()) {
        buckets[c].push(x);
    }
    console.log(buckets)

    // 第三步：倒序遍历 buckets，把出现次数前 k 大的元素加入答案
    const ans = [];
    // 注意题目保证答案唯一，一定会出现某次 push 后 ans.length 恰好等于 k 的情况
    for (let i = maxCnt; ans.length < k; i--) {
        ans.push(...buckets[i]);
    }
    return ans;
};
```
# 295 数据流中的中位数
中位数把这 6 个数均分成了左右两部分，一边是 left=[1,2,3]，另一边是 right=[4,5,6]。我们要计算的中位数，就来自 left 中的最大值，以及 right 中的最小值。

随着 addNum 不断地添加数字，我们需要：

保证 left 的大小和 right 的大小尽量相等。规定：在有奇数个数时，left 比 right 多 1 个数。
保证 left 的所有元素都小于等于 right 的所有元素。
只要时时刻刻满足以上两个要求（满足中位数的定义），我们就可以用 left 中的最大值以及 right 中的最小值计算中位数。

分类讨论：

如果当前 left 的大小和 right 的大小相等：
如果添加的数字 num 比较大，比如添加 7，那么把 7 加到 right 中。现在 left 比 right 少 1 个数，不符合前文的规定，所以必须把 right 的最小值从 right 中去掉，添加到 left 中。如此操作后，可以保证 left 的所有元素都小于等于 right 的所有元素。
如果添加的数字 num 比较小，比如添加 0，那么把 0 加到 left 中。
这两种情况可以合并：无论 num 是大是小，都可以先把 num 加到 right 中，然后把 right 的最小值从 right 中去掉，并添加到 left 中。
如果当前 left 比 right 多 1 个数：
如果添加的数字 num 比较大，比如添加 7，那么把 7 加到 right 中。
如果添加的数字 num 比较小，比如添加 0，那么把 0 加到 left 中。现在 left 比 right 多 2 个数，不符合前文的规定，所以必须把 left 的最大值从 left 中去掉，添加到 right 中。如此操作后，可以保证 left 的所有元素都小于等于 right 的所有元素。
这两种情况可以合并：无论 num 是大是小，都可以先把 num 加到 left 中，然后把 left 的最大值从 left 中去掉，并添加到 right 中。
最后，我们需要什么样的数据结构？这个数据结构要能高效地执行如下操作：

添加元素。
找到最大（小）值。
删除最大（小）值。
这个数据结构是堆。

left 是最大堆，right 是最小堆。

如果当前有奇数个元素，中位数是 left 的堆顶。
如果当前有偶数个元素，中位数是 left 的堆顶和 right 的堆顶的平均值。

```js
var MedianFinder = function() {
    this.left = new MaxPriorityQueue();
    this.right = new MinPriorityQueue();
};

MedianFinder.prototype.addNum = function(num) {
    if (this.left.size() === this.right.size()) {
        this.right.enqueue(num);
        this.left.enqueue(this.right.dequeue());
    } else {
        this.left.enqueue(num);
        this.right.enqueue(this.left.dequeue());
    }
};

MedianFinder.prototype.findMedian = function() {
    if (this.left.size() > this.right.size()) {
        return this.left.front();
    }
    return (this.left.front() + this.right.front()) / 2;
};
```
# 121 买股票的最佳时机
#贪心 
给定一个数组 `prices` ，它的第 `i` 个元素 `prices[i]` 表示一支给定股票第 `i` 天的价格。

你只能选择 **某一天** 买入这只股票，并选择在 **未来的某一个不同的日子** 卖出该股票。设计一个算法来计算你所能获取的最大利润。

返回你可以从这笔交易中获取的最大利润。如果你不能获取任何利润，返回 `0` 。


从左到右枚举卖出价格 prices[i]。要想获得最大利润，哪天买入最好？在股票价格最低的那天买入。

注意，买入日期必须在卖出日期之前，所以我们求的是从 prices[0] 到 prices[i−1] 的最小值，这可以用一个变量 minPrice 维护。

由于只能买卖一次，所以在遍历中，计算 prices[i]−minPrice 的最大值，就是答案。
```js
function maxProfit(prices: number[]): number {
    let minPrice = prices[0]

    let ans = 0

    for (const p of prices) {
        ans = Math.max(ans, p - minPrice)
        minPrice = Math.min(minPrice, p)
    }

    return ans
};
```
# 55 跳跃游戏

```js
var canJump = function(nums) {
    let mx = 0;
    for (let i = 0; i < nums.length; i++) {
        if (i > mx) { // 无法到达 i
            return false;
        }
        mx = Math.max(mx, i + nums[i]); // 从 i 最右可以跳到 i + nums[i]
    }
    return true;
};
```

# 45 跳跃游戏II
https://leetcode.cn/problems/jump-game-ii/?envType=study-plan-v2&envId=top-100-liked
```js
var jump = function(nums) {
    let ans = 0;
    let curEnd = 0; // 已建造的桥的右端点
    let nextEnd = 0; // 下一座桥的右端点的最大值
    for (let i = 0; i < nums.length - 1; i++) {
        // 遍历的过程中，记录下一座桥的最远点
        nextEnd = Math.max(nextEnd, i + nums[i]);
        if (i === curEnd) { // 无路可走，必须建桥
            curEnd = nextEnd; // 建桥后，最远可以到达 nextEnd
            ans++;
        }
    }
    return ans;
};
```
# 763 字母划分
```js
// 遍历 s，计算字母 c 在 s 中的最后出现的下标 last[c]。
// 初始化当前正在合并的区间左右端点 start=0, end=0。
// 再次遍历 s，由于当前区间必须包含所有 s[i]，所以用 last[s[i]] 更新区间右端点 end 的最大值。
// 如果发现 end=i，那么当前区间合并完毕，把区间长度 end−start+1 加入答案。然后更新 start=end+1 作为下一个区间的左端点。
// 遍历完毕，返回答案。
function partitionLabels(s: string): number[] {
    // 要确定每个字母出现的范围，将重合的范围合并，最后剩余的范围就是最后的分割

    // let map = new Map()

    // for (let i = 0; i < s.length; i++) {
    //     const char =s[i]
    //     if(map.has(char)){
    //         map.set(char, [...map.get(char),i])
    //     }else{
    //         map.set(char, [i])
    //     }
    // }

    // console.log(map)
    // return []

    const n = s.length;
    const last = Array(26);
    for (let i = 0; i < n; i++) {
        last[s.charCodeAt(i) - 'a'.charCodeAt(0)] = i; // 每个字母最后出现的下标
    }

    const ans = [];
    let start = 0, end = 0;
    for (let i = 0; i < n; i++) {
        end = Math.max(end, last[s.charCodeAt(i) - 'a'.charCodeAt(0)]); // 更新当前区间右端点的最大值
        if (end === i) { // 当前区间合并完毕
            ans.push(end - start + 1); // 区间长度加入答案
            start = end + 1; // 下一个区间的左端点
        }
    }
    return ans;
};
```
# 300 递增最长子序列 ⌚️
 #动态规划
 `dp[i]`表示已`num[i]`结尾的递增子序列的长度
```js
function lengthOfLIS(nums: number[]): number {
    // dp[i] 表示长为i的数组的最长递归子序列长度

    const dp = Array(nums.length).fill(1)
    // dp[0] = 0

    for (let i = 0; i < nums.length; i++) {
        for (let j = 0; j < i; j++) {
            if (nums[i] > nums[j])
                dp[i] = Math.max(dp[j] + 1, dp[i])
        }
    }

    console.log(dp)
    return Math.max(...dp)
};
```

带有路径
```js
/**
 * @param {number[]} nums
 * @return {number}
 */
var lengthOfLIS = function (nums) {
    if (!nums) return
    let dp = new Array(nums.length).fill(1)
    let trace = new Array(nums.length).fill(-1)
    // console.log(dp);

    for (let i = 0; i < nums.length; i++) {
        for (let j = 0; j < i; j++) {
            if (nums[i] > nums[j]) {
                if (dp[j] + 1 > dp[i]) {
                    dp[i] = dp[j] + 1
                    trace[i] = j
                }
            }
        }
    }
    let index = dp.indexOf(Math.max(...dp))
    let res = []

    while (index !== -1) {
        res.unshift(nums[index])
        index = trace[index]
    }

    return { trace, dp, res }
}

let nums = [1, 4, 3, 6, 0, 7]
console.log(lengthOfLIS(nums))
// {
//   trace: [ -1, 0, 0, 1, -1, 3 ],
//   dp: [ 1, 2, 2, 3, 1, 4 ],
//   res: [ 1, 4, 6, 7 ]
// }
```
# 279 完全平方数
https://leetcode.cn/problems/perfect-squares/?envType=study-plan-v2&envId=top-100-liked
```js
function numSquares(n: number): number {
    // dp[i]表示组成数字i的完全平方数的最小值

    // 初始值：dp[i] = i
    const dp = Array.from({ length: n + 1 }, (_, i) => i)
    console.log(dp)

    // 递推公式：dp[i] = min(dp[i], dp[i - j * j] + 1)
    for (let i = 0; i < n + 1; i++) {
        for (let j = 1; j * j <= i; j++) {
            dp[i] = Math.min(dp[i], dp[i - j * j] + 1)
        }
    }
    console.log(dp)

    return dp[n]
};
```
# 322 找零钱
https://leetcode.cn/problems/coin-change/?envType=study-plan-v2&envId=top-100-liked
```js
function coinChange(coins: number[], amount: number): number {
    const dp = Array(amount + 1).fill(Infinity)
    dp[0] = 0

    for(let i = 1; i <= amount; i++){
        // 遍历每一枚硬币
        for(let j = 0; j < coins.length; j++){
            // 只有当当前硬币的面值小于等于当前要凑的金额 i 时，才能使用
            if (coins[j] <= i) {
                dp[i] = Math.min(dp[i], dp[i - coins[j]] + 1)
            }
        }
    }

    console.log(dp)

    return dp[amount] === Infinity ? -1 : dp[amount]
};
```
# 139 单词拆分
题解
https://www.bilibili.com/video/BV1pd4y147Rh?spm_id_from=333.788.videopod.sections&vd_source=47c9acd507be61251cd2bb730416395c
题目
https://leetcode.cn/problems/word-break/description/?envType=study-plan-v2&envId=top-100-liked
```js
function wordBreak(s: string, wordDict: string[]): boolean {
    const dp = Array(s.length + 1).fill(false)
    dp[0] = true

    // dp[i] 表示长为i的字符串能否被wordDict表示
    for(let i = 1; i <= s.length; i++){
        for(let j = 0; j < i; j++){
            // 获取i之前的子串，如果子串之前的串为true，并且子串在字典中
            // 哈，还是看视频吧，这不太好描述
            const subStr = s.slice(j, i)
            console.log(subStr)
            if(wordDict.includes(subStr) && dp[j]){
                dp[i] = true
            }
        }
    }

    console.log(dp)

    return dp[s.length]
};
```