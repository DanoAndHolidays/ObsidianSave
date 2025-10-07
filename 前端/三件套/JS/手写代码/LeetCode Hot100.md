# 1两数之和算法实现
---
##### 问题描述
[修正术语]：给定数组 `nums` 和目标值 `target`，找出数组中两数之和等于目标值的下标。
##### 暴力解法
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
##### 哈希表优化解法
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
##### 算法分析
[补充说明]：  
- **暴力解法**：双重循环遍历所有组合，简单但效率低  
- **哈希表解法**：通过空间换时间，只需一次遍历  JS的Map是hash表吗
- **使用场景**：哈希表解法适合大规模数据，暴力解适用于小规模数据  
##### 示例测试
```javascript
// 测试用例
const nums = [2, 7, 11, 15];
const target = 9;

console.log(twoSum(nums, target)); // 输出: [0, 1]
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
# 😅
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

# 3字符的最长无重复子串
---
#双指针 #第一道自己做出来的  到目前为止的==第一道自己写出来的==Hot100
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
    console.log(min, max,set)

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

# 搜索二维矩阵
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
