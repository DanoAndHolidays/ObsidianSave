# 03 Tabs 无障碍：Roving Tabindex
> Last Format Time：9/16/2026 19:24:52

> Last Format Time：2026-08-28
> Status：已完成
> 笔记说明：Roving Tabindex、ARIA Tabs Pattern，以及 selection 与 focus 的分离。

---
## 核心规则
Roving tabindex 让一组复合控件在整个页面的 Tab 顺序中只保留一个入口：
- 当前可通过 Tab 键进入的项目使用 `tabIndex={0}`
- 同组其他项目使用 `tabIndex={-1}`
- 方向键移动焦点时，应把 `tabIndex={0}` 同步转移到新的焦点项目
- `tabIndex={-1}` 仍允许通过 `element.focus()` 获得程序化焦点

在手动激活的 Tabs 中，焦点和选中态可以不同：`tabIndex={0}` 跟随最近获得焦点的 Tab，`aria-selected` 跟随已激活的 Tab。

---
## 参考资料
- [WAI-ARIA APG：Tabs Pattern](https://www.w3.org/WAI/ARIA/apg/patterns/tabs/)
- [WAI-ARIA APG：Managing Focus in Composites Using a Roving tabindex](https://www.w3.org/WAI/ARIA/apg/practices/keyboard-interface/#kbd_roving_tabindex)
- [freeCodeCamp：HTML Roving tabindex](https://www.freecodecamp.org/news/html-roving-tabindex-attribute-explained-with-examples/)
- [MDN：ARIA](https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA)
