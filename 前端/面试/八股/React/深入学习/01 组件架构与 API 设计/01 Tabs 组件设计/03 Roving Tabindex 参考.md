# 03 Roving Tabindex 参考
> Last Format Time：8/27/2026 15:20:25

> Last Format Time：8/27/2026
> 笔记说明：Roving Tabindex、ARIA Tabs Pattern，以及 selection 与 focus 的分离。

---
## 核心规则
Roving tabindex 让一组复合控件在整个页面的 Tab 顺序中只保留一个入口：
- 当前可通过 Tab 键进入的项目使用 `tabIndex={0}`
- 同组其他项目使用 `tabIndex={-1}`
- 方向键移动焦点时，应把 `tabIndex={0}` 同步转移到新的焦点项目
- `tabIndex={-1}` 仍允许通过 `element.focus()` 获得程序化焦点

在手动激活的 Tabs 中，焦点和选中态可以不同：`tabIndex={0}` 跟随最近获得焦点的 Tab，`aria-selected` 跟随已激活的 Tab。〔CR-001〕

---
## 参考资料
- [WAI-ARIA APG：Tabs Pattern](https://www.w3.org/WAI/ARIA/apg/patterns/tabs/)
- [WAI-ARIA APG：Managing Focus in Composites Using a Roving tabindex](https://www.w3.org/WAI/ARIA/apg/practices/keyboard-interface/#kbd_roving_tabindex)
- [freeCodeCamp：HTML Roving tabindex](https://www.freecodecamp.org/news/html-roving-tabindex-attribute-explained-with-examples/)
- [MDN：ARIA](https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA)

---
## 内容审核变更记录
### CR-001｜补充说明
- 日期：8/25/2026
- 位置：`核心规则`
- 原内容：仅保存了两条外部参考链接，没有记录 roving tabindex 的行为约束。
- 调整后：补充单一 Tab 入口、方向键移动、程序化聚焦，以及手动激活模式下焦点与选中态分离的规则。
- 原因：原笔记无法独立说明该模式，也容易把 `tabIndex` 与 `aria-selected` 错误绑定。
- 依据：[WAI-ARIA APG：Tabs Pattern](https://www.w3.org/WAI/ARIA/apg/patterns/tabs/)；[WAI-ARIA APG：Managing Focus in Composites Using a Roving tabindex](https://www.w3.org/WAI/ARIA/apg/practices/keyboard-interface/#kbd_roving_tabindex)

