# CodeTop 100
这里的题目的编号和LeetCode一致，相同的题目只有编号。
据我统计，岗位不限中，前80道题目全部做完，基本上可以覆盖前端常考的题目，前端做前60道就可以了。
# 3 无重复字符的最长子串 ⌚️
#双指针 #滑动窗口
https://leetcode.cn/problems/longest-substring-without-repeating-characters/description/
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